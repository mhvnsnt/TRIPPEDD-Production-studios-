import React, { useState } from 'react';
import { ProductionGraph } from '../core/pipeline/productionGraph';

export const ProductionControlWorkspace: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'today' | 'departments' | 'blocked' | 'in_progress' | 'completed' | 'conflicts' | 'missing_evidence'>('today');
  const graph = ProductionGraph.getInstance();
  
  const workOrders = Array.from(graph.workOrders.values());
  const crewAssignments = Array.from(graph.crewAssignments.values());
  const people = Array.from(graph.people.values());
  const productions = Array.from(graph.productionUnits.values());

  const getPersonName = (id?: string) => people.find(p => p.id === id)?.name || id || 'Unassigned';
  const getProductionName = (id?: string) => productions.find(p => p.id === id)?.name || 'Unknown Production';

  const today = new Date(); // In a real app this would be configurable
  
  const conflicts = graph.checkScheduleConflicts(
    new Date(today.getTime() - 86400000).toISOString(),
    new Date(today.getTime() + 86400000).toISOString()
  );

  return (
    <div className="h-full flex flex-col bg-black text-white p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-widest uppercase mb-1">Production Control</h1>
          <p className="text-neutral-500 font-mono text-xs uppercase tracking-wider">
            Work Orders • Crew Assignments • Scheduling
          </p>
        </div>
      </div>

      <div className="flex-1 flex flex-col border border-neutral-800 rounded-lg overflow-hidden bg-neutral-950">
        <div className="flex border-b border-neutral-800 overflow-x-auto custom-scrollbar">
          {['today', 'departments', 'blocked', 'in_progress', 'completed', 'conflicts', 'missing_evidence'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab as any)}
              className={`px-6 py-3 text-xs font-bold uppercase tracking-widest border-b-2 transition-colors whitespace-nowrap ${activeTab === tab ? 'border-blue-500 text-blue-400' : 'border-transparent text-neutral-500 hover:text-neutral-300'}`}
            >
              {tab.replace('_', ' ')}
            </button>
          ))}
        </div>

        <div className="flex-1 overflow-y-auto p-6 custom-scrollbar">
          
          {(activeTab === 'today' || activeTab === 'in_progress' || activeTab === 'completed' || activeTab === 'blocked' || activeTab === 'departments') && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {workOrders
                  .filter(wo => {
                    if (activeTab === 'today') return wo.status === 'SCHEDULED';
                    if (activeTab === 'in_progress') return wo.status === 'IN_PROGRESS';
                    if (activeTab === 'completed') return wo.status === 'COMPLETED';
                    if (activeTab === 'blocked') return wo.status === 'BLOCKED';
                    return true;
                  })
                  .map(wo => (
                  <div key={wo.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-white text-sm">{wo.title}</h3>
                      <span className={`text-[10px] px-2 py-0.5 rounded font-mono uppercase tracking-wider ${
                        wo.status === 'BLOCKED' ? 'bg-red-900/30 text-red-400' : 
                        wo.status === 'COMPLETED' ? 'bg-green-900/30 text-green-400' :
                        wo.status === 'IN_PROGRESS' ? 'bg-blue-900/30 text-blue-400' :
                        'bg-neutral-800 text-neutral-400'
                      }`}>
                        {wo.status}
                      </span>
                    </div>
                    <div className="text-xs text-blue-400 mb-2 truncate">{getProductionName(wo.productionUnitId)}</div>
                    <div className="text-xs text-neutral-500 font-mono mb-2 uppercase tracking-wider">{wo.departmentId}</div>
                    
                    <p className="text-sm text-neutral-400 line-clamp-2 mb-3">{wo.description}</p>
                    
                    <div className="border-t border-neutral-800 pt-3 flex justify-between items-center text-xs">
                       <span className="text-neutral-500 font-mono">Assigned: <span className="text-white">{getPersonName(wo.responsiblePersonId)}</span></span>
                    </div>
                    
                    {activeTab === 'blocked' && wo.dependencies.length > 0 && (
                       <div className="mt-2 bg-red-950/30 border border-red-900/50 p-2 rounded text-xs text-red-400">
                          <span className="font-bold">Dependencies:</span> {wo.dependencies.join(', ')}
                       </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'missing_evidence' && (
             <div className="space-y-4">
               {workOrders.filter(wo => wo.status === 'COMPLETED' && wo.evidenceRefs.length === 0).map(wo => (
                  <div key={wo.id} className="bg-neutral-900 border border-yellow-900/50 rounded-lg p-4">
                     <h3 className="font-bold text-white mb-1">{wo.title}</h3>
                     <p className="text-xs text-yellow-500">Missing evidence refs for completed work order.</p>
                  </div>
               ))}
               {workOrders.filter(wo => wo.status === 'COMPLETED' && wo.evidenceRefs.length === 0).length === 0 && (
                 <div className="text-center py-12 text-neutral-500 font-mono text-sm border border-dashed border-neutral-800 rounded">
                    No completed work orders missing evidence.
                 </div>
               )}
             </div>
          )}

          {activeTab === 'conflicts' && (
             <div className="space-y-4">
               {conflicts.map((conflict, i) => (
                  <div key={i} className="bg-red-950/20 border border-red-900/50 rounded-lg p-4">
                     <div className="text-red-400 font-bold mb-2">{conflict.description}</div>
                     <div className="text-xs text-neutral-400 font-mono">
                        {conflict.type === 'PERSON_OVERLAP' && conflict.assignments.map((a: any) => (
                           <div key={a.id}>- {a.role} ({a.startAt} to {a.endAt})</div>
                        ))}
                        {conflict.type === 'LOCATION_OVERLAP' && conflict.workOrders.map((wo: any) => (
                           <div key={wo.id}>- {wo.title} ({wo.scheduledStart} to {wo.scheduledEnd})</div>
                        ))}
                     </div>
                  </div>
               ))}
               {conflicts.length === 0 && (
                 <div className="text-center py-12 text-neutral-500 font-mono text-sm border border-dashed border-neutral-800 rounded">
                    No scheduling conflicts detected.
                 </div>
               )}
             </div>
          )}
          
        </div>
      </div>
    </div>
  );
};
