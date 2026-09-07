export interface ToolExecutionResult {
  success: boolean;
  tool: string;
  command: string;
  stdout: string;
  stderr: string;
  exitCode: number | null;
  timestamp: string;
  version?: string;
  error?: string;
}

export interface ToolAdapter {
  readonly name: string;
  isAvailable(): Promise<boolean>;
  getVersion(): Promise<string | undefined>;
}

export interface MediaMetadata {
  duration?: number;
  width?: number;
  height?: number;
  codec?: string;
  fps?: number;
  hasAudio?: boolean;
}

export interface MediaAnalysisResult {
  metadata?: MediaMetadata;
  scenes?: { startTime: number; endTime: number }[];
  transcripts?: { startTime: number; endTime: number; text: string }[];
  provenance: ToolExecutionResult;
}
