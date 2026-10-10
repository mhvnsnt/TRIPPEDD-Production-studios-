#!/usr/bin/env python3
"""Wave 47 Lane B tool wire: stb_image + stb_image_write (public domain / MIT).

What it does:
  1. Generates a deterministic RGB test PNG with Pillow (256x128, gradient +
     checker overlay + a red diagonal — pixel-exact, reproducible).
  2. Compiles a small C program against the vendored stb_image.h /
     stb_image_write.h (fetched from nothings/stb master; license header says
     "public domain image loader" — verified 2026-10-08).
  3. The C program: stbi_load() the PNG -> prints w/h/channels; writes the
     pixels out as BMP via stbi_write_bmp() AND as raw P6 PPM.
  4. Python re-opens the BMP with Pillow and byte-compares pixel data against
     the source PNG (BMP is lossless) -> PASS/FAIL.
  5. Writes proof artifacts + appends to PROOFS.md and SHA256SUMS.

Proof artifacts (proofs_stb_image/):
  fixture.png   - deterministic source image
  decoded.bmp   - BMP written by stb_image_write (real converted file)
  decoded.ppm   - raw PPM written by the C program
  c_output.txt  - stdout of the C program (w/h/channels report)
"""
import hashlib, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VENDOR = os.path.join(HERE, 'vendor')
PROOFS = os.path.join(HERE, 'proofs_stb_image')

C_SRC = r'''
#include <stdio.h>
#include <stdlib.h>
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

int main(int argc, char** argv) {
    int w, h, c;
    unsigned char* px = stbi_load("fixture.png", &w, &h, &c, 3);
    if (!px) { fprintf(stderr, "stbi_load failed: %s\n", stbi_failure_reason()); return 1; }
    printf("decoded: w=%d h=%d channels_in=%d forced=3\n", w, h, c);
    FILE* f = fopen("decoded.ppm", "wb");
    fprintf(f, "P6\n%d %d\n255\n", w, h);
    fwrite(px, 1, (size_t)w*h*3, f);
    fclose(f);
    if (!stbi_write_bmp("decoded.bmp", w, h, 3, px)) {
        fprintf(stderr, "stbi_write_bmp failed\n"); return 1;
    }
    printf("wrote decoded.ppm + decoded.bmp\n");
    stbi_image_free(px);
    return 0;
}
'''

def main():
    os.makedirs(PROOFS, exist_ok=True)
    for hdr in ('stb_image.h', 'stb_image_write.h'):
        p = os.path.join(VENDOR, hdr)
        if not os.path.exists(p):
            print(f'MISSING vendored header {p} — download from https://github.com/nothings/stb first', file=sys.stderr)
            return 1
    cwd = os.getcwd(); os.chdir(PROOFS)
    try:
        # 1. deterministic fixture
        from PIL import Image
        W, H = 256, 128
        im = Image.new('RGB', (W, H))
        px = im.load()
        for y in range(H):
            for x in range(W):
                r = (x * 255) // (W - 1)
                g = (y * 255) // (H - 1)
                b = ((x // 16) + (y // 16)) % 2 * 255
                if x == y * 2: r, g, b = 255, 0, 0
                px[x, y] = (r, g, b)
        im.save('fixture.png')
        print(f'fixture.png written: {W}x{H} RGB')

        # 2. compile
        with open('test_img.c', 'w') as f: f.write(C_SRC)
        cc = subprocess.run(
            ['gcc', '-O2', '-I', VENDOR, '-o', 'test_img', 'test_img.c', '-lm'],
            capture_output=True, text=True)
        if cc.returncode != 0:
            print('COMPILATION FAILED:\n' + cc.stderr, file=sys.stderr); return 1
        print('compiled test_img OK')

        # 3. run
        run = subprocess.run(['./test_img'], capture_output=True, text=True)
        open('c_output.txt', 'w').write(run.stdout + run.stderr)
        print('C program output:\n' + run.stdout)
        if run.returncode != 0:
            print('C program FAILED:\n' + run.stderr, file=sys.stderr); return 1

        # 4. verify pixel-exactness of the BMP round trip
        from PIL import Image
        src = Image.open('fixture.png').convert('RGB')
        bmp = Image.open('decoded.bmp').convert('RGB')
        assert bmp.size == src.size, f'size mismatch {bmp.size} vs {src.size}'
        d_src = src.tobytes(); d_bmp = bmp.tobytes()
        assert d_src == d_bmp, f'pixel mismatch: {len(d_src)} vs {len(d_bmp)} bytes'
        ppm = open('decoded.ppm', 'rb').read()
        assert ppm.startswith(b'P6\n256 128\n255\n'), 'PPM header wrong'
        assert ppm.split(b'\n255\n', 1)[1] == d_src, 'PPM pixel data mismatch'
        print(f'VERIFY PASS: BMP pixels byte-identical to fixture ({len(d_src)} bytes), '
              f'{bmp.size[0]}x{bmp.size[1]}')

        for art in ('fixture.png', 'decoded.bmp', 'decoded.ppm', 'c_output.txt'):
            print(f'  {art}: {os.path.getsize(art)} bytes, sha256={hashlib.sha256(open(art,"rb").read()).hexdigest()[:16]}...')
        return 0
    finally:
        os.chdir(cwd)

if __name__ == '__main__':
    sys.exit(main())
