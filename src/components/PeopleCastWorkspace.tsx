import React, { useState } from 'react';
import { ProductionGraph } from '../core/pipeline/productionGraph';
import { Person, Character, CastAssignment, Performance, Take, ProductionUnit } from '../core/types';

export const PeopleCastWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'people' | 'characters' | 'casting' | 'performances' | 'takes' | 'relationships'>('people');
  const graph = ProductionGraph.getInstance();

  const people = Array.from(graph.people.values());
  const characters = Array.from(graph.characters.values());
  const castAssignments = Array.from(graph.castAssignments.values());
  const performances = Array.from(graph.performances.values());
  const takes = Array.from(graph.takes.values());
  const productions = Array.from(graph.productionUnits.values());

  const getProductionName = (id: string) => productions.find(p => p.id === id)?.name || 'Unknown Production';
  const getPersonName = (id?: string) => people.find(p => p.id === id)?.name || 'Unknown Person';
  const getCharacterName = (id?: string) => characters.find(c => c.id === id)?.name || 'Unknown Character';

  return (
    <div className="h-full flex flex-col bg-black text-white p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-widest uppercase mb-1">People & Cast Workspace</h1>
          <p className="text-neutral-500 font-mono text-xs uppercase tracking-wider">
            Roster • Characters • Performances
          </p>
        </div>
      </div>

      <div className="flex-1 flex flex-col border border-neutral-800 rounded-lg overflow-hidden bg-neutral-950">
        <div className="flex border-b border-neutral-800 overflow-x-auto custom-scrollbar">
          {['people', 'characters', 'casting', 'performances', 'takes', 'relationships'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors whitespace-nowrap ${activeTab === tab ? 'border-purple-500 text-purple-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}`}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
          {activeTab === 'people' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center border-b border-neutral-800 pb-4 mb-4">
                <h2 className="text-lg font-bold uppercase tracking-widest text-neutral-300">Studio Roster</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {people.map(person => (
                  <div key={person.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-4">
                    <div className="flex items-center space-x-4 mb-4">
                      <div className="w-12 h-12 rounded-full bg-purple-900/30 border border-purple-800/50 flex items-center justify-center font-bold text-lg text-purple-400">
                        {person.name.charAt(0)}
                      </div>
                      <div>
                        <h3 className="font-bold text-white">{person.name}</h3>
                        <div className="text-xs text-neutral-500 font-mono">{person.status || 'ACTIVE'}</div>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="text-xs text-neutral-400">
                        <span className="font-bold text-neutral-600">ROLES:</span> {graph.getRolesForPerson(person.id).length}
                      </div>
                      <div className="text-xs text-neutral-400">
                        <span className="font-bold text-neutral-600">CAST:</span> {castAssignments.filter(c => c.personId === person.id).length}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'characters' && (
            <div className="space-y-4">
               <div className="flex justify-between items-center border-b border-neutral-800 pb-4 mb-4">
                <h2 className="text-lg font-bold uppercase tracking-widest text-neutral-300">Characters</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {characters.map(char => (
                  <div key={char.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-white">{char.name}</h3>
                      <span className="text-[10px] bg-blue-900/30 text-blue-400 px-2 py-0.5 rounded font-mono uppercase tracking-wider">{char.characterType}</span>
                    </div>
                    <div className="text-xs text-purple-400 mb-2 truncate">{getProductionName(char.productionUnitId)}</div>
                    <p className="text-sm text-neutral-400 line-clamp-2">{char.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'casting' && (
            <div className="space-y-4">
               <div className="flex justify-between items-center border-b border-neutral-800 pb-4 mb-4">
                <h2 className="text-lg font-bold uppercase tracking-widest text-neutral-300">Cast Assignments</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {castAssignments.map(ca => (
                  <div key={ca.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="text-[10px] text-neutral-500 font-bold uppercase tracking-wider mb-1">Character</div>
                        <h3 className="font-bold text-white">{getCharacterName(ca.characterId)}</h3>
                      </div>
                      <span className="text-[10px] bg-green-900/30 text-green-400 px-2 py-0.5 rounded font-mono uppercase tracking-wider">{ca.status}</span>
                    </div>
                    <div className="border-t border-neutral-800 pt-3 mt-3">
                       <div className="text-[10px] text-neutral-500 font-bold uppercase tracking-wider mb-1">Portrayed By</div>
                       <div className="text-sm text-purple-400">{getPersonName(ca.personId)}</div>
                    </div>
                  </div>
                ))}
                {castAssignments.length === 0 && (
                  <div className="col-span-full text-center py-12 text-neutral-500 font-mono text-sm border border-dashed border-neutral-800 rounded">
                    No cast assignments found.
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'performances' && (
            <div className="space-y-4">
               <div className="flex justify-between items-center border-b border-neutral-800 pb-4 mb-4">
                <h2 className="text-lg font-bold uppercase tracking-widest text-neutral-300">Performances</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {performances.map(perf => (
                  <div key={perf.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center space-x-2">
                        <span className={`text-[10px] px-2 py-0.5 rounded font-mono uppercase tracking-wider ${
                          perf.performerType === 'GENERATED' ? 'bg-orange-900/30 text-orange-400' : 'bg-blue-900/30 text-blue-400'
                        }`}>
                          {perf.performerType}
                        </span>
                        <span className="text-[10px] bg-neutral-800 text-neutral-400 px-2 py-0.5 rounded font-mono uppercase tracking-wider">{perf.status}</span>
                      </div>
                    </div>
                    <h3 className="font-bold text-white mt-3 mb-1">{getCharacterName(perf.characterId)}</h3>
                    <div className="text-xs text-purple-400 mb-3 truncate">{getProductionName(perf.productionUnitId)}</div>
                    {perf.personId && (
                       <div className="text-xs text-neutral-400 mb-2">
                         <span className="font-bold text-neutral-600">PERFORMER:</span> {getPersonName(perf.personId)}
                       </div>
                    )}
                    <p className="text-sm text-neutral-300 bg-black/50 p-3 rounded border border-neutral-800/50 mt-2">{perf.notes || 'No description provided.'}</p>
                    <div className="mt-4 pt-3 border-t border-neutral-800 flex justify-between items-center">
                       <div className="text-[10px] text-neutral-500 font-mono">Takes: {takes.filter(t => t.performanceId === perf.id).length}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'takes' && (
             <div className="space-y-4">
               <div className="flex justify-between items-center border-b border-neutral-800 pb-4 mb-4">
                <h2 className="text-lg font-bold uppercase tracking-widest text-neutral-300">Takes</h2>
              </div>
              <div className="space-y-2">
                {takes.map(take => (
                  <div key={take.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-4 flex items-center justify-between">
                     <div>
                       <div className="flex items-center space-x-3 mb-1">
                          <span className="text-sm font-bold text-white">Take {take.takeNumber}</span>
                          <span className="text-[10px] bg-neutral-800 text-neutral-400 px-2 py-0.5 rounded font-mono uppercase tracking-wider">{take.status}</span>
                       </div>
                       <div className="text-xs text-neutral-500 font-mono">Perf ID: {take.performanceId}</div>
                     </div>
                     <div className="text-right">
                       {take.sourceClipId && <div className="text-[10px] text-blue-400 font-mono border border-blue-900/50 bg-blue-950/30 px-2 py-1 rounded inline-block">SOURCE: {take.sourceClipId}</div>}
                       {take.generatedAssetId && <div className="text-[10px] text-orange-400 font-mono border border-orange-900/50 bg-orange-950/30 px-2 py-1 rounded inline-block">GENERATED: {take.generatedAssetId}</div>}
                     </div>
                  </div>
                ))}
                {takes.length === 0 && (
                  <div className="text-center py-12 text-neutral-500 font-mono text-sm border border-dashed border-neutral-800 rounded">
                    No takes recorded.
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'relationships' && (
             <div className="space-y-4">
                <div className="text-center py-12 text-neutral-500 font-mono text-sm border border-dashed border-neutral-800 rounded">
                    Relationship graph visualization coming soon...
                </div>
             </div>
          )}

        </div>
      </div>
    </div>
  );
};
