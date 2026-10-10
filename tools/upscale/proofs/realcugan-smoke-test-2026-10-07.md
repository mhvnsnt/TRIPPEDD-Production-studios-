# Smoke-test log — realcugan-ncnn-vulkan (2026-10-07)

Tool: nihui realcugan-ncnn-vulkan 20220728 (ubuntu build), MIT
Vendored at: tools/upscale/realcugan-ncnn-vulkan/realcugan-ncnn-vulkan-20220728-ubuntu/
Includes: binary + LICENSE (MIT) + README.md + models-nose/models-pro/models-se

## What was proven
- Binary downloads, extracts, and EXECUTES on this VM: `./realcugan-ncnn-vulkan -h`
  prints full usage (options -i/-o/-n/-s/-t/-c/-m/-g/-j/-x/-f verified).
- Input JPEG decodes (reached encode stage on second attempt after path fix).

## What FAILED (environment limitation, not a tool defect)
- `vkCreateInstance failed -9` — this ncnn-vulkan build requires a Vulkan
  instance even in CPU mode (-g -1); this VM has no Vulkan device/driver.
- Inference therefore cannot complete here: "encode image ... failed",
  exit code 2. No output artifact was produced (nothing faked).
- First attempt also had a wrong relative input path (my error, fixed on retry).

## Verdict
NOT WIRED. Binary vendored + arg-parsing proven. Full inference needs a worker
with Vulkan (GPU box or lavapipe software Vulkan). Re-run on GPU hardware:
  ./realcugan-ncnn-vulkan -i in.jpg -o out.png -s 2 -n 0 -g 0 -t 400
Then promote the catalog entry to WIRED.
