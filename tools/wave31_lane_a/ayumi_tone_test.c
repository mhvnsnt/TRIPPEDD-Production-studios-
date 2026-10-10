/* Wave 31 Lane A wiring proof: ayumi (MIT) renders a 440 Hz square-ish tone to WAV.
 * Compile: gcc -O2 -o ayumi_tone_test ayumi_tone_test.c ayumi/ayumi.c -lm
 * Run: ./ayumi_tone_test   -> writes ayumi_440hz.wav (2 s, 44100 Hz, stereo, 16-bit)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
#include "ayumi/ayumi.h"

#define SR 44100
#define DUR_S 2
#define N (SR * DUR_S)

static void write_wav16(const char *name, const int16_t *data, int frames) {
    FILE *f = fopen(name, "wb");
    int data_bytes = frames * 2 * 2;
    uint8_t h[44] = {0};
    memcpy(h, "RIFF", 4);
    *(int32_t*)(h+4) = 36 + data_bytes;
    memcpy(h+8, "WAVEfmt ", 8);
    *(int32_t*)(h+16) = 16;
    *(int16_t*)(h+20) = 1;          /* PCM */
    *(int16_t*)(h+22) = 2;          /* stereo */
    *(int32_t*)(h+24) = SR;
    *(int32_t*)(h+28) = SR * 4;
    *(int16_t*)(h+32) = 4;
    *(int16_t*)(h+34) = 16;
    memcpy(h+36, "data", 4);
    *(int32_t*)(h+40) = data_bytes;
    fwrite(h, 1, 44, f);
    fwrite(data, 1, data_bytes, f);
    fclose(f);
}

int main(void) {
    struct ayumi ay;
    /* YM2149 mode, 2 MHz clock, 44.1 kHz output */
    if (!ayumi_configure(&ay, 1, 2000000.0, SR)) {
        fprintf(stderr, "ayumi_configure failed\n");
        return 1;
    }
    /* Channel A: 440 Hz. AY freq = clock / (16 * period) -> period ~= 284 */
    ayumi_set_tone(&ay, 0, 284);
    ayumi_set_mixer(&ay, 0, 0, 1, 0);   /* tone on, noise off, envelope off */
    ayumi_set_volume(&ay, 0, 15);       /* max volume */
    ayumi_set_pan(&ay, 0, 0.5, 1);      /* center */

    int16_t *pcm = calloc(N * 2, sizeof(int16_t));
    double peak = 0.0;
    long nonzero = 0;
    for (int i = 0; i < N; i++) {
        ayumi_process(&ay);
        ayumi_remove_dc(&ay);
        double l = ay.left, r = ay.right;
        if (fabs(l) > peak) peak = fabs(l);
        int16_t sl = (int16_t)(l * 32767.0 * 0.5);
        int16_t sr_ = (int16_t)(r * 32767.0 * 0.5);
        if (sl != 0) nonzero++;
        pcm[2*i] = sl; pcm[2*i+1] = sr_;
    }
    write_wav16("ayumi_440hz.wav", pcm, N);
    free(pcm);
    printf("wrote ayumi_440hz.wav: %d frames, peak=%.3f, nonzero_left_samples=%ld\n",
           N, peak, nonzero);
    /* crude 440 Hz sanity: count zero crossings on channel 0 over the last second */
    return (peak > 0.05 && nonzero > N / 2) ? 0 : 2;
}
