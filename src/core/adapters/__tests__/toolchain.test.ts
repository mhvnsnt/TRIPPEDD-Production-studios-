import { describe, it, expect, vi } from 'vitest';
import { FFprobeAdapter } from '../FFprobeAdapter';
import { PySceneDetectAdapter } from '../PySceneDetectAdapter';
import { ToolchainOrchestrator } from '../ToolchainOrchestrator';
import * as child_process from 'child_process';
import * as fs from 'fs';

vi.mock('child_process', () => {
  return {
    exec: (command: string, cb: any) => {
      if (command.includes('ffprobe -version')) {
        cb(null, { stdout: 'ffprobe version 4.4.2-0ubuntu0.22.04.1', stderr: '' });
      } else if (command.includes('scenedetect version')) {
        cb(null, { stdout: 'PySceneDetect v0.6.1.1', stderr: '' });
      } else if (command.includes('ffprobe') && command.includes('fake_video.mp4')) {
        cb(null, { 
          stdout: JSON.stringify({
            format: { duration: "120.5" },
            streams: [
              { codec_type: "video", width: 1920, height: 1080, codec_name: "h264", r_frame_rate: "24000/1001" },
              { codec_type: "audio" }
            ]
          }),
          stderr: ''
        });
      } else if (command.includes('scenedetect') && command.includes('fake_video.mp4')) {
        // Pretend it successfully creates the CSV file, we'll mock fs.existsSync and fs.readFile in the test
        cb(null, { stdout: 'Scene count: 2', stderr: '' });
      } else if (command.includes('corrupted.mp4')) {
        cb(new Error('Invalid data found'), { stdout: '', stderr: 'Invalid data' });
      } else {
        cb(new Error('Command not found'), { stdout: '', stderr: '' });
      }
    }
  };
});

vi.mock('fs', async (importOriginal) => {
  const actual = await importOriginal<typeof import('fs')>();
  return {
    ...actual,
    existsSync: (path: string) => {
      if (path.includes('scenedetect') || path.includes('scene_')) return true;
      return actual.existsSync(path);
    },
    readFile: (path: string, options: any, cb: any) => {
      if (typeof options === 'function') {
        cb = options;
      }
      if (path.includes('scene_')) {
        const fakeCsv = `Timecode List:
Scene Number,Start Frame,Start Timecode,Start Time (seconds),End Frame,End Timecode,End Time (seconds),Length (frames),Length (timecode),Length (seconds)
1,0,00:00:00.000,0.0,240,00:00:10.000,10.0,240,00:00:10.000,10.0
2,240,00:00:10.000,10.0,480,00:00:20.000,20.0,240,00:00:10.000,10.0`;
        cb(null, fakeCsv);
      } else {
        actual.readFile(path, options, cb);
      }
    },
    unlink: (path: string, cb: any) => {
      cb(null);
    }
  };
});

describe('Toolchain Integration Layer', () => {
  it('PySceneDetectAdapter analyzes scenes successfully', async () => {
    const adapter = new PySceneDetectAdapter();
    const isAvail = await adapter.isAvailable();
    const version = await adapter.getVersion();
    
    expect(isAvail).toBe(true);
    expect(version).toBe('0.6.1.1');
    
    const result = await adapter.analyzeMedia('fake_video.mp4');
    expect(result.provenance.success).toBe(true);
    expect(result.scenes).toBeDefined();
    expect(result.scenes?.length).toBe(2);
    expect(result.scenes?.[0].startTime).toBe(0.0);
    expect(result.scenes?.[0].endTime).toBe(10.0);
    expect(result.scenes?.[1].startTime).toBe(10.0);
    expect(result.scenes?.[1].endTime).toBe(20.0);
  });

  it('ToolchainOrchestrator invokes tools and returns unified results', async () => {
    const orchestrator = new ToolchainOrchestrator();
    const results = await orchestrator.analyzeFile('fake_video.mp4');
    
    expect(results.length).toBe(3);
    
    const ffprobeRes = results.find(r => r.provenance.tool === 'ffprobe');
    const sceneRes = results.find(r => r.provenance.tool === 'scenedetect');
    
    expect(ffprobeRes?.metadata?.width).toBe(1920);
    expect(sceneRes?.scenes?.length).toBe(2);
  });
});
