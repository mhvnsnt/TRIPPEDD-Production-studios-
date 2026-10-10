/* mod2wav.c — minimal DUMB-based tracker-module renderer (no argtable dep).
 * Usage: mod2wav <input.mod> <output.wav> [seconds]
 * Renders stereo 16-bit 44.1kHz PCM via DUMB and writes a valid WAV.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <dumb.h>

static void write_u32le(FILE *f, uint32_t v) {
    uint8_t b[4] = {v & 255, (v >> 8) & 255, (v >> 16) & 255, (v >> 24) & 255};
    fwrite(b, 1, 4, f);
}
static void write_u16le(FILE *f, uint16_t v) {
    uint8_t b[2] = {v & 255, (v >> 8) & 255};
    fwrite(b, 1, 2, f);
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "usage: %s <input.mod> <output.wav> [seconds]\n", argv[0]);
        return 2;
    }
    double seconds = argc > 3 ? atof(argv[3]) : 12.0;
    const int freq = 44100, nch = 2, bits = 16;

    dumb_register_stdfiles(); /* DUMB is filesystem-agnostic: register stdio */

    DUH *duh = dumb_load_any(argv[1], 0, 0);
    if (!duh) { fprintf(stderr, "dumb_load_any failed for %s\n", argv[1]); return 1; }

    DUH_SIGRENDERER *sr = duh_start_sigrenderer(duh, 0, nch, 0);
    if (!sr) { fprintf(stderr, "sigrenderer failed\n"); unload_duh(duh); return 1; }
    DUMB_IT_SIGRENDERER *itsr = duh_get_it_sigrenderer(sr);
    if (itsr) { /* IT-family: stop at song end instead of looping forever */
        dumb_it_set_loop_callback(itsr, &dumb_it_callback_terminate, NULL);
        dumb_it_set_xm_speed_zero_callback(itsr, &dumb_it_callback_terminate, NULL);
        dumb_it_set_resampling_quality(itsr, DUMB_RQ_CUBIC);
    }

    FILE *f = fopen(argv[2], "wb");
    if (!f) { perror("fopen"); duh_end_sigrenderer(sr); unload_duh(duh); return 1; }

    /* WAV header with placeholder sizes */
    fwrite("RIFF", 1, 4, f); write_u32le(f, 0);
    fwrite("WAVEfmt ", 1, 8, f); write_u32le(f, 16);
    write_u16le(f, 1); write_u16le(f, nch); write_u32le(f, freq);
    write_u32le(f, freq * nch * bits / 8); write_u16le(f, nch * bits / 8); write_u16le(f, bits);
    fwrite("data", 1, 4, f); write_u32le(f, 0);
    long data_start = ftell(f);

    float delta = 65536.0f / freq;
    long target = (long)(seconds * freq);
    long done = 0;
    char buf[8192];
    sample_t **sig = NULL; long sigsize = 0;
    while (done < target) {
        long want = target - done > 2048 ? 2048 : target - done;
        long got = duh_render_int(sr, &sig, &sigsize, bits, 0, 1.0f, delta, want, buf);
        if (got <= 0) break;
        fwrite(buf, 1, (size_t)got * nch * bits / 8, f);
        done += got;
    }
    if (sig) destroy_sample_buffer(sig);

    long data_end = ftell(f);
    uint32_t data_bytes = (uint32_t)(data_end - data_start);
    fseek(f, 4, SEEK_SET); write_u32le(f, 36 + data_bytes);
    fseek(f, data_start - 4, SEEK_SET); write_u32le(f, data_bytes);
    fclose(f);

    printf("rendered %.2f s (%ld samples, %u data bytes) -> %s\n",
           done / (double)freq, done, data_bytes, argv[2]);
    duh_end_sigrenderer(sr);
    unload_duh(duh);
    dumb_exit();
    return 0;
}
