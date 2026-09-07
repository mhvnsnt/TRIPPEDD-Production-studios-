import React, { useState, useEffect } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import { HardDrive, ShieldCheck, FileVideo, Database, RefreshCcw, Search, Link as LinkIcon, Activity, CheckCircle, AlertTriangle, XCircle, List, Play } from 'lucide-react';
import { PhysicalTimelineManager } from '../core/pipeline/physicalTimeline';

import { DependencyPanel } from './ingest/DependencyPanel';
import { SummaryDashboard } from './ingest/SummaryDashboard';
import { PhysicalTimelineView } from './ingest/PhysicalTimelineView';
import { StoryboardComparison } from './ingest/StoryboardComparison';
import { PipelineMonitor } from './ingest/PipelineMonitor';
import { PipelineHealthView } from './ingest/PipelineHealthView';
import { MediaJob } from '../core/types';

interface IngestFile {
  id: string;
  name: string;
  mimeType: string;
  size?: string;
  thumbnailLink?: string;
  videoMediaMetadata?: { durationMillis: string };
}

export function DriveIngestWorkspace() {
  const [activeTab, setActiveTab] = useState<'ingest'|'dashboard'|'timeline'|'comparison'>('ingest');
  const [folderUrl, setFolderUrl] = useState('https://drive.google.com/drive/folders/1e55zooUU98r9MXyRzcR0qgNq1EqGiqVI');
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [files, setFiles] = useState<IngestFile[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [ptManager] = useState(() => new PhysicalTimelineManager());
  const [timelineState, setTimelineState] = useState(ptManager.getTimeline());
  
  const [analyzingFileId, setAnalyzingFileId] = useState<string | null>(null);
  const [analysisJob, setAnalysisJob] = useState<any>(null);
  const [jobIntervalId, setJobIntervalId] = useState<any>(null);

  const login = useGoogleLogin({
    onSuccess: (tokenResponse) => {
      setAccessToken(tokenResponse.access_token);
      if (folderUrl) fetchFiles(tokenResponse.access_token, folderUrl);
    },
    scope: 'https://www.googleapis.com/auth/drive.readonly',
    onError: (err) => setError('Failed to authenticate with Google Drive.')
  });

  const extractFolderId = (url: string) => {
    const match = url.match(/folders\/([a-zA-Z0-9-_]+)/);
    return match ? match[1] : url;
  };

  const fetchFiles = async (token: string, url: string) => {
    setIsLoading(true); setError(null);
    try {
      const folderId = extractFolderId(url);
      if (!folderId) throw new Error('Invalid folder URL or ID.');
      
      const q = `'${folderId}' in parents and trashed = false`;
      const response = await fetch(
        `https://www.googleapis.com/drive/v3/files?q=${encodeURIComponent(q)}&fields=files(id,name,mimeType,size,thumbnailLink,videoMediaMetadata)`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'Failed to fetch files from Drive.');
      }
      const data = await response.json();
      setFiles(data.files || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFetchClick = () => {
    if (!accessToken) login();
    else fetchFiles(accessToken, folderUrl);
  };

  const pollJobStatus = async (jobId: string) => {
    try {
      const res = await fetch(`/api/jobs/${jobId}`);
      if (res.ok) {
        const data = await res.json();
        setAnalysisJob(data);
        if (data.status === 'COMPLETED' || data.status === 'FAILED') return true;
      }
    } catch (e) { }
    return false;
  };

  const startAnalysis = async (file: IngestFile) => {
    if (!accessToken) return;
    setAnalyzingFileId(file.id);
    setAnalysisJob({ status: 'STARTING', logs: [], progress: 0 });
    try {
      const res = await fetch('/api/ingest/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileId: file.id, token: accessToken, originalName: file.name, mimeType: file.mimeType })
      });
      if (!res.ok) throw new Error('Failed to start analysis');
      const { jobId } = await res.json();
      const interval = setInterval(async () => {
        const done = await pollJobStatus(jobId);
        if (done) clearInterval(interval);
      }, 1000);
      setJobIntervalId(interval);
    } catch (e: any) {
      setAnalysisJob({ status: 'FAILED', logs: [e.message], progress: 0 });
    }
  };

  useEffect(() => {
    return () => { if (jobIntervalId) clearInterval(jobIntervalId); };
  }, [jobIntervalId]);

  
  const promoteToSourceClip = (job: MediaJob) => {
    // Create a SourceClip
    const newClip = {
      id: job.fileId,
      assetId: job.originalName,
      startTimecode: '00:00:00',
      endTimecode: 'Unknown',
      description: 'Ingested source file',
      hash: job.hash || ''
    };
    
    // Mutating through manager to ensure standard API usage
    const tl = ptManager.getTimeline();
    if (!tl.clips.some(c => c.id === job.fileId)) {
       tl.clips.push(newClip as any);
    }
    
    // Process real tools that executed successfully
    if (job.tools?.ffprobe?.status === 'COMPLETED') {
        const data = job.tools.ffprobe.data;
        const videoStream = data.streams?.find((s: any) => s.codec_type === 'video');
        const audioStream = data.streams?.find((s: any) => s.codec_type === 'audio');
        
        ptManager.addObservation({
           id: 'obs_ffprobe_' + Date.now(),
           sourceClipId: job.fileId,
           type: 'VISUAL',
           description: `Video: ${videoStream?.codec_name || 'unknown'} ${videoStream?.width}x${videoStream?.height} ${videoStream?.r_frame_rate}fps | Audio: ${audioStream?.codec_name || 'unknown'}`,
           confidence: 1.0,
           origin: 'MACHINE_GENERATED',
           reviewState: 'CONFIRMED',
           editorialClassification: 'PRODUCTION_ARTIFACT',
           editorialReason: 'Technical metadata',
           createdAt: new Date().toISOString(),
           toolProvenance: job.tools.ffprobe.provenance
        } as any);
    }

    setTimelineState({...ptManager.getTimeline()});
  };


  const formatDuration = (millis?: string) => {
    if (!millis) return 'Unknown';
    const totalSeconds = Math.floor(parseInt(millis, 10) / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const renderStatusIcon = (status: string) => {
    if (status === 'COMPLETED') return <CheckCircle size={14} className="text-green-500" />;
    if (status === 'UNAVAILABLE') return <AlertTriangle size={14} className="text-yellow-500" />;
    if (status === 'FAILED') return <XCircle size={14} className="text-red-500" />;
    return <RefreshCcw size={14} className="text-blue-500 animate-spin" />;
  };

  const renderAnalysisModal = () => {
    if (!analyzingFileId || !analysisJob) return null;
    const file = files.find(f => f.id === analyzingFileId);
    return (
      <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6">
        <div className="bg-neutral-900 border border-neutral-700 rounded-lg shadow-2xl w-full max-w-4xl flex flex-col max-h-full">
          <div className="p-4 border-b border-neutral-800 flex items-center justify-between">
            <h3 className="text-lg font-bold text-white uppercase tracking-widest flex items-center">
              <Activity className="mr-3 text-blue-500" size={20} /> Media Analysis: {file?.name}
            </h3>
            <button onClick={() => { setAnalyzingFileId(null); setAnalysisJob(null); if (jobIntervalId) clearInterval(jobIntervalId); }} className="text-neutral-400 hover:text-white">
              <XCircle size={24} />
            </button>
          </div>
          <div className="p-6 overflow-y-auto custom-scrollbar flex-1 flex flex-col md:flex-row gap-6">
            <div className="flex-1 space-y-6">
              <div>
                <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-widest mb-3">Pipeline Status</h4>
                <div className="space-y-2">
                  <div className="flex items-center justify-between p-3 bg-black border border-neutral-800 rounded">
                    <span className="text-sm font-mono text-white">Drive Access</span>
                    <CheckCircle size={14} className="text-green-500" />
                  </div>
                  {['ffprobe', 'ffmpeg', 'pyscenedetect', 'whisper', 'vlm'].map(tool => {
                     const toolState = analysisJob.result ? analysisJob.result[tool] : analysisJob.analysis?.[tool];
                     const status = toolState?.status || 'PENDING';
                     return (
                      <div key={tool} className="flex items-center justify-between p-3 bg-black border border-neutral-800 rounded">
                        <span className="text-sm font-mono text-white">{tool}</span>
                        <div className="flex items-center text-xs font-bold uppercase tracking-wider text-neutral-400">
                          <span className="mr-2">{status}</span>{renderStatusIcon(status)}
                        </div>
                      </div>
                     );
                  })}
                </div>
              </div>
            </div>
            <div className="flex-1 flex flex-col">
              <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-widest mb-3">Execution Logs</h4>
              <div className="flex-1 bg-black border border-neutral-800 rounded p-4 font-mono text-xs text-green-400 overflow-y-auto whitespace-pre-wrap max-h-96">
                {analysisJob.logs?.map((l: string, i: number) => <div key={i} className="mb-1">{l}</div>)}
                {analysisJob.status === 'RUNNING' && <div className="animate-pulse mt-2">_</div>}
              </div>
            </div>
          </div>
          <div className="p-4 border-t border-neutral-800 flex justify-end">
             {analysisJob.status === 'COMPLETED' ? (
                <button onClick={promoteToSourceClip} className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-md text-sm font-bold tracking-wide uppercase transition-colors">
                  Create SourceClip Record
                </button>
             ) : (
                <div className="flex items-center text-neutral-400 text-sm font-bold uppercase tracking-widest">
                  {analysisJob.status === 'FAILED' ? 'Analysis Failed' : 'Analyzing...'}
                </div>
             )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="h-full flex flex-col bg-black text-white">
      <header className="px-6 py-4 border-b border-neutral-800 bg-black/50 backdrop-blur-md flex items-center justify-between shrink-0">
        <div>
          <h1 className="text-xl font-bold uppercase tracking-widest text-white flex items-center">
            <HardDrive className="mr-3 text-blue-500" size={20} /> Source Reality / Media Ingest
          </h1>
          <p className="text-neutral-400 text-sm mt-1">Immutable source ingestion, analysis, and chronological verification.</p>
        </div>
        <div className="flex items-center space-x-3">
          {accessToken ? (
            <div className="flex items-center px-3 py-1.5 bg-green-950/30 border border-green-900/50 rounded-md text-green-400 text-xs font-bold">
              <ShieldCheck size={14} className="mr-2" /> DRIVE AUTHENTICATED
            </div>
          ) : (
            <button onClick={() => login()} className="flex items-center px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-white rounded-md text-xs font-bold transition-colors">
              AUTHENTICATE DRIVE
            </button>
          )}
        </div>
      </header>
      
      <div className="flex border-b border-neutral-800 shrink-0">
        <button onClick={() => setActiveTab('ingest')} className={`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'ingest' ? 'border-blue-500 text-blue-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}`}>
          Ingest & Discovery
        </button>
        <button onClick={() => setActiveTab('dashboard')} className={`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'dashboard' ? 'border-blue-500 text-blue-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}`}>
          Telemetry
        </button>
        <button onClick={() => setActiveTab('timeline')} className={`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'timeline' ? 'border-blue-500 text-blue-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}`}>
          Physical Timeline
        </button>
        <button onClick={() => setActiveTab('comparison')} className={`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors ${activeTab === 'comparison' ? 'border-blue-500 text-blue-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}`}>
          Storyboard Comparison
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
        <div className="max-w-5xl mx-auto space-y-8">
          
          
  {activeTab === 'ingest' && (
     <div className="h-full mt-[-24px] mx-[-24px]">
       <div className="px-6 pt-6">
         <PipelineHealthView accessToken={accessToken} folderUrl={folderUrl} />
       </div>
       <PipelineMonitor 
          folderUrl={folderUrl} 
          accessToken={accessToken} 
          onJobPromote={promoteToSourceClip} 
          timelineClips={timelineState.clips.map((c: any) => c.id)}
       />
     </div>
  )}


          {activeTab === 'dashboard' && <SummaryDashboard timeline={timelineState} totalDriveFiles={files.length} />}
          
          {activeTab === 'timeline' && (
             <PhysicalTimelineView 
               timeline={timelineState} 
               onConfirm={(id) => { ptManager.confirmObservation(id); setTimelineState({...ptManager.getTimeline()}); }}
               onReject={(id) => { ptManager.rejectObservation(id); setTimelineState({...ptManager.getTimeline()}); }}
             />
          )}

          {activeTab === 'comparison' && <StoryboardComparison results={ptManager.compareWithStoryboard()} />}

        </div>
      </div>
      {renderAnalysisModal()}
    </div>
  );
}
