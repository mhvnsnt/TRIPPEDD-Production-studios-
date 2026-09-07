const fs = require('fs');

let tm = fs.readFileSync('src/server/toolManager.ts', 'utf8');
tm = tm.replace(/this\.createDef\('ffmpeg', 'FFmpeg', 'Media processing'\)/g, "this.createDef('ffmpeg', 'FFmpeg', 'Media processing', 'CLI')");
tm = tm.replace(/this\.createDef\('ffprobe', 'FFprobe', 'Media metadata'\)/g, "this.createDef('ffprobe', 'FFprobe', 'Media metadata', 'CLI')");
tm = tm.replace(/this\.createDef\('opencv', 'OpenCV', 'Computer Vision'\)/g, "this.createDef('opencv', 'OpenCV', 'Computer Vision', 'PYTHON')");
tm = tm.replace(/this\.createDef\('pyscenedetect', 'PySceneDetect', 'Scene detection'\)/g, "this.createDef('pyscenedetect', 'PySceneDetect', 'Scene detection', 'PYTHON')");
tm = tm.replace(/this\.createDef\('whisper', 'Whisper', 'Speech recognition'\)/g, "this.createDef('whisper', 'Whisper', 'Speech recognition', 'PYTHON')");
tm = tm.replace(/this\.createDef\('tesseract', 'Tesseract OCR', 'Optical Character Recognition'\)/g, "this.createDef('tesseract', 'Tesseract OCR', 'Optical Character Recognition', 'CLI')");
tm = tm.replace(/this\.createDef\('demucs', 'Demucs', 'Audio separation'\)/g, "this.createDef('demucs', 'Demucs', 'Audio separation', 'PYTHON')");
tm = tm.replace(/this\.createDef\('whisperx', 'WhisperX', 'Aligned Speech recognition'\)/g, "this.createDef('whisperx', 'WhisperX', 'Aligned Speech recognition', 'PYTHON')");
tm = tm.replace(/this\.createDef\('otio', 'OpenTimelineIO', 'Editorial interchange'\)/g, "this.createDef('otio', 'OpenTimelineIO', 'Editorial interchange', 'PYTHON')");
fs.writeFileSync('src/server/toolManager.ts', tm);
