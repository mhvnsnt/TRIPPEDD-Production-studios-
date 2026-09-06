import { useState, useEffect, useMemo } from 'react';
import { Settings, RefreshCw, Play, CheckCircle2, AlertCircle, XCircle } from 'lucide-react';
import { ToolRegistry } from '../core/tools/registry';
import { ToolDefinition, ToolStatus } from '../core/types';

export function ToolManager() {
  const [tools, setTools] = useState<ToolDefinition[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initial load
    setTools(ToolRegistry.getAllDefinitions());
    setLoading(false);
  }, []);

  const handleDetect = async (toolId: string) => {
    const adapter = ToolRegistry.getAdapter(toolId);
    if (!adapter) return;
    
    // Optimistic UI update
    setTools(prev => prev.map(t => t.id === toolId ? { ...t, installationStatus: 'NOT_CHECKED' } : t));
    
    try {
      const status = await adapter.detect();
      setTools(prev => prev.map(t => {
        if (t.id === toolId) {
          return { ...t, installationStatus: status };
        }
        return t;
      }));
      // Update definition in registry (just for in-memory persistence)
      adapter.definition.installationStatus = status;
    } catch (err) {
      setTools(prev => prev.map(t => t.id === toolId ? { ...t, installationStatus: 'ERROR' } : t));
    }
  };

  const handleDetectAll = async () => {
    for (const tool of tools) {
      if (tool.installationStatus !== 'NOT_IMPLEMENTED') {
        await handleDetect(tool.id);
      }
    }
  };

  const StatusBadge = ({ status }: { status: ToolStatus }) => {
    switch (status) {
      case 'INSTALLED':
      case 'CONFIGURED':
      case 'CONNECTED':
      case 'RUNNING':
        return <span className="bg-emerald-500/10 text-emerald-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-emerald-500/20"><CheckCircle2 size={12} /> {status}</span>;
      case 'ERROR':
        return <span className="bg-red-500/10 text-red-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-red-500/20"><XCircle size={12} /> ERROR</span>;
      case 'NOT_IMPLEMENTED':
      case 'UNSUPPORTED':
        return <span className="bg-neutral-800 text-neutral-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-neutral-700"> {status}</span>;
      case 'NOT_INSTALLED':
        return <span className="bg-amber-500/10 text-amber-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-amber-500/20"><AlertCircle size={12} /> NOT INSTALLED</span>;
      default:
        return <span className="bg-neutral-800 text-neutral-400 px-2 py-1 rounded text-xs font-bold border border-neutral-700">{status}</span>;
    }
  };

  const groupedTools = useMemo(() => {
    const groups: Record<string, ToolDefinition[]> = {};
    tools.forEach(tool => {
      const cat = tool.category || 'Other';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(tool);
    });
    return groups;
  }, [tools]);

  return (
    <div className="p-8 max-w-6xl mx-auto w-full space-y-8">
      <header className="border-b border-neutral-800 pb-6 flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black tracking-tight text-white mb-2">TOOL MANAGER</h2>
          <p className="text-neutral-400">Discover, install, and configure integrated creative tools.</p>
        </div>
        <button 
          onClick={handleDetectAll}
          className="bg-neutral-800 hover:bg-neutral-700 text-white px-4 py-2 rounded font-bold transition-colors flex items-center gap-2 text-sm"
        >
          <RefreshCw size={16} /> DETECT ALL
        </button>
      </header>

      <div className="space-y-10 pb-12">
        {Object.entries(groupedTools).sort(([a], [b]) => a.localeCompare(b)).map(([category, catTools]) => (
          <div key={category}>
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2 border-b border-neutral-800 pb-2">
              <span className="text-blue-500">/</span> {category.toUpperCase()}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {(catTools as ToolDefinition[]).map(tool => (
                <div key={tool.id} className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 flex flex-col">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-white flex items-center gap-2">
                        {tool.name}
                        <span className="text-xs bg-neutral-800 px-2 py-0.5 rounded text-neutral-400 font-mono font-normal">
                          {tool.version || 'UNKNOWN VER'}
                        </span>
                      </h3>
                      <p className="text-sm text-neutral-400 mt-1">{tool.description}</p>
                    </div>
                    <StatusBadge status={tool.installationStatus} />
                  </div>

                  <div className="flex-1 text-sm font-mono text-neutral-500 mb-6 space-y-1">
                    <div><span className="text-neutral-600">INTEGRATION:</span> {tool.integrationType}</div>
                    <div><span className="text-neutral-600">LICENSE:</span> {tool.license}</div>
                  </div>

                  <div className="flex flex-wrap gap-2 pt-4 border-t border-neutral-800 mt-auto">
                    {tool.installationStatus !== 'NOT_IMPLEMENTED' && (
                      <button 
                        onClick={() => handleDetect(tool.id)}
                        className="bg-neutral-800 hover:bg-neutral-700 text-white px-3 py-1.5 rounded text-xs font-bold transition-colors flex items-center gap-1"
                      >
                        <RefreshCw size={14} /> DETECT
                      </button>
                    )}
                    {tool.capabilities.canLaunch && tool.installationStatus === 'INSTALLED' && (
                      <button className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded text-xs font-bold transition-colors flex items-center gap-1">
                        <Play size={14} /> LAUNCH
                      </button>
                    )}
                    <button className="bg-neutral-950 hover:bg-neutral-900 border border-neutral-800 text-neutral-400 px-3 py-1.5 rounded text-xs font-bold transition-colors flex items-center gap-1 ml-auto">
                      <Settings size={14} /> CONFIGURE
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
