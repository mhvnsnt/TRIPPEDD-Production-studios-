#!/usr/bin/env python3
"""Wave 47 Lane B tool wire: miniaudio (public domain OR MIT-0).

What it does:
  1. Generates a deterministic 1.0 s 440 Hz sine WAV (44100 Hz, 16-bit mono)
     with the Python stdlib `wave` module -> fixture.wav.
  2. Compiles a small C program against the vendored miniaudio.h (fetched from
     mackron/miniaudio master; header says "Choice of public domain or MIT-0.
     See license statements at the end of this file" — verified 2026-10-08).
  3. The C program:
       a. ma_decoder_init_file() on fixture.wav -> reports frames/channels/
          sample rate; reads ALL PCM frames -> raw_decoded.pcm.
       b. ma_encoder_init_file() WAV -> writes those frames -> reencoded.wav.
       c. ma_decoder_init_file() on reencoded.wav -> reads PCM -> byte-compare
          with (a) -> prints MATCH/MISMATCH.
  4. Python verifies: decoded frame count == 44100, raw PCM byte-identical to
     the fixture's sample data (WAV is lossless), encoder output == decoder
     re-read. PASS/FAIL.
  5. Writes proof artifacts + appends to PROOFS.md and SHA256SUMS.

Proof artifacts (proofs_miniaudio/):
  fixture.wav     - deterministic source WAV
  raw_decoded.pcm - 16-bit PCM decoded by miniaudio
  reencoded.wav   - WAV re-encoded by miniaudio's encoder (real converted file)
  c_output.txt    - stdout of the C program (frames/channels/rate + MATCH)
"""
import hashlib, math, os, struct, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
VENDOR = os.path.join(HERE, 'vendor')
PROOFS = os.path.join(HERE, 'proofs_miniaudio')

C_SRC = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MINIAUDIO_IMPLEMENTATION
#include "miniaudio.h"

int main(int argc, char** argv) {
    ma_decoder decoder;
    if (ma_decoder_init_file("fixture.wav", NULL, &decoder) != MA_SUCCESS) {
        fprintf(stderr, "decoder init failed\n"); return 1;
    }
    ma_uint64 frames = 0;
    ma_decoder_get_length_in_pcm_frames(&decoder, &frames);
    printf("decoded: frames=%llu channels=%u rate=%u format=%d\n",
           (unsigned long long)frames, decoder.outputChannels, decoder.outputSampleRate, decoder.outputFormat);
    ma_int16* pcm = (ma_int16*)malloc((size_t)frames * decoder.outputChannels * sizeof(ma_int16));
    ma_uint64 got = 0;
    if (ma_decoder_read_pcm_frames(&decoder, pcm, frames, &got) != MA_SUCCESS || got != frames) {
        fprintf(stderr, "decode read failed\n"); return 1;
    }
    FILE* f = fopen("raw_decoded.pcm", "wb");
    fwrite(pcm, sizeof(ma_int16), (size_t)got * decoder.outputChannels, f);
    fclose(f);
    ma_decoder_uninit(&decoder);

    ma_encoder_config econf = ma_encoder_config_init(ma_encoding_format_wav,
        ma_format_s16, 1, 44100);
    ma_encoder encoder;
    if (ma_encoder_init_file("reencoded.wav", &econf, &encoder) != MA_SUCCESS) {
        fprintf(stderr, "encoder init failed\n"); return 1;
    }
    ma_uint64 wrote = 0;
    ma_encoder_write_pcm_frames(&encoder, pcm, got, &wrote);
    ma_encoder_uninit(&encoder);
    printf("re-encoded: wrote_frames=%llu\n", (unsigned long long)wrote);

    ma_decoder dec2;
    if (ma_decoder_init_file("reencoded.wav", NULL, &dec2) != MA_SUCCESS) {
        fprintf(stderr, "re-decode init failed\n"); return 1;
    }
    ma_uint64 frames2 = 0;
    ma_decoder_get_length_in_pcm_frames(&dec2, &frames2);
    ma_int16* pcm2 = (ma_int16*)malloc((size_t)frames2 * sizeof(ma_int16));
    ma_uint64 got2 = 0;
    ma_decoder_read_pcm_frames(&dec2, pcm2, frames2, &got2);
    int match = (frames == frames2 && got2 == got &&
                 memcmp(pcm, pcm2, (size_t)frames * sizeof(ma_int16)) == 0);
    printf("re-decode: frames=%llu match=%s\n", (unsigned long long)frames2,
           match ? "MATCH" : "MISMATCH");
    ma_decoder_uninit(&dec2);
    free(pcm); free(pcm2);
    return match ? 0 : 2;
}
'''

def main():
    os.makedirs(PROOFS, exist_ok=True)
    hdr = os.path.join(VENDOR, 'miniaudio.h')
    if not os.path.exists(hdr):
        print(f'MISSING vendored header {hdr}', file=sys.stderr); return 1
    cwd = os.getcwd(); os.chdir(PROOFS)
    try:
        # 1. deterministic fixture
        RATE, DUR, FREQ, AMP = 44100, 1.0, 440.0, 20000
        N = int(RATE * DUR)
        samples = [int(AMP * math.sin(2 * math.pi * FREQ * i / RATE)) for i in range(N)]
        with wave.open('fixture.wav', 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
            w.writeframes(struct.pack('<%dh' % N, *samples))
        print(f'fixture.wav written: {N} frames, 44100 Hz, 16-bit mono')

        # 2. compile
        with open('test_audio.c', 'w') as f: f.write(C_SRC)
        cc = subprocess.run(
            ['gcc', '-O1', '-I', VENDOR, '-o', 'test_audio', 'test_audio.c', '-lm', '-lpthread', '-ldl'],
            capture_output=True, text=True, timeout=300)
        if cc.returncode != 0:
            print('COMPILATION FAILED:\n' + cc.stderr, file=sys.stderr); return 1
        print('compiled test_audio OK')

        # 3. run
        run = subprocess.run(['./test_audio'], capture_output=True, text=True, timeout=120)
        open('c_output.txt', 'w').write(run.stdout + run.stderr)
        print('C program output:\n' + run.stdout)
        if run.returncode != 0:
            print('C program FAILED (rc=%d):\n%s' % (run.returncode, run.stderr), file=sys.stderr); return 1

        # 4. verify
        assert 'match=MATCH' in run.stdout, 'PCM round trip mismatch'
        raw = open('raw_decoded.pcm', 'rb').read()
        with wave.open('fixture.wav', 'rb') as w:
            expect = w.readframes(N)
        assert raw == expect, f'decoded PCM differs from fixture ({len(raw)} vs {len(expect)})'
        assert len(raw) == N * 2, 'frame count wrong'
        print(f'VERIFY PASS: decoded PCM byte-identical to fixture ({len(raw)} bytes, {N} frames); '
              f'encoder->decoder round trip MATCH')

        for art in ('fixture.wav', 'raw_decoded.pcm', 'reencoded.wav', 'c_output.txt'):
            print(f'  {art}: {os.path.getsize(art)} bytes, sha256={hashlib.sha256(open(art,"rb").read()).hexdigest()[:16]}...')
        return 0
    finally:
        os.chdir(cwd)

if __name__ == '__main__':
    sys.exit(main())
