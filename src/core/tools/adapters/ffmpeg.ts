import { ToolAdapter, ToolStatus, ToolDefinition, Job } from '../../types';

export class FFmpegAdapter implements ToolAdapter {
  id = 'ffmpeg';
  definition: ToolDefinition = {
    id: 'ffmpeg',
    name: 'FFmpeg',
    category: 'Media',
    description: 'Core media processing/transcoding/inspection',
    license: 'LGPL/GPL',
    installationStatus: 'UNAVAILABLE' as ToolStatus,
    integrationType: 'CLI' as const,
    capabilities: {
      canLaunch: false,
      canOpenProject: false,
      canImportAsset: true,
      canExportAsset: true,
      canSubmitJob: true
    },
    healthStatus: 'UNAVAILABLE' as ToolStatus
  };

  async detect(): Promise<ToolStatus> {
    try {
      const res = await fetch('/api/tools/ffmpeg/detect');
      if (res.ok) {
        const data = await res.json();
        if (data.installed) {
          this.definition.version = data.version;
          return 'AVAILABLE';
        }
      }
      return 'NOT_INSTALLED';
    } catch (e) {
      return 'NOT_INSTALLED';
    }
  }

  async healthCheck(): Promise<ToolStatus> {
    return this.detect();
  }

  async execute(job: Job, onUpdate: (update: Partial<Job>) => void): Promise<void> {
    const isImage = job.operation === 'extract_frame';
    const ext = isImage ? 'png' : 'mp4';
    const outputPath = `/trippedd_project/assets/generated/ffmpeg/${job.id}_out.${ext}`;
    
    // Construct command based on operation
    let command: string[] = [];
    if (job.operation === 'extract_frame') {
       command = [
         "-y",
         "-i", "public" + job.inputs.videoPath,
         "-ss", "00:00:01",
         "-vframes", "1",
         "public" + outputPath
       ];
    } else if (job.operation === 'green_iris_freeze') {
       command = [
         "-y",
         "-i", "public" + job.inputs.videoPath,
         "-i", "public" + job.inputs.characterPath,
         "-filter_complex", "[0:v][1:v]overlay=(W-w)/2:(H-h)/2,fade=t=out:st=1:d=1:color=green[v]",
         "-map", "[v]",
         "-t", "2",
         "public" + outputPath
       ];
    } else if (job.operation === 'concatenate_sequence') {
       command = [
         "-y",
         "-i", "public" + job.inputs.segments[0],
         "-loop", "1", "-t", "2", "-i", "public" + job.inputs.segments[1],
         "-loop", "1", "-t", "2", "-i", "public" + job.inputs.segments[2],
         "-filter_complex",
         "[1:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v1];" +
         "[2:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1[v2];" +
         "[0:v]scale=1280:720,setsar=1[v0];" +
         "[v0][v1][v2]concat=n=3:v=1:a=0[outv]",
         "-map", "[outv]",
         "public" + outputPath
       ];
    } else if (job.operation === 'composite_overlay') {
       command = [
         "-y",
         "-i", "public" + job.inputs.videoPath,
         "-i", "public" + job.inputs.imagePath,
         "-filter_complex", "[0:v][1:v]overlay=10:10",
         "-c:a", "copy",
         "public" + outputPath
       ];
    } else {
       command = [
         "-y",
         "-i", "public" + (job.inputs.inputFile || job.inputs.videoPath),
         "-vf", "hue=s=0",
         "-c:a", "copy",
         "public" + outputPath
       ];
    }

    try {
      const res = await fetch('/api/jobs/ffmpeg', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, output_path: outputPath })
      });
      const { jobId } = await res.json();
      
      // Polling loop
      while (true) {
        await new Promise(r => setTimeout(r, 500));
        const statusRes = await fetch(`/api/jobs/${jobId}`);
        const data = await statusRes.json();
        
        const update: Partial<Job> = {
          status: data.status,
          progress: data.progress,
          logs: data.logs || []
        };
        
        if (data.result) {
          update.outputs = { path: data.result.path };
        }
        
        onUpdate(update);
        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          break;
        }
      }
    } catch (e: any) {
      onUpdate({ status: 'FAILED', logs: [...(job.logs || []), `Error: ${e.message}`] });
    }
  }
}
