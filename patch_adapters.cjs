const fs = require('fs');
const files = [
  'src/core/tools/adapters/generic.ts',
  'src/core/tools/adapters/ffmpeg.ts',
  'src/core/tools/adapters/blender.ts',
  'src/core/tools/adapters/comfyui.ts'
];

for (const f of files) {
  if (!fs.existsSync(f)) continue;
  let content = fs.readFileSync(f, 'utf8');
  content = content.replace(/'INSTALLED'/g, "'AVAILABLE'");
  content = content.replace(/'NOT_CHECKED'/g, "'UNAVAILABLE'");
  content = content.replace(/'CONNECTED'/g, "'AVAILABLE'");
  fs.writeFileSync(f, content);
}
console.log('Patched adapters');
