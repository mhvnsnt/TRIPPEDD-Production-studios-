import React, { useState, useEffect, useMemo } from 'react';
import { Archive, Database, FileImage, FileVideo, FileAudio, FileText, CheckCircle, Search, Filter, Info, ChevronRight, Hash } from 'lucide-react';
import { Asset, AggregateClassification } from '../core/types';
import { AssetRegistry } from '../core/assets/registry';

export const AssetWorkspace = () => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterProvenance, setFilterProvenance] = useState<AggregateClassification | 'ALL'>('ALL');
  const [viewMode, setViewMode] = useState<'GRID' | 'LIST'>('LIST');

  useEffect(() => {
    return AssetRegistry.subscribe((newAssets) => {
      setAssets(newAssets);
    });
  }, []);

  const selectedAsset = useMemo(() => assets.find(a => a.id === selectedAssetId), [assets, selectedAssetId]);

  const filteredAssets = useMemo(() => {
    return assets.filter(asset => {
      const matchesSearch = asset.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            asset.id.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesProv = filterProvenance === 'ALL' || asset.provenance.aggregate.aggregate === filterProvenance;
      return matchesSearch && matchesProv;
    });
  }, [assets, searchQuery, filterProvenance]);

  const getIconForType = (type: string) => {
    switch (type) {
      case 'video': return <FileVideo size={16} className="text-purple-400" />;
      case 'image': return <FileImage size={16} className="text-blue-400" />;
      case 'audio': return <FileAudio size={16} className="text-emerald-400" />;
      default: return <FileText size={16} className="text-neutral-400" />;
    }
  };

  const getProvenanceColor = (prov: string) => {
    switch (prov) {
      case 'REAL_PRODUCTION': return 'text-amber-400 bg-amber-400/10 border-amber-400/20';
      case 'FICTIONAL_CREATION': return 'text-purple-400 bg-purple-400/10 border-purple-400/20';
      case 'HYBRID_PRODUCTION': return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
      case 'IDEA': 
      case 'PLAN': return 'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';
      case 'REFERENCE': return 'text-neutral-400 bg-neutral-400/10 border-neutral-400/20';
      default: return 'text-neutral-400 bg-neutral-800 border-neutral-700';
    }
  };

  return (
    <div className="flex h-full bg-neutral-950 text-neutral-300">
      {/* Left: Asset List/Grid */}
      <div className="flex-1 flex flex-col border-r border-neutral-800">
        <header className="p-6 border-b border-neutral-800 flex justify-between items-end bg-neutral-900/50">
          <div>
            <h1 className="text-3xl font-black text-white flex items-center gap-3 tracking-tight">
              <Database className="text-blue-500" size={28} />
              ASSET REGISTRY
            </h1>
            <p className="text-neutral-400 mt-1">Canonical media inventory and provenance tracker.</p>
          </div>
          
          <div className="flex gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-500" size={16} />
              <input 
                type="text" 
                placeholder="Search assets..." 
                className="bg-neutral-900 border border-neutral-700 rounded pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500 w-64"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <select 
              className="bg-neutral-900 border border-neutral-700 rounded px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              value={filterProvenance}
              onChange={(e) => setFilterProvenance(e.target.value as any)}
            >
              <option value="ALL">All Provenance</option>
              <option value="REAL_PRODUCTION">Real Production</option>
              <option value="FICTIONAL_CREATION">Fictional Creation</option>
              <option value="HYBRID_PRODUCTION">Hybrid</option>
              <option value="REFERENCE">Reference</option>
            </select>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6">
          <div className="space-y-2">
            {filteredAssets.length === 0 ? (
              <div className="text-center text-neutral-600 mt-20">
                <Database size={48} className="mx-auto mb-4 opacity-20" />
                <p>No assets found.</p>
              </div>
            ) : (
              filteredAssets.map(asset => (
                <div 
                  key={asset.id} 
                  onClick={() => setSelectedAssetId(asset.id)}
                  className={`flex items-center p-3 rounded cursor-pointer border transition-colors ${selectedAssetId === asset.id ? 'bg-blue-900/20 border-blue-500/50' : 'bg-neutral-900 border-neutral-800 hover:bg-neutral-800 hover:border-neutral-700'}`}
                >
                  <div className="w-10 h-10 bg-neutral-950 rounded flex items-center justify-center border border-neutral-800 mr-4 shrink-0">
                    {getIconForType(asset.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-white font-medium truncate">{asset.name}</span>
                      <span className="text-xs font-mono bg-neutral-800 px-1.5 py-0.5 rounded text-neutral-400 shrink-0">
                        v{asset.version.toString().padStart(3, '0')}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getProvenanceColor(asset.provenance.aggregate)} shrink-0 uppercase tracking-wider`}>
                        {asset.provenance.aggregate.replace('_', ' ')}
                      </span>
                    </div>
                    <div className="flex text-xs text-neutral-500 gap-4 font-mono truncate">
                      <span className="flex items-center gap-1"><Hash size={12} /> {asset.id}</span>
                      <span>{new Date(asset.createdAt).toLocaleString()}</span>
                      {asset.sourceTool && <span>TOOL: {asset.sourceTool.toUpperCase()}</span>}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Right: Asset Detail Panel */}
      <div className="w-[400px] bg-neutral-900 border-l border-neutral-800 overflow-y-auto flex flex-col">
        {selectedAsset ? (
          <div className="flex flex-col h-full">
            <div className="p-6 border-b border-neutral-800">
              <div className="flex justify-between items-start mb-4">
                <div className="w-16 h-16 bg-neutral-950 border border-neutral-800 rounded-lg flex items-center justify-center mb-4">
                  {getIconForType(selectedAsset.type)}
                </div>
                <div className={`text-xs font-bold px-3 py-1 rounded border uppercase tracking-wider ${getProvenanceColor(selectedAsset.provenance)}`}>
                  {selectedAsset.provenance.replace('_', ' ')}
                </div>
              </div>
              
              <h2 className="text-2xl font-bold text-white leading-tight break-words">{selectedAsset.name}</h2>
              <div className="text-sm font-mono text-neutral-500 mt-2 flex items-center gap-2">
                <Hash size={14} /> {selectedAsset.id}
              </div>
            </div>

            <div className="p-6 space-y-6 flex-1">
              {/* Media Preview Simulation */}
              <div className="aspect-video bg-neutral-950 border border-neutral-800 rounded-lg flex flex-col items-center justify-center text-neutral-600 relative overflow-hidden group">
                {getIconForType(selectedAsset.type)}
                <span className="text-xs font-mono mt-2 uppercase tracking-widest">{selectedAsset.type} PREVIEW</span>
                <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center backdrop-blur-sm">
                  <span className="text-white text-sm font-bold tracking-wider">VIEW SOURCE</span>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <h4 className="text-xs font-bold text-neutral-500 mb-2 uppercase tracking-wider flex items-center gap-2"><Archive size={14} /> Core Metadata</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="bg-neutral-950 p-2 rounded border border-neutral-800">
                      <span className="text-neutral-500 block text-[10px] mb-1">FORMAT</span>
                      <span className="text-white font-mono">{selectedAsset.fileFormat?.toUpperCase() || 'UNKNOWN'}</span>
                    </div>
                    <div className="bg-neutral-950 p-2 rounded border border-neutral-800">
                      <span className="text-neutral-500 block text-[10px] mb-1">CONTENT TYPE</span>
                      <span className="text-white font-mono">{selectedAsset.contentType.toUpperCase()}</span>
                    </div>
                    <div className="bg-neutral-950 p-2 rounded border border-neutral-800">
                      <span className="text-neutral-500 block text-[10px] mb-1">VERIFICATION</span>
                      <span className="text-white flex items-center gap-1">
                        {selectedAsset.verificationState === 'VERIFIED' && <CheckCircle size={12} className="text-emerald-500" />}
                        {selectedAsset.verificationState}
                      </span>
                    </div>
                    <div className="bg-neutral-950 p-2 rounded border border-neutral-800">
                      <span className="text-neutral-500 block text-[10px] mb-1">STATUS</span>
                      <span className="text-white">{selectedAsset.status}</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-neutral-500 mb-2 uppercase tracking-wider flex items-center gap-2"><Database size={14} /> Storage & Location</h4>
                  <div className="bg-neutral-950 p-3 rounded border border-neutral-800 text-xs font-mono text-neutral-400 break-all">
                    {selectedAsset.path}
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-neutral-500 mb-2 uppercase tracking-wider flex items-center gap-2"><Info size={14} /> Lineage & Context</h4>
                  <div className="bg-neutral-950 rounded border border-neutral-800 p-3 text-sm space-y-2 font-mono">
                    <div className="flex justify-between border-b border-neutral-800 pb-2">
                      <span className="text-neutral-500">Project</span>
                      <span className="text-white">{selectedAsset.projectId}</span>
                    </div>
                    {(selectedAsset.episodeId || selectedAsset.sceneId || selectedAsset.shotId) && (
                      <div className="flex justify-between border-b border-neutral-800 pb-2">
                        <span className="text-neutral-500">Placement</span>
                        <span className="text-blue-400 text-right">
                          {selectedAsset.episodeId && `${selectedAsset.episodeId} `}
                          {selectedAsset.sceneId && `/ ${selectedAsset.sceneId} `}
                          {selectedAsset.shotId && `/ ${selectedAsset.shotId}`}
                        </span>
                      </div>
                    )}
                    {selectedAsset.sourceTool && (
                      <div className="flex justify-between border-b border-neutral-800 pb-2">
                        <span className="text-neutral-500">Source Tool</span>
                        <span className="text-purple-400">{selectedAsset.sourceTool}</span>
                      </div>
                    )}
                    {selectedAsset.producingJobId && (
                      <div className="flex justify-between border-b border-neutral-800 pb-2">
                        <span className="text-neutral-500">Origin Job</span>
                        <span className="text-emerald-400">{selectedAsset.producingJobId}</span>
                      </div>
                    )}
                    {selectedAsset.parentAssets && selectedAsset.parentAssets.length > 0 && (
                      <div className="flex justify-between pt-1">
                        <span className="text-neutral-500">Parent Assets</span>
                        <span className="text-white text-right">
                          {selectedAsset.parentAssets.map(p => <div key={p}>{p}</div>)}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-neutral-600 p-8 text-center">
            <Database size={48} className="mb-4 opacity-20" />
            <p className="text-sm">Select an asset from the registry to inspect its metadata, location, and provenance.</p>
          </div>
        )}
      </div>
    </div>
  );
};
