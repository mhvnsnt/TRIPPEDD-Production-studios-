### Open-source audio restoration & processing — Wave 22 (+16)

#### librosa ✅ commercial-safe
- **What:** Python audio-analysis library — feature extraction, beat tracking, spectrograms; the NumPy of music/audio research
- **URL:** https://github.com/librosa/librosa
- **License:** ✅ ISC (verified 2026-10-07: GitHub API spdx_id librosa/librosa)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** First import for any audio QA or analysis script (duration, silence detection, spectral checks on restorations). [Wave 22 Lane A]

#### torchaudio ✅ commercial-safe
- **What:** PyTorch's audio I/O and processing library — GPU-accelerated resampling, spectrograms, and audio models
- **URL:** https://github.com/pytorch/audio
- **License:** ✅ BSD-2-Clause (verified 2026-10-07: GitHub API spdx_id pytorch/audio)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Pairs with Demucs/Asteroid pipelines for GPU batch audio processing. [Wave 22 Lane A]

#### noisereduce ✅ commercial-safe
- **What:** Spectral-gating noise reduction in pure Python — clean hiss/hum from field recordings and digitized 78s with a few lines of code
- **URL:** https://github.com/timsainb/noisereduce
- **License:** ✅ MIT (verified 2026-10-07: LICENSE file in repo, master branch; PyPI also lists MIT)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The quick-win denoiser for archive audio — stationary-noise profile, no training, no GPU. [Wave 22 Lane A]

#### audiomentations ✅ commercial-safe
- **What:** Audio augmentation library — pitch shift, time stretch, noise/reverb injection for training robust audio models
- **URL:** https://github.com/iver56/audiomentations
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id iver56/audiomentations)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Useful for stress-testing restoration chains against degraded variants. [Wave 22 Lane A]

#### Demucs ✅ commercial-safe
- **What:** Meta's state-of-the-art music source separation — split stems (vocals/drums/bass/other) from mixed recordings; the open standard for stem extraction
- **URL:** https://github.com/facebookresearch/demucs
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id facebookresearch/demucs)
- **Free tier:** N/A (pip; GPU recommended)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Separate-then-remix workflow: isolate dialogue/music from noisy archive recordings, or pull acapellas for scoring. [Wave 22 Lane A]

#### Spleeter ✅ commercial-safe
- **What:** Deezer's fast source-separation engine (2/4/5 stems) — lighter and faster than Demucs, pretrained models included
- **URL:** https://github.com/deezer/spleeter
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id deezer/spleeter)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Faster CPU-friendly alternative to Demucs when quality bar allows. [Wave 22 Lane A]

#### Open-Unmix ✅ commercial-safe
- **What:** SigSep's open music-separation reference (PyTorch) — the reproducible baseline behind the SiSEC separation campaigns
- **URL:** https://github.com/sigsep/open-unmix-pytorch
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id sigsep/open-unmix-pytorch)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Research baseline; prefer Demucs/Spleeter for production separation. [Wave 22 Lane A]

#### Asteroid ✅ commercial-safe
- **What:** PyTorch audio source-separation toolkit — recipes for speech/music separation, enhancement, and dereverberation
- **URL:** https://github.com/asteroid-team/asteroid
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id asteroid-team/asteroid)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Includes speech-enhancement recipes — the training/eval harness if we ever fine-tune a denoiser. [Wave 22 Lane A]

#### nussl ✅ commercial-safe
- **What:** Northwestern's audio source-separation library — modular separation/benchmarking with music and speech recipes
- **URL:** https://github.com/nussl/nussl
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id nussl/nussl)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strong evaluation tooling (BSS metrics) for comparing separation outputs objectively. [Wave 22 Lane A]



#### pyrubberband ✅ commercial-safe
- **What:** Python wrapper for Rubber Band time-stretching/pitch-shifting — the highest-quality open time-stretch, scriptable
- **URL:** https://github.com/bmcfee/pyrubberband
- **License:** ✅ ISC (verified 2026-10-07: GitHub API spdx_id bmcfee/pyrubberband)
- **Free tier:** N/A (pip; needs rubberband binary)
- **Repo lane:** trippedd (audio)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Note: the Rubber Band library itself is GPL-2.0 (quarantine row) — the wrapper is ISC, but using it shells to the GPL binary; keep as a standalone tool step, never link the library into shipped code. [Wave 22 Lane A]

