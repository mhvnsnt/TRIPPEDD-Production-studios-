const fs = require('fs');

let content = fs.readFileSync('src/components/DriveIngestWorkspace.tsx', 'utf8');

// Replace standard imports
content = content.replace(
  "import { HardDrive, Link as LinkIcon, RefreshCcw, FileVideo, ShieldCheck, Database } from 'lucide-react';",
  "import { HardDrive, Link as LinkIcon, RefreshCcw, FileVideo, ShieldCheck, Database, Activity, CheckCircle, AlertTriangle, XCircle, Search } from 'lucide-react';"
);

// Define state for jobs and reports
const stateAdditions = `
  const [analyzingFileId, setAnalyzingFileId] = useState<string | null>(null);
  const [analysisJob, setAnalysisJob] = useState<any>(null);
  const [jobIntervalId, setJobIntervalId] = useState<any>(null);
`;

content = content.replace(
  "const [error, setError] = useState<string | null>(null);",
  "const [error, setError] = useState<string | null>(null);\n" + stateAdditions
);

// Implement handleAnalyze
const handleAnalyze = `
  const pollJobStatus = async (jobId: string) => {
    try {
      const res = await fetch(\`/api/jobs/\${jobId}\`);
      if (res.ok) {
        const data = await res.json();
        setAnalysisJob(data);
        if (data.status === 'COMPLETED' || data.status === 'FAILED') {
          return true; // done
        }
      }
    } catch (e) {
      console.error('Poll error', e);
    }
    return false;
  };

  const startAnalysis = async (file: DriveFile) => {
    if (!accessToken) return;
    setAnalyzingFileId(file.id);
    setAnalysisJob({ status: 'STARTING', logs: [], progress: 0 });
    
    try {
      const res = await fetch('/api/ingest/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fileId: file.id,
          token: accessToken,
          originalName: file.name,
          mimeType: file.mimeType
        })
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

  React.useEffect(() => {
    return () => {
      if (jobIntervalId) clearInterval(jobIntervalId);
    };
  }, [jobIntervalId]);
`;

content = content.replace(
  "const handleFetchClick = () => {",
  handleAnalyze + "\n  const handleFetchClick = () => {"
);

// Render the analysis report
const renderAnalysis = `
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
              <Activity className="mr-3 text-blue-500" size={20} />
              Media Analysis: {file?.name}
            </h3>
            <button 
              onClick={() => { setAnalyzingFileId(null); setAnalysisJob(null); if (jobIntervalId) clearInterval(jobIntervalId); }}
              className="text-neutral-400 hover:text-white"
            >
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
                          <span className="mr-2">{status}</span>
                          {renderStatusIcon(status)}
                        </div>
                      </div>
                     );
                  })}
                </div>
              </div>
              
              {analysisJob.result?.hash && (
                <div>
                   <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-widest mb-3">Immutable Source</h4>
                   <div className="p-3 bg-black border border-neutral-800 rounded font-mono text-xs text-neutral-300 break-all">
                     MD5: {analysisJob.result.hash}
                   </div>
                </div>
              )}
            </div>
            
            <div className="flex-1 flex flex-col">
              <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-widest mb-3">Execution Logs</h4>
              <div className="flex-1 bg-black border border-neutral-800 rounded p-4 font-mono text-xs text-green-400 overflow-y-auto whitespace-pre-wrap">
                {analysisJob.logs?.map((l: string, i: number) => (
                  <div key={i} className="mb-1">{l}</div>
                ))}
                {analysisJob.status === 'RUNNING' && (
                  <div className="animate-pulse mt-2">_</div>
                )}
              </div>
            </div>
          </div>
          
          <div className="p-4 border-t border-neutral-800 flex justify-end">
             {analysisJob.status === 'COMPLETED' ? (
                <button className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-md text-sm font-bold tracking-wide uppercase transition-colors">
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
`;

content = content.replace(
  "return (",
  renderAnalysis + "\n  return ("
);

// Add the Analyze button to the file cards
content = content.replace(
  "<span className=\"text-[10px] font-mono text-neutral-500\">\n                          {file.size ? (parseInt(file.size, 10) / (1024 * 1024)).toFixed(1) + ' MB' : 'Unknown size'}\n                        </span>",
  "<span className=\"text-[10px] font-mono text-neutral-500\">\n                          {file.size ? (parseInt(file.size, 10) / (1024 * 1024)).toFixed(1) + ' MB' : 'Unknown size'}\n                        </span>\n                      </div>\n                      <button onClick={() => startAnalysis(file)} className=\"w-full mt-3 py-2 bg-neutral-800 hover:bg-blue-900 hover:text-blue-400 text-neutral-400 rounded text-xs font-bold uppercase tracking-wider flex items-center justify-center transition-colors\">\n                        <Search size={14} className=\"mr-2\" /> Run Analysis\n                      </button>"
);

// Add the modal overlay
content = content.replace(
  "</div>\n      </div>\n    </div>",
  "</div>\n      </div>\n      {renderAnalysisModal()}\n    </div>"
);

fs.writeFileSync('src/components/DriveIngestWorkspace.tsx', content);
