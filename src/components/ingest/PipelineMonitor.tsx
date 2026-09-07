import React, { useState, useEffect } from 'react';
import { Activity, RefreshCcw, CheckCircle, AlertTriangle, XCircle, Search, Video, HardDrive, Database, Settings, RefreshCw, FileVideo, Cpu } from 'lucide-react';
import { MediaJob, JobToolStatus } from '../../core/types';

interface Props {
  folderUrl: string;
  accessToken: string | null;
  onJobPromote: (job: MediaJob) => void;
  timelineClips: string[];
}

export function PipelineMonitor({ folderUrl, accessToken, onJobPromote, timelineClips }: Props) {
  const [jobs, setJobs] = useState<MediaJob[]>([]);
  const [isScanning, setIsScanning] = useState(false);
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);

  const fetchJobs = async () => {
    try {
      const res = await fetch('/api/queue');
      if (res.ok) setJobs(await res.json());
    } catch(e) {}
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleScan = async () => {
    if (!accessToken) return;
    setIsScanning(true);
    const folderId = folderUrl.split('/').pop();
    try {
      await fetch('/api/queue/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folderId, token: accessToken })
      });
      await fetchJobs();
    } catch(e) {}
    setIsScanning(false);
  };

  const handleRetry = async (fileId: string) => {
     try {
       await fetch(`/api/queue/${fileId}/retry`, { method: 'POST' });
       await fetchJobs();
     } catch(e) {}
  };

  const selectedJob = jobs.find(j => j.fileId === selectedJobId);

  const renderJobToolStatus = (name: string, status?: JobToolStatus) => {
    if (!status) return null;
    return (
       <div key={name} className="flex flex-col p-2 bg-neutral-900 border border-neutral-800 rounded">
         <div className="flex items-center justify-between">
           <span className="text-xs font-mono text-white capitalize">{name}</span>
           {status.status === 'COMPLETED' ? <CheckCircle size={12} className="text-green-500" /> :
            status.status === 'UNAVAILABLE' ? <AlertTriangle size={12} className="text-yellow-500" /> :
            status.status === 'FAILED' ? <XCircle size={12} className="text-red-500" /> :
            <RefreshCcw size={12} className="text-blue-500 animate-spin" />}
         </div>
         {status.provenance && (
           <div className="mt-1 text-[9px] text-neutral-500 font-mono truncate">
             {status.provenance.version}
           </div>
         )}
       </div>
    );
  };

  const formatDuration = (millis?: string) => {
    if (!millis) return 'Unknown';
    const totalSeconds = Math.floor(parseInt(millis, 10) / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="flex-1 flex overflow-hidden">
      {/* Left panel: Queue List */}
      <div className="w-1/2 border-r border-neutral-800 flex flex-col bg-black overflow-hidden">
        <div className="p-4 border-b border-neutral-800 flex items-center justify-between shrink-0 bg-neutral-950/50">
           <div className="flex items-center space-x-2 text-sm font-bold uppercase tracking-widest text-neutral-300">
             <Cpu size={16} className="text-blue-500" />
             <span>Automated Media Pipeline</span>
           </div>
           <button onClick={handleScan} disabled={isScanning || !accessToken} className="flex items-center px-4 py-2 bg-blue-900/30 text-blue-400 hover:bg-blue-900/50 rounded text-xs font-bold transition-colors disabled:opacity-50">
             {isScanning ? <RefreshCcw size={14} className="animate-spin mr-2" /> : <Search size={14} className="mr-2" />}
             Process New Media
           </button>
        </div>
        
        {/* Dashboard summary */}
        <div className="flex items-center space-x-4 p-4 border-b border-neutral-800 bg-neutral-900/30 shrink-0">
           <div className="flex-1 text-center">
             <div className="text-2xl font-bold text-white">{jobs.length}</div>
             <div className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest">Discovered</div>
           </div>
           <div className="w-px h-8 bg-neutral-800"></div>
           <div className="flex-1 text-center">
             <div className="text-2xl font-bold text-yellow-400">{jobs.filter(j => ['QUEUED', 'DOWNLOADING/STREAMING', 'PROBING', 'ANALYZING'].includes(j.state)).length}</div>
             <div className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest">Processing</div>
           </div>
           <div className="w-px h-8 bg-neutral-800"></div>
           <div className="flex-1 text-center">
             <div className="text-2xl font-bold text-emerald-400">{jobs.filter(j => j.state === 'NEEDS_REVIEW' || j.state === 'EVIDENCE_READY').length}</div>
             <div className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest">Awaiting Review</div>
           </div>
        </div>

        <div className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-3">
          {jobs.length === 0 ? (
            <div className="text-center py-12 text-neutral-500 text-sm">
               No media discovered yet. Click "Process New Media".
            </div>
          ) : (
            jobs.map(job => (
              <div key={job.id} onClick={() => setSelectedJobId(job.fileId)} className={`p-4 rounded-lg border cursor-pointer transition-colors ${selectedJobId === job.fileId ? 'bg-blue-900/10 border-blue-500/50' : 'bg-neutral-900/50 border-neutral-800 hover:border-neutral-700'}`}>
                <div className="flex items-center justify-between mb-2">
                  <div className="font-mono text-sm text-white truncate mr-4">{job.originalName}</div>
                  <div className={`px-2 py-1 rounded text-[10px] font-bold tracking-wider uppercase ${
                     job.state === 'NEEDS_REVIEW' ? 'bg-emerald-500/20 text-emerald-400' :
                     job.state === 'FAILED' ? 'bg-red-500/20 text-red-400' :
                     ['QUEUED','PROBING','ANALYZING','DOWNLOADING/STREAMING'].includes(job.state) ? 'bg-yellow-500/20 text-yellow-400' :
                     'bg-neutral-800 text-neutral-400'
                  }`}>
                    {job.state}
                  </div>
                </div>
                <div className="flex items-center justify-between text-xs text-neutral-500">
                  <span>{job.mimeType}</span>
                  <div className="flex items-center space-x-1">
                     {Object.entries(job.tools).map(([name, statusRaw]) => { const status = statusRaw as JobToolStatus; return (
                        <div key={name} title={name} className={`w-2 h-2 rounded-full ${
                          status.status === 'COMPLETED' ? 'bg-green-500' :
                          status.status === 'UNAVAILABLE' ? 'bg-neutral-700' :
                          status.status === 'FAILED' ? 'bg-red-500' : 'bg-yellow-500 animate-pulse'
                        }`}></div>
                     );})}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Right panel: Details */}
      <div className="w-1/2 flex flex-col bg-neutral-950">
         {selectedJob ? (
           <div className="flex-1 flex flex-col h-full overflow-hidden">
             <div className="p-6 border-b border-neutral-800 shrink-0">
               <div className="flex justify-between items-start">
                 <div>
                   <h2 className="text-xl font-bold text-white mb-1 break-all">{selectedJob.originalName}</h2>
                   <div className="text-xs font-mono text-neutral-500">ID: {selectedJob.fileId}</div>
                 </div>
               </div>
               
               <div className="grid grid-cols-2 gap-4 mt-6">
                 {Object.entries(selectedJob.tools).map(([name, status]) => renderJobToolStatus(name, status as JobToolStatus))}
               </div>

               {selectedJob.state === 'NEEDS_REVIEW' && !timelineClips.includes(selectedJob.fileId) && (
                 <button onClick={() => onJobPromote(selectedJob)} className="w-full mt-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-bold uppercase tracking-wider text-xs transition-colors">
                    Promote to SourceClip & Extract Evidence
                 </button>
               )}
               {timelineClips.includes(selectedJob.fileId) && (
                 <div className="w-full mt-6 py-3 bg-neutral-900 border border-neutral-800 text-neutral-500 text-center rounded font-bold uppercase tracking-wider text-xs">
                    Promoted to Timeline
                 </div>
               )}
               {selectedJob.state === 'FAILED' && (
                 <button onClick={() => handleRetry(selectedJob.fileId)} className="w-full mt-6 py-3 bg-neutral-800 hover:bg-neutral-700 text-white rounded font-bold uppercase tracking-wider text-xs transition-colors">
                    Retry Pipeline
                 </button>
               )}
             </div>

             <div className="flex-1 overflow-y-auto custom-scrollbar p-6 bg-black">
                <h3 className="text-xs font-bold uppercase tracking-widest text-neutral-500 mb-4">Pipeline Execution Logs</h3>
                <div className="font-mono text-[10px] text-green-400/80 space-y-1">
                   {selectedJob.logs.map((log, i) => (
                     <div key={i} className="break-all">{log}</div>
                   ))}
                </div>
             </div>
           </div>
         ) : (
           <div className="flex-1 flex items-center justify-center text-neutral-600 text-sm">
             Select a media job to view details
           </div>
         )}
      </div>
    </div>
  );
}
