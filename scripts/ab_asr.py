"""Compare ASR pipelines on real footage. Nothing is applied; numbers are printed.

Each stage is one open-source thing this project already has or can pull:
  small                 what the pipeline ships today
  distil-large-v3       Systran's distilled large-v3 — near large-v3 accuracy at
                        a fraction of the compute, which is what makes a big
                        model usable on a CPU box
  + demucs              vocal isolation BEFORE ASR. Already provisioned here and
                        never used for transcription. Handheld outdoor audio is
                        wind, road and room; separating the vocal stem is the
                        single biggest lever on this kind of material
  + hotwords            bias decoding toward this production's own vocabulary.
                        "Shumafied" is a made-up word no ASR produces unprompted

  python scripts/ab_asr.py <clip.mp4> [--stages small,distil,demucs,hotwords]
"""
import sys, os, subprocess, tempfile, time, collections, shutil

CACHE = os.path.join(os.getcwd(), '.trippedd_tools', 'models')
from faster_whisper import WhisperModel

def opt(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

clips = [a for a in sys.argv[1:] if not a.startswith('--') and os.path.exists(a)]
stages = opt('--stages', 'small,distil,demucs,hotwords').split(',')

# The show's own vocabulary. Proper nouns an ASR has never seen.
HOTWORDS = os.environ.get('TRIPPEDD_HOTWORDS') or (
    'Shumafied, Goodville, Tyneshia, Marquis, Mars, Joe, Nashville, TRIPPEDD, '
    'zigzags, Swishers, cigars, blunt'
)

def prep(path, src=None):
    """The analysis copy: mono 16k, wind/rumble removed, loudness normalised."""
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src or path, '-af',
                    'highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-ac', '1', '-ar', '16000', tmp], capture_output=True, timeout=1800)
    return tmp

def demucs_vocals(path):
    """Separate the vocal stem. Returns the stem path, or None if demucs fails."""
    out = tempfile.mkdtemp(prefix='demucs_')
    wav = os.path.join(out, 'in.wav')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', path, '-ac', '2', '-ar', '44100', wav],
                   capture_output=True, timeout=900)
    r = subprocess.run([sys.executable, '-m', 'demucs', '--two-stems', 'vocals',
                        '-n', 'htdemucs', '-d', 'cpu', '-o', out, wav],
                       capture_output=True, timeout=3600)
    for root, _, files in os.walk(out):
        for f in files:
            if f == 'vocals.wav':
                return os.path.join(root, f), out
    print('    demucs failed:', (r.stderr or b'').decode()[-200:])
    return None, out

def stats(segs):
    texts = [s.text.strip() for s in segs]
    c = collections.Counter(texts)
    rep = sum(v for k, v in c.items() if v > 1)
    run = 1; mx = 1
    for i in range(1, len(texts)):
        if texts[i] == texts[i-1]: run += 1; mx = max(mx, run)
        else: run = 1
    lp = [s.avg_logprob for s in segs]
    words = sum(len(t.split()) for t in texts)
    return dict(segs=len(segs), repeat=rep, run=mx, words=words,
                logprob=(sum(lp)/len(lp)) if lp else 0.0)

VAD = dict(vad_filter=True, vad_parameters=dict(threshold=0.5, min_silence_duration_ms=2000))
MODELS = {}
def get(size):
    if size not in MODELS:
        MODELS[size] = WhisperModel(size, device='cpu', compute_type='int8', download_root=CACHE)
    return MODELS[size]

for clip in clips:
    print('=' * 92)
    print(os.path.basename(clip))
    print('=' * 92)
    base = prep(clip)
    vocals = tmpdir = None
    if 'demucs' in stages:
        print('  separating vocal stem (demucs, CPU — this is the slow one)...')
        v, tmpdir = demucs_vocals(clip)
        vocals = prep(clip, src=v) if v else None

    runs = []
    if 'small' in stages: runs.append(('small', 'small', base, None))
    if 'distil' in stages: runs.append(('distil-large-v3', 'Systran/faster-distil-whisper-large-v3', base, None))
    if 'demucs' in stages and vocals:
        runs.append(('distil + demucs vocals', 'Systran/faster-distil-whisper-large-v3', vocals, None))
    if 'hotwords' in stages:
        src = vocals or base
        label = 'distil + demucs + hotwords' if vocals else 'distil + hotwords'
        runs.append((label, 'Systran/faster-distil-whisper-large-v3', src, HOTWORDS))

    for label, size, audio, hw in runs:
        t = time.time()
        segs = list(get(size).transcribe(audio, language='en', beam_size=5,
                                         condition_on_previous_text=False,
                                         hotwords=hw, **VAD)[0])
        st = stats(segs)
        print(f"\n  {label}   {time.time()-t:.0f}s")
        print(f"    segs {st['segs']:3d}  words {st['words']:4d}  repeated {st['repeat']:3d}  "
              f"longest-run {st['run']:2d}  mean logprob {st['logprob']:.2f}")
        for s in segs[:6]:
            print(f'      [{s.start:6.1f}] {s.text.strip()[:74]}')
        if len(segs) > 6: print(f'      ... {len(segs)-6} more')

    for p in [base, vocals]:
        if p and os.path.exists(p): os.unlink(p)
    if tmpdir: shutil.rmtree(tmpdir, ignore_errors=True)
    print()
