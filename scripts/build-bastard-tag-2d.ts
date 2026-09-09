#!/usr/bin/env bun
import { mkdir, rm, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { spawnSync } from "node:child_process";

const FPS = 24;
const WIDTH = 1920;
const HEIGHT = 1080;
const DURATION = 6;
const FRAMES = FPS * DURATION;
const ROOT = "production/EP01/generated/comic";
const SVG = join(ROOT, "bannon-the-bastard-terminal.svg");
const PNG = join(ROOT, "bannon-the-bastard-terminal.png");
const OUT = join(ROOT, "ep01_bastard_tag.mp4");

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${WIDTH}" height="${HEIGHT}" viewBox="0 0 ${WIDTH} ${HEIGHT}">
<defs>
<radialGradient id="bg" cx="50%" cy="48%" r="75%"><stop offset="0" stop-color="#30313a"/><stop offset=".45" stop-color="#11131a"/><stop offset="1" stop-color="#020307"/></radialGradient>
<linearGradient id="red" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff3b30"/><stop offset=".55" stop-color="#a50000"/><stop offset="1" stop-color="#250000"/></linearGradient>
<pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r="2.1" fill="#fff" opacity=".16"/></pattern>
</defs>
<rect width="1920" height="1080" fill="url(#bg)"/>
<path d="M0 840 L420 690 L770 800 L1140 620 L1540 770 L1920 610 L1920 1080 L0 1080Z" fill="#05060a"/>
<path d="M0 0 L420 0 L250 1080 L0 1080Z" fill="#080a10"/><path d="M1920 0 L1510 0 L1680 1080 L1920 1080Z" fill="#090a0f"/>
<rect width="1920" height="1080" fill="url(#dots)"/>
<path d="M1480 0 L1385 210 L1450 190 L1350 430 L1485 275 L1425 290 L1535 90Z" fill="#e8f4ff" opacity=".9"/>
<path d="M45 45 H1875 V1035 H45 Z" fill="none" stroke="#f1f1eb" stroke-width="10"/><path d="M70 70 H1850 V1010 H70 Z" fill="none" stroke="#7d0a0a" stroke-width="4"/>
<ellipse cx="970" cy="1010" rx="530" ry="80" fill="#000" opacity=".8"/>
<!-- original 2D comic silhouette: hulking masked figure, hard inks and chiaroscuro -->
<path d="M520 1010 C540 820 585 665 700 550 C755 495 800 420 835 315 C865 225 940 170 1020 190 C1110 215 1160 290 1165 390 C1170 470 1215 515 1295 575 C1420 670 1480 825 1510 1010 Z" fill="#030405" stroke="#e7e7e1" stroke-width="12"/>
<path d="M650 720 C690 570 770 500 850 470 L875 700 L790 905 L625 945Z" fill="#1d2027" stroke="#050505" stroke-width="16"/>
<path d="M1290 720 C1250 570 1170 500 1090 470 L1065 700 L1150 905 L1315 945Z" fill="#171920" stroke="#050505" stroke-width="16"/>
<path d="M845 500 C900 455 1050 455 1105 500 L1070 760 L960 835 L850 760Z" fill="#242730" stroke="#050505" stroke-width="18"/>
<path d="M835 260 C855 190 940 150 1010 175 C1085 202 1125 270 1105 350 L1060 445 L960 485 L865 430 L820 350Z" fill="#15171d" stroke="#f0f0e8" stroke-width="14"/>
<path d="M850 315 L920 292 L965 315 L1030 290 L1090 318 L1055 350 L1010 338 L965 355 L910 340 L870 360Z" fill="#050507"/>
<path d="M900 240 L1015 220 L1080 260" fill="none" stroke="#aeb1b8" stroke-width="16"/><path d="M925 380 L1015 390 L1040 370" fill="none" stroke="#c5c6c8" stroke-width="11"/><path d="M950 390 L990 410 L1030 388" fill="none" stroke="#650000" stroke-width="8"/>
<path d="M700 545 C625 520 555 570 500 650 L390 835 L505 900 L650 735 L780 650Z" fill="#101217" stroke="#eee" stroke-width="14"/>
<path d="M1220 545 C1295 520 1365 570 1420 650 L1530 835 L1415 900 L1270 735 L1140 650Z" fill="#101217" stroke="#eee" stroke-width="14"/>
<path d="M405 830 L330 900 L395 960 L505 900" fill="#1d2027" stroke="#eee" stroke-width="12"/><path d="M1515 830 L1590 900 L1525 960 L1415 900" fill="#1d2027" stroke="#eee" stroke-width="12"/>
<path d="M515 825 L630 690 M625 690 L720 580 M1320 690 L1410 825 M1200 560 L1290 650" stroke="url(#red)" stroke-width="30" stroke-linecap="round"/>
<g stroke="#d7d7d0" stroke-width="5" opacity=".35"><path d="M650 620 l170 -90 M625 660 l190 -95 M610 700 l190 -95"/><path d="M1270 620 l-170 -90 M1295 660 l-190 -95 M1310 700 l-190 -95"/><path d="M760 830 l170 -120 M790 865 l160 -115 M1160 830 l-170 -120 M1130 865 l-160 -115"/></g>
<g stroke="#8bb7d7" stroke-width="5" opacity=".42"><path d="M180 180 L95 430 M290 120 L205 370 M410 210 L330 455 M530 95 L450 345 M620 150 L540 400 M1390 120 L1310 370 M1510 190 L1430 440 M1650 100 L1570 350 M1780 170 L1700 420 M1860 300 L1780 550"/></g>
<path d="M95 850 L720 850 L675 1000 L55 1000Z" fill="#07080c" stroke="#f0f0e8" stroke-width="7"/>
<text x="105" y="915" fill="#f2f1e9" font-family="DejaVu Sans, sans-serif" font-size="30" font-weight="700" letter-spacing="8">FIRST APPEARANCE</text>
<text x="100" y="975" fill="#e00000" font-family="DejaVu Sans, sans-serif" font-size="72" font-weight="900" letter-spacing="4">BANNON // THE BASTARD</text>
<text x="1540" y="930" fill="#f2f1e9" font-family="DejaVu Sans, sans-serif" font-size="42" font-weight="900" text-anchor="middle">TO BE</text><text x="1540" y="985" fill="#e00000" font-family="DejaVu Sans, sans-serif" font-size="58" font-weight="900" text-anchor="middle">CØNTINUED</text>
</svg>`;

await mkdir(ROOT, { recursive: true });
await writeFile(SVG, svg, "utf8");

const rasterizer = spawnSync("bash", ["-lc", "command -v magick || command -v convert"], { encoding: "utf8" });
const rasterizerPath = rasterizer.stdout.trim();
if (rasterizer.status !== 0 || !rasterizerPath) throw new Error("ImageMagick rasterizer unavailable: expected magick or convert");
const raster = spawnSync(rasterizerPath, [SVG, PNG], { stdio: "inherit" });
if (raster.status !== 0) throw new Error(`ImageMagick rasterization failed with status ${raster.status}`);

const ffmpeg = spawnSync("ffmpeg", ["-y", "-hide_banner", "-loglevel", "error", "-loop", "1", "-i", PNG, "-frames:v", String(FRAMES), "-vf", `zoompan=z='min(zoom+0.0006,1.04)':d=1:s=${WIDTH}x${HEIGHT}:fps=${FPS}`, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], { stdio: "inherit" });
if (ffmpeg.status !== 0) throw new Error(`FFmpeg failed with status ${ffmpeg.status}`);
const probe = spawnSync("ffprobe", ["-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,nb_read_frames", "-of", "json", OUT], { encoding: "utf8" });
if (probe.status !== 0) throw new Error("ffprobe validation failed");
const stream = JSON.parse(probe.stdout).streams?.[0];
if (!stream || stream.width !== WIDTH || stream.height !== HEIGHT || stream.nb_read_frames !== String(FRAMES)) throw new Error(`2D Bastard tag validation failed: ${probe.stdout}`);
await rm(PNG, { force: true });
console.log(JSON.stringify({ verified: true, mode: "2D_COMIC", character: "Bannon/The Bastard", fps: FPS, frames: FRAMES, width: WIDTH, height: HEIGHT, svg: SVG, mp4: OUT, rasterizer: rasterizerPath, timestamp: new Date().toISOString() }, null, 2));
