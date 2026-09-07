import React, { useState, useEffect } from 'react';
import { ProductionGraph } from '../core/pipeline/productionGraph';
import { 
  CreativeDiscovery, 
  DevelopmentSeed, 
  CreativeDocument, 
  DocumentVersion,
  DiscoveryStatus,
  SeedStatus
} from '../core/types';
import { Plus, Search, FileText, ChevronRight, Lightbulb, PlayCircle, Clock, Save, FileEdit, Trash } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export function StoryWorkspace() {
  const [activeTab, setActiveTab] = useState<'inbox' | 'active' | 'writers' | 'pitch' | 'greenlit' | 'lineage'>('inbox');
  const [graph] = useState(() => ProductionGraph.getInstance());
  
  const [discoveries, setDiscoveries] = useState<CreativeDiscovery[]>([]);
  const [seeds, setSeeds] = useState<DevelopmentSeed[]>([]);
  const [documents, setDocuments] = useState<CreativeDocument[]>([]);
  
  const [selectedDiscovery, setSelectedDiscovery] = useState<CreativeDiscovery | null>(null);
  const [selectedSeed, setSelectedSeed] = useState<DevelopmentSeed | null>(null);
  const [selectedDoc, setSelectedDoc] = useState<CreativeDocument | null>(null);
  const [docContent, setDocContent] = useState('');

  // Auto-seed for development
  useEffect(() => {
    if (graph.discoveries.size === 0) {
      const d1: CreativeDiscovery = {
        id: 'disc_1', title: 'Absurd survival-TV seriousness', 
        premise: 'Reality show takes trivial things completely seriously.',
        description: 'Reference: Naked and Afraid. They act like incompetent survival behavior is life or death.',
        status: 'CAPTURED', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
        sourceRefs: ['clip_naf_1'], evidenceRefs: [], tags: ['PARODY', 'SURVIVAL']
      };
      const d2: CreativeDiscovery = {
        id: 'disc_2', title: 'Unnecessarily difficult raft behavior', 
        premise: 'Contestants struggling with a raft in shallow water.',
        description: 'They push a raft but it is just walking in the water. Reference: Shipwrecked S1E5.',
        status: 'CAPTURED', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
        sourceRefs: ['clip_naf_1'], evidenceRefs: [], tags: ['PARODY']
      };
      const d3: CreativeDiscovery = {
        id: 'disc_3', title: 'Pig-catcher contrast', 
        premise: 'Heroic old imagery vs unimpressive present day.',
        description: 'Dude used to look like Tarzan catching pigs. Now he looks normal and can not catch anything.',
        status: 'CAPTURED', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
        sourceRefs: ['clip_naf_2'], evidenceRefs: [], tags: ['CHARACTER']
      };
      
      graph.addDiscovery(d1);
      graph.addDiscovery(d2);
      graph.addDiscovery(d3);

      const s1: DevelopmentSeed = {
        id: 'seed_1', discoveryId: 'disc_1', title: 'Clothed and Confused',
        logline: 'A fictional survival reality show takes trivial problems completely seriously.',
        premise: 'Parody of Naked and Afraid: Shipwrecked S1E5. Fictional characters deal with absurd non-issues.',
        format: 'PARODY_DOCUMENTARY', targetProductionType: 'GENERATED_MEDIA',
        characters: ['Heroic Loser', 'Panicked Survivor'], setting: 'Fictional Jungle', tone: 'Absurdist / Deadpan',
        referenceRefs: ['Naked and Afraid: Shipwrecked S1E5, "Smoke Signals and Fire Fights"'], sourceEvidenceRefs: [],
        status: 'IDEA', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
      };
      
      graph.addSeed(s1);

      const doc1: CreativeDocument = {
        id: 'doc_1', seedId: 'seed_1', title: 'Clothed and Confused - Pilot Outline',
        type: 'OUTLINE', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
      };
      graph.addDocument(doc1);

      graph.addDocumentVersion({
        id: 'ver_1', documentId: 'doc_1', versionNumber: 1, 
        createdAt: new Date().toISOString(), content: 'Act 1: They arrive clothed. They panic over a puddle.',
        status: 'DRAFT'
      });
    }
    
    refreshData();
  }, [graph]);

  const refreshData = () => {
    setDiscoveries(Array.from(graph.discoveries.values()).sort((a: any, b: any) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()));
    setSeeds(Array.from(graph.seeds.values()).sort((a: any, b: any) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()));
    setDocuments(Array.from(graph.documents.values()).sort((a: any, b: any) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()));
  };

  const handleCreateSeed = (discovery: CreativeDiscovery) => {
    const seed: DevelopmentSeed = {
      id: `seed_\${Date.now()}`, discoveryId: discovery.id, title: discovery.title,
      logline: '', premise: discovery.premise, format: '', targetProductionType: 'SKETCH',
      characters: [], setting: '', tone: '', referenceRefs: discovery.sourceRefs, sourceEvidenceRefs: [],
      status: 'IDEA', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString()
    };
    graph.addSeed(seed);
    graph.updateDiscoveryStatus(discovery.id, 'CONVERTED');
    refreshData();
  };

  const handleGreenlight = (seed: DevelopmentSeed) => {
    graph.greenlightSeed(seed.id);
    refreshData();
    alert('Seed converted to Production Unit successfully.');
  };

  const handleSaveVersion = (doc: CreativeDocument) => {
    const versions = graph.getVersionsForDocument(doc.id);
    const newVerNum = versions.length > 0 ? versions[0].versionNumber + 1 : 1;
    graph.addDocumentVersion({
      id: `ver_\${Date.now()}`, documentId: doc.id, versionNumber: newVerNum,
      createdAt: new Date().toISOString(), content: docContent, status: 'DRAFT'
    });
    refreshData();
    alert(`Version \${newVerNum} saved.`);
  };

  const loadDoc = (doc: CreativeDocument) => {
    setSelectedDoc(doc);
    const versions = graph.getVersionsForDocument(doc.id);
    setDocContent(versions.length > 0 ? versions[0].content : '');
  };

  return (
    <div className="flex h-full w-full bg-black text-white">
      {/* Sidebar */}
      <div className="w-64 border-r border-neutral-800 bg-neutral-900/50 flex flex-col h-full shrink-0">
        <div className="p-4 border-b border-neutral-800">
          <h2 className="font-black text-white tracking-widest text-sm uppercase">Development</h2>
        </div>
        <div className="overflow-y-auto p-2 space-y-1">
          {[
            { id: 'inbox', label: 'Discovery Inbox', icon: Lightbulb },
            { id: 'active', label: 'Active Seeds', icon: Clock },
            { id: 'writers', label: 'Writers Room', icon: FileEdit },
            { id: 'pitch', label: 'Pitch Queue', icon: PlayCircle },
            { id: 'greenlit', label: 'Greenlit', icon: Save },
            { id: 'lineage', label: 'Source Lineage', icon: ChevronRight },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => { setActiveTab(tab.id as any); setSelectedDiscovery(null); setSelectedSeed(null); setSelectedDoc(null); }}
              className={`w-full text-left p-3 rounded-lg flex items-center gap-3 transition-colors \${
                activeTab === tab.id 
                  ? 'bg-blue-600/10 border-blue-500/30 border text-blue-400' 
                  : 'hover:bg-neutral-800 border border-transparent text-neutral-400'
              }`}
            >
              <tab.icon size={16} />
              <span className="text-sm font-bold uppercase tracking-wider">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Area */}
      <div className="flex-1 flex flex-col overflow-hidden bg-neutral-950 p-6">
        
        {activeTab === 'inbox' && (
          <div className="space-y-4 max-w-4xl">
            <h2 className="text-xl font-bold mb-6 border-b border-neutral-800 pb-2">DISCOVERY INBOX</h2>
            {discoveries.filter(d => d.status === 'CAPTURED').map(d => (
              <div key={d.id} className="bg-neutral-900 border border-neutral-800 p-4 rounded-lg">
                <div className="flex justify-between items-start">
                  <h3 className="text-lg font-bold text-white">{d.title}</h3>
                  <button onClick={() => handleCreateSeed(d)} className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 text-xs rounded uppercase font-bold tracking-wider">
                    Convert to Seed
                  </button>
                </div>
                <p className="text-sm text-neutral-400 mt-2">{d.premise}</p>
                <div className="mt-3 flex gap-2">
                  {d.tags.map(t => <span key={t} className="text-[10px] bg-neutral-800 text-neutral-400 px-2 py-0.5 rounded uppercase font-mono">{t}</span>)}
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'active' && (
          <div className="space-y-4 max-w-4xl">
            <h2 className="text-xl font-bold mb-6 border-b border-neutral-800 pb-2">ACTIVE DEVELOPMENT SEEDS</h2>
            {seeds.filter(s => s.status === 'IDEA' || s.status === 'DEVELOPING').map(s => (
              <div key={s.id} className="bg-neutral-900 border border-neutral-800 p-4 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-[10px] text-blue-400 font-mono border border-blue-900 bg-blue-900/20 px-2 py-0.5 rounded mr-2">{s.targetProductionType}</span>
                    <span className="text-[10px] text-neutral-500 font-mono uppercase">{s.status}</span>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => { graph.updateSeedStatus(s.id, 'PITCHABLE'); refreshData(); }} className="bg-emerald-900/50 hover:bg-emerald-900 text-emerald-400 border border-emerald-800 px-3 py-1 text-xs rounded uppercase font-bold">
                      Mark Pitchable
                    </button>
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white mt-2 mb-1">{s.title}</h3>
                <p className="text-sm text-neutral-300 italic mb-3">"{s.logline || s.premise}"</p>
                {s.referenceRefs.length > 0 && (
                  <div className="text-xs text-neutral-500 font-mono bg-black p-2 rounded">
                    REFS: {s.referenceRefs.join(', ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {activeTab === 'writers' && (
          <div className="flex h-full gap-4">
            <div className="w-1/3 flex flex-col space-y-2 overflow-y-auto">
              <h2 className="text-sm font-bold mb-2 uppercase text-neutral-500 tracking-widest">Documents</h2>
              {documents.map(d => (
                <button 
                  key={d.id} 
                  onClick={() => loadDoc(d)}
                  className={`text-left p-3 rounded border transition-colors \${selectedDoc?.id === d.id ? 'bg-neutral-800 border-neutral-600' : 'bg-neutral-900 border-neutral-800 hover:border-neutral-700'}`}
                >
                  <div className="text-[10px] text-purple-400 font-mono mb-1">{d.type}</div>
                  <div className="text-sm font-bold text-white truncate">{d.title}</div>
                  <div className="text-xs text-neutral-500 mt-1">Updated {formatDistanceToNow(new Date(d.updatedAt))} ago</div>
                </button>
              ))}
            </div>
            <div className="flex-1 bg-neutral-900 border border-neutral-800 rounded-lg p-4 flex flex-col">
              {selectedDoc ? (
                <>
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg font-bold">{selectedDoc.title}</h3>
                    <div className="flex gap-2">
                      <span className="text-xs font-mono bg-neutral-800 text-neutral-400 px-2 py-1 rounded">
                        v{graph.getVersionsForDocument(selectedDoc.id).length > 0 ? graph.getVersionsForDocument(selectedDoc.id)[0].versionNumber : 0}
                      </span>
                      <button onClick={() => handleSaveVersion(selectedDoc)} className="bg-blue-600 hover:bg-blue-500 px-3 py-1 text-xs rounded text-white font-bold uppercase">Save New Version</button>
                    </div>
                  </div>
                  <textarea 
                    value={docContent}
                    onChange={(e) => setDocContent(e.target.value)}
                    className="flex-1 w-full bg-black border border-neutral-800 rounded p-4 text-sm text-neutral-300 font-mono focus:outline-none focus:border-neutral-600 resize-none"
                    placeholder="Start writing..."
                  />
                  <div className="mt-4 border-t border-neutral-800 pt-4">
                    <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-widest mb-2">Version History</h4>
                    <div className="flex gap-2 overflow-x-auto">
                      {graph.getVersionsForDocument(selectedDoc.id).map(v => (
                        <div key={v.id} className="bg-neutral-950 border border-neutral-800 p-2 rounded min-w-[150px] shrink-0 cursor-pointer hover:border-neutral-700" onClick={() => setDocContent(v.content)}>
                          <div className="text-xs font-bold">Version {v.versionNumber}</div>
                          <div className="text-[10px] text-neutral-500 font-mono mt-1">{formatDistanceToNow(new Date(v.createdAt))} ago</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="flex-1 flex items-center justify-center text-neutral-500 font-mono text-xs">Select a document to edit</div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'pitch' && (
          <div className="space-y-4 max-w-4xl">
            <h2 className="text-xl font-bold mb-6 border-b border-neutral-800 pb-2">PITCH QUEUE</h2>
            {seeds.filter(s => s.status === 'PITCHABLE').map(s => (
              <div key={s.id} className="bg-gradient-to-r from-neutral-900 to-neutral-800 border border-neutral-700 p-5 rounded-xl shadow-lg">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-2xl font-black text-white uppercase tracking-wider">{s.title}</h3>
                  <button onClick={() => handleGreenlight(s)} className="bg-green-600 hover:bg-green-500 text-white px-4 py-2 text-xs rounded uppercase font-bold tracking-widest shadow-lg shadow-green-900/50">
                    Greenlight
                  </button>
                </div>
                <div className="bg-black/50 p-4 rounded border border-neutral-800 mb-4">
                  <p className="text-sm text-neutral-300 font-serif text-lg italic">"{s.logline || s.premise}"</p>
                </div>
                <div className="grid grid-cols-2 gap-4 text-xs font-mono text-neutral-400">
                  <div>FORMAT: <span className="text-white">{s.format}</span></div>
                  <div>TONE: <span className="text-white">{s.tone}</span></div>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'greenlit' && (
          <div className="space-y-4 max-w-4xl">
            <h2 className="text-xl font-bold mb-6 border-b border-neutral-800 pb-2">GREENLIT PRODUCTIONS</h2>
            {seeds.filter(s => s.status === 'GREENLIT').map(s => {
              const rels = graph.getRelationshipsFor(s.id, 'DEVELOPMENT_SEED');
              const puRel = graph.relationships.values().toArray().find(r => r.targetId === s.id && r.relationshipType === 'PRODUCTION_CREATED_FROM_SEED');
              const pu = puRel ? graph.productionUnits.get(puRel.sourceId) : null;
              
              return (
                <div key={s.id} className="bg-neutral-900 border border-green-900/50 p-4 rounded-lg">
                  <h3 className="text-lg font-bold text-white mb-2">{s.title}</h3>
                  {pu && (
                    <div className="flex items-center gap-2 mt-2 bg-green-950/30 text-green-400 p-2 rounded text-xs font-mono border border-green-900/30">
                      <ChevronRight size={14} /> Production Unit: {pu.id} ({pu.status})
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}

        {activeTab === 'lineage' && (
          <div className="space-y-6 max-w-4xl">
            <h2 className="text-xl font-bold mb-6 border-b border-neutral-800 pb-2">SOURCE LINEAGE</h2>
            {seeds.map(s => {
              const discRel = graph.relationships.values().toArray().find(r => r.sourceId === s.id && r.relationshipType === 'DEVELOPMENT_SEED_FROM_DISCOVERY');
              const disc = discRel ? graph.discoveries.get(discRel.targetId) : null;
              const puRel = graph.relationships.values().toArray().find(r => r.targetId === s.id && r.relationshipType === 'PRODUCTION_CREATED_FROM_SEED');
              
              return (
                <div key={s.id} className="flex items-center gap-4 text-sm font-mono">
                  {disc && (
                    <>
                      <div className="bg-neutral-900 p-3 rounded border border-neutral-800 flex-1">
                        <div className="text-[10px] text-neutral-500 mb-1">DISCOVERY</div>
                        <div className="text-white truncate">{disc.title}</div>
                      </div>
                      <ChevronRight size={16} className="text-neutral-600 shrink-0" />
                    </>
                  )}
                  <div className="bg-blue-900/20 p-3 rounded border border-blue-900/50 flex-1">
                    <div className="text-[10px] text-blue-500 mb-1">SEED</div>
                    <div className="text-blue-100 truncate">{s.title}</div>
                  </div>
                  {puRel && (
                    <>
                      <ChevronRight size={16} className="text-green-600 shrink-0" />
                      <div className="bg-green-900/20 p-3 rounded border border-green-900/50 flex-1">
                        <div className="text-[10px] text-green-500 mb-1">PRODUCTION</div>
                        <div className="text-green-100 truncate">{puRel.sourceId}</div>
                      </div>
                    </>
                  )}
                </div>
              )
            })}
          </div>
        )}

      </div>
    </div>
  );
}
