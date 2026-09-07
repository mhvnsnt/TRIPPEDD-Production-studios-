const fs = require('fs');
let content = fs.readFileSync('src/components/StudioOpsWorkspace.tsx', 'utf8');

// 1. Add History Tab & Filter State
content = content.replace(
  "const [activeTab, setActiveTab] = useState<'dashboard' | 'productions' | 'people' | 'work'>('dashboard');",
  "const [activeTab, setActiveTab] = useState<'dashboard' | 'productions' | 'people' | 'work' | 'history'>('dashboard');\n  const [historyFilter, setHistoryFilter] = useState({ unitId: '', type: '', source: '' });\n  const [expandedBlocker, setExpandedBlocker] = useState<string | null>(null);"
);

// 2. Add History Tab Button
content = content.replace(
  "        <div className=\"flex space-x-2\">\n          {['dashboard', 'productions', 'people', 'work'].map(tab => (",
  "        <div className=\"flex space-x-2\">\n          {['dashboard', 'productions', 'people', 'work', 'history'].map(tab => ("
);

// 3. Add formatTime function if not present
if (!content.includes('formatTime(')) {
  content = content.replace(
    "export function StudioOpsWorkspace() {",
    "export function StudioOpsWorkspace() {\n  const formatTime = (ts: string) => {\n    const d = new Date(ts);\n    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + '.' + d.getMilliseconds().toString().padStart(3, '0');\n  };"
  );
}

// 4. In the Dashboard Tab, rewrite the Blocker Feeds section to include expandable chains.
// Right now the dashboard blocker section looks like this:
/*
<div className="bg-black/50 border border-red-900/30 rounded-lg p-5">
  <h3 className="text-sm font-bold text-white mb-4 flex items-center">
    <AlertTriangle size={16} className="text-red-500 mr-2" />
    Active Blockers
  </h3>
  <div className="space-y-3">
    {blockedProductions.length > 0 ? blockedProductions.map(pu => {
      const blockers = graph.getBlockersForStage(pu.id, STAGE_ORDER[STAGE_ORDER.indexOf(pu.status) + 1] || pu.status);
      ...
*/

const blockerStartRegex = /<div className="bg-black\/50 border border-red-900\/30 rounded-lg p-5">/;
const blockerEndRegex = /<\/div>\s*<\/section>\s*<\/div>\s*<\/div>\s*\)\}/; // This might be hard to match. Let's be more precise.

// Instead of string replacement for the big chunk, let's just use string replace on specific parts.
const oldBlockerRender = `{blockedProductions.length > 0 ? blockedProductions.map(pu => {
                        const blockers = graph.getBlockersForStage(pu.id, STAGE_ORDER[STAGE_ORDER.indexOf(pu.status) + 1] || pu.status);
                        return (
                          <div key={pu.id} className="bg-neutral-900 border-l-2 border-red-500 rounded p-3">
                            <div className="flex justify-between items-start">
                              <div>
                                <span className="text-[10px] text-neutral-500 font-mono uppercase">{pu.type}</span>
                                <h4 className="text-sm font-bold text-white">{pu.name}</h4>
                              </div>
                              <span className="text-xs text-red-400 bg-red-950/30 px-2 py-0.5 rounded font-mono">
                                BLOCKED
                              </span>
                            </div>
                            <div className="mt-3 space-y-2">
                              {blockers.map(b => (
                                <div key={b.id} className="text-xs text-neutral-400 bg-black/50 p-2 rounded border border-neutral-800 flex items-start">
                                  <AlertTriangle size={12} className="text-yellow-500 mr-2 mt-0.5 shrink-0" />
                                  <span>{b.description} <span className="text-neutral-600 ml-1">({b.type})</span></span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )
                      }) : (`;

