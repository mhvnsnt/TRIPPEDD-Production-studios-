const fs = require('fs');
let content = fs.readFileSync('src/components/StudioOpsWorkspace.tsx', 'utf8');

// 1. Add "Templates" to tab state
content = content.replace(
  "const [activeTab, setActiveTab] = useState<'dashboard' | 'productions' | 'people' | 'work' | 'history'>('dashboard');",
  "const [activeTab, setActiveTab] = useState<'dashboard' | 'productions' | 'people' | 'work' | 'history' | 'templates'>('dashboard');"
);

// 2. Add button
const oldTabButtons = `<button onClick={() => setActiveTab('history')} className={\`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors \${activeTab === 'history' ? 'border-purple-500 text-purple-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}\`}>
          History
        </button>`;
const newTabButtons = oldTabButtons + `
        <button onClick={() => setActiveTab('templates')} className={\`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors \${activeTab === 'templates' ? 'border-purple-500 text-purple-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}\`}>
          Templates
        </button>`;
content = content.replace(oldTabButtons, newTabButtons);

// 3. Add templates content
const templatesContent = `
          {activeTab === 'templates' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center border-b border-neutral-800 pb-4">
                <h2 className="text-xl font-bold text-white tracking-widest uppercase">Production Templates</h2>
                <button className="bg-neutral-800 hover:bg-neutral-700 text-white px-3 py-1.5 rounded text-xs font-bold uppercase tracking-wider transition-colors">
                  + New Template
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Array.from(graph.productionTemplates.values()).map(t => {
                  const pt = graph.productionTypes.get(t.productionTypeId);
                  return (
                    <div key={t.id} className="bg-neutral-900 border border-neutral-800 p-4 rounded-lg flex flex-col">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="text-lg font-bold text-white">{t.name} <span className="text-xs text-neutral-500 font-mono ml-2">v{t.version}</span></h3>
                          <div className="text-[10px] text-blue-400 font-mono uppercase bg-blue-900/20 px-2 py-0.5 rounded inline-block mt-1">{pt?.name || 'Unknown Type'}</div>
                        </div>
                        <button className="text-neutral-500 hover:text-white transition-colors" title="Duplicate (New Version)">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        </button>
                      </div>
                      <p className="text-sm text-neutral-400 mb-4">{t.description}</p>
                      <div className="mt-auto space-y-3">
                        <div>
                          <div className="text-[10px] text-neutral-500 font-bold uppercase tracking-wider mb-1">Phases</div>
                          <div className="flex flex-wrap gap-1">
                            {t.phases.map(p => <span key={p} className="text-[9px] bg-neutral-950 border border-neutral-800 text-neutral-400 px-1.5 py-0.5 rounded font-mono">{p}</span>)}
                          </div>
                        </div>
                        <div>
                          <div className="text-[10px] text-neutral-500 font-bold uppercase tracking-wider mb-1">Default Requirements</div>
                          <div className="flex flex-wrap gap-1">
                            {t.requirements.map(r => <span key={r.id} className="text-[9px] bg-purple-950/30 border border-purple-900/50 text-purple-400 px-1.5 py-0.5 rounded font-mono">{r.name}</span>)}
                          </div>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )}
`;

content = content.replace("{activeTab === 'history' && (", templatesContent + "\n          {activeTab === 'history' && (");

// 4. Update the dependency chain display in 'productions' tab
const oldBlockerDisplay = `<div className="mt-2 text-xs text-red-400 bg-red-950/30 p-2 rounded border border-red-900/50">
                                <span className="font-bold">BLOCKED BY:</span> {blockers.map(b => b.description).join(', ')}
                              </div>`;

const newBlockerDisplay = `
                              <div className="mt-2 text-xs text-red-400 bg-red-950/30 p-3 rounded border border-red-900/50 flex flex-col gap-2">
                                <div className="font-bold">BLOCKED:</div>
                                <div className="text-red-300">{graph.getDependencyChain(p.id).message}</div>
                              </div>`;
content = content.replace(oldBlockerDisplay, newBlockerDisplay);


// 5. Update the Productions List to show the Template Name
const templateNameDisplay = `
                              <div className="text-[10px] font-mono text-neutral-500 mt-1">
                                TEMPLATE: {graph.productionTemplates.get(p.templateId || '')?.name || 'Legacy / None'}
                              </div>`;
content = content.replace('<div className="font-bold text-white mb-1">{p.name}</div>', '<div className="font-bold text-white mb-1">{p.name}</div>' + templateNameDisplay);


fs.writeFileSync('src/components/StudioOpsWorkspace.tsx', content);
console.log("StudioOps updated.");