#### resampy ✅ commercial-safe
- **What:** Efficient sample-rate conversion (Kaiser-windowed sinc) — the resampling behind librosa; scriptable and dependency-light
- **URL:** https://github.com/bmcfee/resampy
- **License:** ✅ ISC (verified 2026-10-07: GitHub API spdx_id bmcfee/resampy)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (audio)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Standardize archive audio sample rates before any restoration chain. [Wave 22 Lane A]

#### RNNoise ✅ commercial-safe
- **What:** Xiph's RNN-based noise suppression — real-time speech denoising from a tiny neural model; the engine inside many denoisers
- **URL:** https://github.com/xiph/rnnoise
- **License:** ✅ BSD-3-Clause (verified 2026-10-07: GitHub API spdx_id xiph/rnnoise)
- **Free tier:** N/A (C; training in Torch)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Real-time capable — candidate for live dialogue cleanup, not just offline restoration. [Wave 22 Lane A]

#### DeepFilterNet ✅ commercial-safe
- **What:** Deep-learning noise reduction for full-band speech — real-time capable, beats classic spectral gating on non-stationary noise
- **URL:** https://github.com/Rikorose/DeepFilterNet
- **License:** ✅ MIT/Apache-2.0 dual (verified 2026-10-07: README license section — dual-licensed MIT or Apache-2.0)
- **Free tier:** N/A (Rust + PyTorch)
- **Repo lane:** trippedd (audio/restoration)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Step up from noisereduce when noise is non-stationary (crowds, wind, room tone shifts). [Wave 22 Lane A]

#### PaddleSpeech ✅ commercial-safe
- **What:** Baidu's all-in-one speech toolkit — ASR, TTS, text analysis, and audio classification; production-grade Chinese/English speech pipelines
- **URL:** https://github.com/PaddlePaddle/PaddleSpeech
- **License:** ✅ Apache-2.0 (verified 2026-10-07: GitHub API spdx_id PaddlePaddle/PaddleSpeech)
- **Free tier:** N/A
- **Repo lane:** trippedd (audio/speech)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Heaviest option here; reach for it when the pipeline needs ASR+TTS in one stack. [Wave 22 Lane A]

### PDF table & text extraction — Wave 22 (+4)

#### Camelot ✅ commercial-safe
- **What:** Python PDF table extraction — lattice/stream methods to pull tables out of digitized reports and catalogs as DataFrames
- **URL:** https://github.com/camelot-dev/camelot
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id camelot-dev/camelot)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (digitization/extraction)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pairs with OCRmyPDF output — extract tabular data from scanned library catalogs. [Wave 22 Lane A]

#### Tabula ✅ commercial-safe
- **What:** Java-based PDF table extractor with a simple UI — the journalist-standard tool for liberating tables from PDFs
- **URL:** https://github.com/tabulapdf/tabula
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id tabulapdf/tabula)
- **Free tier:** N/A
- **Repo lane:** trippedd (digitization/extraction)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** GUI route when table extraction needs a human to draw the selection boxes. [Wave 22 Lane A]

#### pdfplumber ✅ commercial-safe
- **What:** Python PDF text/table extraction with visual debugging — per-character positioning for precise text recovery from digitized PDFs
- **URL:** https://github.com/jsvine/pdfplumber
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id jsvine/pdfplumber)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (digitization/extraction)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Best-in-class for debugging extraction against the visual page — `.to_image()` overlays show exactly what was captured. [Wave 22 Lane A]

#### pdfminer.six ✅ commercial-safe
- **What:** Pure-Python PDF text extraction and layout analysis — the low-level engine behind many PDF-to-text pipelines
- **URL:** https://github.com/pdfminer/pdfminer.six
- **License:** ✅ MIT (verified 2026-10-07: GitHub API spdx_id pdfminer/pdfminer.six)
- **Free tier:** N/A (pip)
- **Repo lane:** trippedd (digitization/extraction)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Reach past pdfplumber when you need raw layout objects rather than convenience wrappers. [Wave 22 Lane A]
