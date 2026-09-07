import React, { useEffect, useState } from 'react';
import { CheckCircle, AlertTriangle, XCircle, RefreshCcw, Activity } from 'lucide-react';

interface ToolStatus {
  installed: boolean;
  version?: string;
  error?: string;
}

export function DependencyPanel() {
  const [tools, setTools] = useState<Record<string, ToolStatus>>({});
  const [loading, setLoading] = useState(true);

  const toolsToCheck = ['ffmpeg', 'ffprobe', 'comfyui', 'pyscenedetect', 'whisper', 'opencv', 'tesseract'];

  useEffect(() => {
    checkTools();
  }, []);

  const checkTools = async () => {
    setLoading(true);
    const results: Record<string, ToolStatus> = {};
    for (const tool of toolsToCheck) {
      // Mocking check for ones that might not exist in backend directly, but we map them to existing api
      // The backend has /api/tools/:tool/detect
      try {
        const res = await fetch(`/api/tools/\${tool}/detect`);
        if (res.ok) {
          results[tool] = await res.json();
        } else {
          results[tool] = { installed: false, error: 'Endpoint error' };
        }
      } catch (e: any) {
        results[tool] = { installed: false, error: e.message };
      }
    }
    setTools(results);
    setLoading(false);
  };

  const renderIcon = (status: ToolStatus) => {
    if (status.installed) return <CheckCircle className="text-green-500" size={16} />;
    return <AlertTriangle className="text-yellow-500" size={16} />;
  };

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-sm font-bold text-neutral-500 uppercase tracking-widest flex items-center">
          <Activity size={16} className="mr-2" /> Open-Source Dependencies
        </h2>
        <button onClick={checkTools} disabled={loading} className="text-blue-500 hover:text-blue-400">
          <RefreshCcw size={14} className={loading ? 'animate-spin' : ''} />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {toolsToCheck.map(tool => {
          const status = tools[tool];
          return (
            <div key={tool} className="flex flex-col p-4 bg-black border border-neutral-800 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="font-mono text-sm text-white font-bold">{tool}</span>
                {status ? renderIcon(status) : <RefreshCcw className="text-neutral-500 animate-spin" size={16} />}
              </div>
              <div className="text-xs font-mono text-neutral-400">
                {status?.installed ? (
                  <span className="text-green-400">{status.version}</span>
                ) : (
                  <span className="text-red-400">{status?.error || 'UNAVAILABLE'}</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