const newBlockerRender = `{blockedProductions.length > 0 ? blockedProductions.map(pu => {
                        const blockers = graph.getBlockersForStage(pu.id, STAGE_ORDER[STAGE_ORDER.indexOf(pu.status) + 1] || pu.status);
                        const isExpanded = expandedBlocker === pu.id;
                        const chain = isExpanded ? graph.getDependencyChain(pu.id) : [];
                        return (
                          <div key={pu.id} className="bg-neutral-900 border-l-2 border-red-500 rounded p-3">
                            <div className="flex justify-between items-start cursor-pointer" onClick={() => setExpandedBlocker(isExpanded ? null : pu.id)}>
                              <div>
                                <span className="text-[10px] text-neutral-500 font-mono uppercase">{pu.type}</span>
                                <h4 className="text-sm font-bold text-white">{pu.name}</h4>
                              </div>
                              <div className="flex items-center">
                                <span className="text-xs text-red-400 bg-red-950/30 px-2 py-0.5 rounded font-mono mr-2">
                                  BLOCKED
                                </span>
                                <ChevronRight size={16} className={\`text-neutral-500 transition-transform \${isExpanded ? 'rotate-90' : ''}\`} />
                              </div>
                            </div>
                            
                            {!isExpanded && (
                              <div className="mt-3 space-y-2">
                                {blockers.map(b => (
                                  <div key={b.id} className="text-xs text-neutral-400 bg-black/50 p-2 rounded border border-neutral-800 flex items-start">
                                    <AlertTriangle size={12} className="text-yellow-500 mr-2 mt-0.5 shrink-0" />
                                    <span>{b.description} <span className="text-neutral-600 ml-1">({b.type})</span></span>
                                  </div>
                                ))}
                              </div>
                            )}

                            {isExpanded && (
                              <div className="mt-4 pt-3 border-t border-neutral-800">
                                <h5 className="text-[10px] uppercase tracking-widest text-neutral-500 mb-3">Dependency Chain</h5>
                                <div className="space-y-3 pl-2 border-l border-neutral-800/50">
                                  {chain.map((node: any, idx: number) => (
                                    <div key={idx} className="relative">
                                      <div className="absolute -left-[13px] top-1.5 w-2 h-2 rounded-full bg-neutral-700 border border-neutral-900" />
                                      <div className="pl-4">
                                        <div className="text-[10px] font-bold text-purple-400 uppercase">{node.type.replace(/_/g, ' ')}</div>
                                        <div className="text-sm text-white">{node.name}</div>
                                        {node.description && <div className="text-xs text-neutral-400 mt-1">{node.description}</div>}
                                        {node.status && (
                                          <div className="inline-block mt-1 px-1.5 py-0.5 bg-black border border-neutral-800 rounded text-[9px] text-neutral-500 font-mono">
                                            {node.status}
                                          </div>
                                        )}
                                        {node.type === 'EVENTS' && node.details && node.details.length > 0 && (
                                          <div className="mt-2 space-y-1 bg-black/30 p-2 rounded border border-neutral-800/50">
                                            {node.details.map((e: any) => (
                                              <div key={e.id} className="text-[10px] text-neutral-500 font-mono">
                                                [{formatTime(e.timestamp)}] {e.description}
                                              </div>
                                            ))}
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              </div>
                            )}
                          </div>
                        )
                      }) : (`;

content = content.replace(oldBlockerRender, newBlockerRender);

// 5. Add History Tab content at the end of the file before the final </div></div></div>
const historyTab = `
          {activeTab === 'history' && (
            <div className="space-y-4 h-full flex flex-col">
              <div className="flex space-x-4 mb-2">
                <select 
                  className="bg-neutral-900 border border-neutral-800 rounded text-xs text-white p-2"
                  value={historyFilter.unitId}
                  onChange={e => setHistoryFilter({...historyFilter, unitId: e.target.value})}
                >
                  <option value="">All Productions</option>
                  {productions.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
                <select 
                  className="bg-neutral-900 border border-neutral-800 rounded text-xs text-white p-2"
                  value={historyFilter.source}
                  onChange={e => setHistoryFilter({...historyFilter, source: e.target.value})}
                >
                  <option value="">All Sources</option>
                  <option value="SYSTEM">System</option>
                  <option value="HUMAN">Human</option>
                  <option value="MEDIA_ANALYSIS">Media Analysis</option>
                </select>
                <select 
                  className="bg-neutral-900 border border-neutral-800 rounded text-xs text-white p-2"
                  value={historyFilter.type}
                  onChange={e => setHistoryFilter({...historyFilter, type: e.target.value})}
                >
                  <option value="">All Event Types</option>
                  {Array.from(new Set(events.map(e => e.type))).map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>

              <div className="flex-1 overflow-y-auto bg-neutral-900/50 border border-neutral-800 rounded-lg p-4 custom-scrollbar">
                <div className="space-y-1">
                  {events
                    .filter(e => !historyFilter.unitId || e.productionUnitId === historyFilter.unitId)
                    .filter(e => !historyFilter.source || e.source === historyFilter.source)
                    .filter(e => !historyFilter.type || e.type === historyFilter.type)
                    .map(event => (
                    <div key={event.id} className="flex text-xs py-2 border-b border-neutral-800/50 hover:bg-neutral-800/30 transition-colors">
                      <div className="w-24 shrink-0 text-neutral-500 font-mono">
                        {formatTime(event.timestamp)}
                      </div>
                      <div className="w-24 shrink-0">
                        <span className={\`text-[9px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded \${
                          event.source === 'SYSTEM' ? 'bg-blue-900/30 text-blue-400' :
                          event.source === 'HUMAN' ? 'bg-purple-900/30 text-purple-400' :
                          'bg-green-900/30 text-green-400'
                        }\`}>
                          {event.source || 'UNKNOWN'}
                        </span>
                      </div>
                      <div className="w-32 shrink-0">
                        <span className="text-[9px] text-neutral-400 font-mono">{event.type}</span>
                      </div>
                      <div className="flex-1 text-neutral-300">
                        {event.description}
                      </div>
                    </div>
                  ))}
                  {events.length === 0 && (
                    <div className="text-center p-8 text-neutral-500 font-mono text-xs">
                      No events recorded.
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
`;

content = content.replace("        </div>\n      </div>\n    </div>\n  );\n}", historyTab + "        </div>\n      </div>\n    </div>\n  );\n}");

fs.writeFileSync('src/components/StudioOpsWorkspace.tsx', content);
