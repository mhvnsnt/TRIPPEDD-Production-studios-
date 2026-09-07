"""Measure WHY a clip transcribes badly, before changing anything.

Per clip: audio stream facts, measured level, silence share, VAD speech regions
under the CURRENT settings, and the ASR result including the per-segment
confidences faster-whisper already computes and we currently throw away.

The two failure signatures this is built to separate:
  SILENT   nothing came back, and the audio says why (no stream / near silence)
           versus the ASR missing speech that is demonstrably there.
  LOOP     the same line repeated, or one "segment" spanning a large share of
           the clip. A long VAD region is the suspect: faster-whisper decodes a
           region in 30s windows and maps timestamps back across the whole
           region, so an unbounded region can both stretch a timestamp and give
           the decoder the long context it loops in.

  python scripts/diagnose_asr.py <clip.mp4> [more.mp4 ...] [--model small]
"""
import sys, os, json, subprocess, tempfile, math, collections

args = [a for a in sys.argv[1:] if not a.startswith('--')]
def opt(name, default):
    if name in sys.argv: return sys.argv[sys.argv.index(name) + 1]
    return default
MODEL = opt('--model', 'small')
CACHE = opt('--cache', os.path.join(os.getcwd(), '.trippedd_models'))
# The VAD settings currently in whisper_transcribe.py.
VAD_THRESHOLD = float(opt('--vad-threshold', '0.35'))
VAD_MIN_SILENCE = int(opt('--vad-min-silence', '700'))
VAD_MAX_SPEECH = float(opt('--vad-max-speech', 'inf'))

from faster_whisper import WhisperModel, decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps

def ffprobe_audio(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a',
                        '-show_entries', 'stream=codec_name,channels,sample_rate,duration',
                        '-of', 'json', path], capture_output=True, text=True)
    try: streams = json.loads(r.stdout).get('streams', [])
    except Exception: streams = []
    return streams[0] if streams else None

def levels(path):
    """mean/max dBFS, and the share of the clip ffmpeg calls silence."""
    r = subprocess.run(['ffmpeg', '-i', path, '-af',
                        'volumedetect,silencedetect=noise=-40dB:d=0.5', '-f', 'null', '-'],
                       capture_output=True, text=True)
    err = r.stderr
    mean = mx = None
    silent = 0.0
    for line in err.splitlines():
        if 'mean_volume:' in line: mean = float(line.split('mean_volume:')[1].split('dB')[0])
        if 'max_volume:' in line: mx = float(line.split('max_volume:')[1].split('dB')[0])
        if 'silence_duration:' in line: silent += float(line.split('silence_duration:')[1])
    return mean, mx, silent

def prepared_audio(path):
    """The exact preprocessing the real transcriber applies."""
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', path, '-af',
                        'highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11',
                        '-ac', '1', '-ar', '16000', tmp], capture_output=True, timeout=900)
    return tmp if r.returncode == 0 and os.path.getsize(tmp) > 1024 else None

print(f'model={MODEL}  vad threshold={VAD_THRESHOLD} min_silence={VAD_MIN_SILENCE}ms '
      f'max_speech={VAD_MAX_SPEECH}s')
model = WhisperModel(MODEL, device='cpu', compute_type='int8', download_root=CACHE)

for path in args:
    name = os.path.basename(path)
    print('\n' + '=' * 78)
    print(name)
    print('=' * 78)

    st = ffprobe_audio(path)
    if not st:
        print('  audio stream        : NONE — genuinely silent to any ASR')
        continue
    print(f"  audio stream        : {st.get('codec_name')} {st.get('sample_rate')}Hz {st.get('channels')}ch")

    mean, mx, silent = levels(path)
    wav = prepared_audio(path)
    if not wav:
        print('  PREPROCESSING FAILED — the transcriber would fall back to raw audio')
        continue
    audio = decode_audio(wav, sampling_rate=16000)
    dur = len(audio) / 16000
    print(f'  duration            : {dur:.1f}s')
    print(f'  measured level      : mean {mean} dBFS   peak {mx} dBFS')
    print(f'  ffmpeg silence      : {silent:.1f}s ({100*silent/dur:.0f}% below -40dB for >=0.5s)')

    vo = VadOptions(threshold=VAD_THRESHOLD, min_silence_duration_ms=VAD_MIN_SILENCE,
                    max_speech_duration_s=VAD_MAX_SPEECH)
    ts = get_speech_timestamps(audio, vo)
    regions = [((t['end'] - t['start']) / 16000) for t in ts]
    speech = sum(regions)
    print(f'  VAD speech          : {speech:.1f}s in {len(regions)} region(s) '
          f'({100*speech/dur:.0f}% of clip)')
    if regions:
        regions_sorted = sorted(regions, reverse=True)
        print(f'  VAD region lengths  : longest {regions_sorted[0]:.1f}s  '
              f'median {regions_sorted[len(regions_sorted)//2]:.1f}s  '
              f'>30s: {sum(1 for r in regions if r > 30)}  >60s: {sum(1 for r in regions if r > 60)}')

    segs, info = model.transcribe(
        wav, language='en', beam_size=5, vad_filter=True,
        vad_parameters=dict(threshold=VAD_THRESHOLD, min_silence_duration_ms=VAD_MIN_SILENCE,
                            max_speech_duration_s=VAD_MAX_SPEECH),
        condition_on_previous_text=False)
    segs = list(segs)
    texts = [s.text.strip() for s in segs]
    counts = collections.Counter(texts)
    repeated = sum(c for t, c in counts.items() if c > 1)
    longest = max([(s.end - s.start) for s in segs], default=0)
    maxrun = 1; run = 1
    for i in range(1, len(texts)):
        if texts[i] == texts[i-1]: run += 1; maxrun = max(maxrun, run)
        else: run = 1

    print(f'  ASR segments        : {len(segs)}')
    print(f'  repeated-text ratio : {repeated}/{len(texts)} '
          f'({100*repeated/len(texts) if texts else 0:.0f}%)  longest identical run {maxrun}')
    print(f'  longest ASR segment : {longest:.1f}s ({100*longest/dur:.0f}% of the clip)')
    if segs:
        nsp = [s.no_speech_prob for s in segs]
        alp = [s.avg_logprob for s in segs]
        print(f'  no_speech_prob      : min {min(nsp):.2f}  median {sorted(nsp)[len(nsp)//2]:.2f}  max {max(nsp):.2f}')
        print(f'  avg_logprob         : min {min(alp):.2f}  median {sorted(alp)[len(alp)//2]:.2f}  max {max(alp):.2f}')
        worst = sorted(segs, key=lambda s: s.avg_logprob)[:3]
        for s in worst:
            print(f'      low-confidence  : [{s.start:6.1f}-{s.end:6.1f}] logprob {s.avg_logprob:.2f} '
                  f'nospeech {s.no_speech_prob:.2f}  "{s.text.strip()[:52]}"')
    os.unlink(wav)
