# TRIPPEDD free/open-source production stack

The production stack is intentionally composed of tools that can run locally, in GitHub Actions, or in a browser/cloud worker without making a paid SaaS product a production dependency.

## Evidence + geometry

- **Blender** — headless scene generation, rigging, rendering, and byte-verifiable visual proof.
- **MediaPipe** — canonical face landmark reference and live landmark extraction.
- **ICT-FaceKit** — FACS-compatible donor geometry and expression basis.
- **Rigify** — Blender-native rig generation where appropriate.
- **trimesh** — mesh inspection, connected components, transforms, ray tests, and geometry measurements.
- **SciPy** — numerical fitting, optimization, interpolation, and registration primitives.
- **pycpd** — non-rigid/rigid point-set registration when correspondence is not already authoritative.
- **libigl** — robust mesh processing primitives; use as an optional adapter, never as an authority by itself.
- **Open3D** — point-cloud/mesh registration and ICP experiments; useful as a cross-check against the Blender/trimesh path.
- **OpenCV** — image registration, edge/contour processing, and deterministic image measurements.
- **scikit-image** — morphology, geometric transforms, segmentation helpers, and image-quality measurements.

## Media + transcription

- **FFmpeg / ffprobe** — canonical media inspection, transcoding, frame extraction, and byte-level metadata.
- **PySceneDetect** — shot/scene boundary detection; current upstream release is actively maintained.
- **Whisper-compatible open models** — transcript generation when a local model/runtime is available; unavailable states remain explicit.
- **Tesseract** — OCR for slate/text evidence, never as a replacement for visual QC.

## Character/asset support

- **MakeHuman / MPFB2** — open human base meshes and Blender integration for donor/reference workflows.
- **MeshLab** — manual/CLI mesh inspection and cleanup cross-checks.
- **NumPy** — deterministic numerical substrate used by the analysis layer.

## Integration rule

A tool enters the production authority only after:

1. its license/provenance is recorded;
2. its adapter has an explicit `AVAILABLE | UNAVAILABLE | FAILED` state;
3. a deterministic smoke test exists;
4. artifacts have byte hashes;
5. the tool cannot silently convert `UNKNOWN` into `PASS`;
6. visual claims are backed by actual rendered images/sequences.

Optional heavy dependencies should remain optional. The baseline runtime must continue to boot when GPU-only or large research packages are unavailable.
