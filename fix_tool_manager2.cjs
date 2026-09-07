const fs = require('fs');

let tm = fs.readFileSync('src/server/toolManager.ts', 'utf8');
tm = tm.replace(
  /this\.createDef\('demucs', 'Demucs', 'Audio source separation'\)/g,
  "this.createDef('demucs', 'Demucs', 'Audio source separation', 'PYTHON')"
);
tm = tm.replace(
  /this\.createDef\('ffmpeg', 'FFmpeg', 'Media manipulation'\)/g,
  "this.createDef('ffmpeg', 'FFmpeg', 'Media manipulation', 'CLI')"
);
fs.writeFileSync('src/server/toolManager.ts', tm);
