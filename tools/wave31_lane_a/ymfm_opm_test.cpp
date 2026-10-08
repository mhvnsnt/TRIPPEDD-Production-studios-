//
// Wave 31 Lane A wiring proof: ymfm (BSD-3-Clause) YM2151/OPM core renders
// an FM patch to WAV. Compile with:
//   g++ --std=c++14 -Iymfm/src ymfm_opm_test.cpp ymfm/src/ymfm_misc.cpp \
//       ymfm/src/ymfm_opm.cpp -o ymfm_opm_test
// Run: ./ymfm_opm_test  -> writes ymfm_opm.wav (2 s, 44100 Hz, stereo, 16-bit)
//
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include "ymfm_opm.h"

class chip_wrapper : public ymfm::ymfm_interface {
public:
    chip_wrapper() : m_chip(*this) { m_chip.reset(); }
    void write(uint8_t reg, uint8_t data) { m_chip.write(0, reg); m_chip.write(1, data); }
    ymfm::ym2151 &chip() { return m_chip; }
private:
    ymfm::ym2151 m_chip;
};

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
    *(int16_t*)(h+20) = 1;
    *(int16_t*)(h+22) = 2;
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

int main() {
    chip_wrapper ym;
    const int ch = 0;
    // Channel setup: L+R on, FB=0, algorithm 7 (all 4 ops = carriers)
    ym.write(0x20 + ch, 0xC7);
    ym.write(0x28 + ch, 0x4A);   // KC: octave 4, note A (~440 Hz @ 3.58 MHz)
    ym.write(0x30 + ch, 0x00);   // KF = 0
    ym.write(0x38 + ch, 0x00);   // PMS/AMS = 0
    for (int op = 0; op < 4; op++) {
        int o = op * 8 + ch;
        ym.write(0x40 + o, 0x01);  // DT1=0, MUL=1
        ym.write(0x60 + o, 0x00);  // TL = 0 (loudest)
        ym.write(0x80 + o, 0x1F);  // KS=0, AR=31 (instant attack)
        ym.write(0xA0 + o, 0x00);  // AME=0, D1R=0 (no decay)
        ym.write(0xC0 + o, 0x00);  // DT2=0, D2R=0
        ym.write(0xE0 + o, 0xF0);  // D1L=15 (full sustain), RR=0
    }
    ym.write(0x08, 0x78 | ch);    // key on, all 4 slots, channel 0

    int16_t *pcm = (int16_t*)calloc(N * 2, sizeof(int16_t));
    ymfm::ym2151::output_data out;
    double peak = 0.0;
    long nonzero = 0;
    for (int i = 0; i < N; i++) {
        ym.chip().generate(&out, 1);
        // OPM output is ~13-bit; normalize
        double l = out.data[0] / 4096.0, r = out.data[1] / 4096.0;
        if (fabs(l) > peak) peak = fabs(l);
        int16_t sl = (int16_t)(l * 32767.0 * 0.08);
        int16_t srr = (int16_t)(r * 32767.0 * 0.08);
        if (sl != 0) nonzero++;
        pcm[2*i] = sl; pcm[2*i+1] = srr;
    }
    write_wav16("ymfm_opm.wav", pcm, N);
    free(pcm);
    printf("wrote ymfm_opm.wav: %d frames, peak=%.3f, nonzero=%ld\n", N, peak, nonzero);
    return (peak > 0.02 && nonzero > N / 2) ? 0 : 2;
}
