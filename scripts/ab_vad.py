"""A/B the VAD setting that was changed, on the clips that broke.

Two failures to separate, both caused by the same knob if the hypothesis holds:
  LOOP    tiny noise regions admitted as speech, each decoded as the same short
          phrase. Lowering the VAD threshold is what admits them.
  SILENT  no speech regions found at all, so the decoder never sees the audio.
          If the speech is really there, disabling VAD will find it.

Prints the measured numbers per configuration. No configuration is applied.
"""
import sys, os, collections
from faster_whisper import WhisperModel, decode_audio
from faster_whisper.vad import VadOptions, get_speech_timestamps
import subprocess, tempfile

CACHE = os.path.join(os.getcwd(), '.trippedd_models')
MODEL = os.environ.get('AB_MODEL', 'small')

def prep(path):
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False).name
    subprocess.run(['ffmpeg','-y','-v','error','-i',path,'-af',
                    'highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-ac','1','-ar','16000',tmp], capture_output=True, timeout=900)
    return tmp

model = WhisperModel(MODEL, device='cpu', compute_type='int8', download_root=CACHE)
print(f'model={MODEL}\n')

CONFIGS = [
    ('vad 0.35 (CURRENT)', dict(vad_filter=True, vad_parameters=dict(threshold=0.35, min_silence_duration_ms=700))),
    ('vad 0.50 (library default)', dict(vad_filter=True, vad_parameters=dict(threshold=0.5, min_silence_duration_ms=2000))),
    ('vad 0.60 (strict)', dict(vad_filter=True, vad_parameters=dict(threshold=0.6, min_silence_duration_ms=2000))),
    ('NO VAD', dict(vad_filter=False)),
]

for path in sys.argv[1:]:
    name = os.path.basename(path)
    wav = prep(path)
    audio = decode_audio(wav, sampling_rate=16000)
    dur = len(audio)/16000
    print('='*80); print(f'{name}   {dur:.1f}s'); print('='*80)
    for label, cfg in CONFIGS:
        vp = cfg.get('vad_parameters')
        if cfg.get('vad_filter') and vp:
            ts = get_speech_timestamps(audio, VadOptions(**vp))
            speech = sum((t['end']-t['start'])/16000 for t in ts)
            vadinfo = f'{speech:5.1f}s speech in {len(ts):3d} region(s) ({100*speech/dur:3.0f}%)'
        else:
            vadinfo = 'whole clip decoded          '
        segs = list(model.transcribe(wav, language='en', beam_size=5,
                                     condition_on_previous_text=False, **cfg)[0])
        texts = [s.text.strip() for s in segs]
        c = collections.Counter(texts)
        rep = sum(v for k, v in c.items() if v > 1)
        run = 1; mx = 1
        for i in range(1, len(texts)):
            if texts[i] == texts[i-1]: run += 1; mx = max(mx, run)
            else: run = 1
        longest = max([(s.end-s.start) for s in segs], default=0)
        print(f'  {label:28s} {vadinfo}  segs {len(segs):3d}  '
              f'repeat {rep:3d}/{len(texts):3d}  run {mx:2d}  longestSeg {longest:6.1f}s')
        if texts:
            print(f'      first: "{texts[0][:64]}"')
            uniq = [t for t, n in c.most_common(2)]
            if mx >= 3: print(f'      LOOPED TEXT: "{uniq[0][:48]}" x{c[uniq[0]]}')
    os.unlink(wav)
    print()
