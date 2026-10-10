#!/bin/sh
# BUILD.sh — rebuild hvl2wav from bundled source. Requires only gcc+make.
set -e
cd "$(dirname "$0")"
rm -rf build && mkdir build && cp src/* build/ && cd build
make -f makefile
cp hvl2wav ..
cd .. && rm -rf build
echo "built: ./hvl2wav"
