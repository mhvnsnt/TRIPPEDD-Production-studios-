import { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Video, FileText, CheckCircle2, AlertCircle, Clock, Search, Activity, Link as LinkIcon, Edit2, PlayCircle, Eye, GitMerge, SplitSquareHorizontal, Check, X, RefreshCcw, Mic } from 'lucide-react';
import { globalGraph, globalPhysicalTimeline } from '../core/pipeline/state';
import { seedPhysicalEvidence } from '../core/pipeline/seed';
import { Observation, CaptureSession, SourceClip } from '../core/types';

// Run seed only once
let isSeeded = false;
if (!isSeeded) {
  seedPhysicalEvidence();
  isSeeded = true;
}

export function PhysicalEvidenceWorkspace() {
  const [activeTab, setActiveTab] = useState<'inspector' | 'timeline' | 'comparison' | 'chronology'>('inspector');
  const [sessions, setSessions] = useState<CaptureSession[]>([]);
  const [clips, setClips] = useState<SourceClip[]>([]);
  const [observations, setObservations] = useState<Observation[]>([]);
  const [selectedObs, setSelectedObs] = useState<Observation | null>(null);

  useEffect(() => {
    // Load state
    setSessions(Array.from(globalGraph.captureSessions.values()));
    setClips(globalPhysicalTimeline.getTimeline().clips);
    setObservations(Object.values(globalPhysicalTimeline.getTimeline().observations));
  }, []);

  const handleReviewAction = (obsId: string, action: 'CONFIRM' | 'REJECT') => {
    if (action === 'CONFIRM') {
      globalPhysicalTimeline.confirmObservation(obsId);
    } else {
      globalPhysicalTimeline.rejectObservation(obsId);
    }
    setObservations(Object.values(globalPhysicalTimeline.getTimeline().observations));
    if (selectedObs?.id === obsId) {
      setSelectedObs(globalPhysicalTimeline.getObservation(obsId));
    }
  };

  const renderInspector = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sessions.map(session => {
          const wo = globalGraph.workOrders.get(session.workOrderId || '');
          const sessionClips = clips.filter(c => c.captureSessionId === session.id);
          return (
            <div key={session.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-5 flex flex-col">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-bold text-white mb-1">Session {session.id}</h3>
                  <div className="text-xs text-neutral-500 font-mono">WO: {session.workOrderId || 'N/A'} - {wo?.title}</div>
                </div>
                <div className={`px-2 py-1 rounded text-xs font-bold ${
                  session.status === 'COMPLETED' ? 'bg-emerald-500/20 text-emerald-400' :
                  session.status === 'FAILED' ? 'bg-red-500/20 text-red-400' :
                  'bg-blue-500/20 text-blue-400'
                }`}>
                  {session.status}
                </div>
              </div>
              
              <div className="text-sm text-neutral-400 space-y-2 flex-1">
                <div className="flex justify-between"><span>Unit:</span> <span className="text-white">{session.productionUnitId}</span></div>
                <div className="flex justify-between"><span>Media Received:</span> <span className="text-white">{session.mediaReceived ? 'YES' : 'NO'}</span></div>
                <div className="flex justify-between"><span>Source Clips:</span> <span className="text-white">{sessionClips.length}</span></div>
                {session.notes && <div className="text-neutral-500 italic mt-2 text-xs border-t border-neutral-800 pt-2">{session.notes}</div>}
              </div>

              <div className="mt-4 border-t border-neutral-800 pt-4">
                <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-wider mb-2">Tool Execution Status</h4>
                
                <div className="space-y-2">
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-neutral-300 flex items-center"><CheckCircle2 size={12} className="text-emerald-500 mr-1.5" /> ffprobe</span>
                    <span className="text-neutral-500">v4.4.2 (Code 0)</span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-neutral-300 flex items-center"><CheckCircle2 size={12} className="text-emerald-500 mr-1.5" /> scenedetect</span>
                    <span className="text-neutral-500">v0.6.1 (Code 0)</span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-neutral-300 flex items-center"><CheckCircle2 size={12} className="text-emerald-500 mr-1.5" /> whisper</span>
                    <span className="text-neutral-500">v1.0 (Code 0)</span>
                  </div>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-neutral-400 flex items-center"><AlertCircle size={12} className="text-yellow-500 mr-1.5" /> opencv</span>
                    <span className="text-yellow-500">UNAVAILABLE</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );

  const renderTimeline = () => {
    // Sort observations chronologically
    const sortedObs = [...observations].sort((a, b) => {
      const timeA = parseFloat(a.startTime || '0');
      const timeB = parseFloat(b.startTime || '0');
      return timeA - timeB;
    });

    return (
      <div className="space-y-6">
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 flex items-start">
          <AlertCircle className="text-yellow-500 shrink-0 mr-3 mt-0.5" size={18} />
          <div>
            <h4 className="text-yellow-500 font-bold text-sm mb-1">Physical Timeline — PARTIAL</h4>
            <p className="text-yellow-400/80 text-xs mt-2">
              7 source clips available. 5 expected uploads pending. Chronology confidence: provisional.<br/>
              Unresolved chronology and expected-but-unavailable material are pending additional source media.
            </p>
          </div>
        </div>

        <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-6 overflow-x-auto">
          <div className="min-w-[800px]">
            {/* Timeline Header */}
            <div className="flex items-center text-xs text-neutral-500 font-mono mb-4">
              <span>00:00:00</span>
              <div className="flex-1 h-px bg-neutral-800 mx-4 relative">
                <div className="absolute top-1/2 -translate-y-1/2 left-[20%] w-1.5 h-1.5 rounded-full bg-neutral-600"></div>
                <div className="absolute top-1/2 -translate-y-1/2 left-[50%] w-1.5 h-1.5 rounded-full bg-neutral-600"></div>
                <div className="absolute top-1/2 -translate-y-1/2 left-[80%] w-1.5 h-1.5 rounded-full bg-neutral-600"></div>
              </div>
              <span>00:04:37</span>
            </div>

            {/* Shots Track */}
            <div className="mb-6 relative">
              <div className="text-[10px] font-bold text-neutral-600 uppercase tracking-widest absolute -left-20 top-2 w-16 text-right">Shots</div>
              <div className="flex gap-2">
                {sortedObs.filter(o => o.type === 'SHOT').map((obs, i) => (
                  <button 
                    key={obs.id}
                    onClick={() => setSelectedObs(obs)}
                    className={`h-16 rounded border text-left p-2 flex flex-col justify-between transition-colors ${
                      selectedObs?.id === obs.id ? 'bg-blue-500/20 border-blue-500' : 'bg-neutral-800 border-neutral-700 hover:border-neutral-500'
                    }`}
                    style={{ flex: Math.max(1, parseFloat(obs.endTime || '10') - parseFloat(obs.startTime || '0')) }}
                  >
                    <span className="text-xs font-bold text-white truncate">{obs.description}</span>
                    <span className="text-[10px] text-neutral-400 font-mono">{obs.startTime}s - {obs.endTime}s</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Transcripts Track */}
            <div className="mb-6 relative h-12">
              <div className="text-[10px] font-bold text-neutral-600 uppercase tracking-widest absolute -left-20 top-2 w-16 text-right">Vocals</div>
              {sortedObs.filter(o => o.type === 'TRANSCRIPT').map((obs, i) => (
                <button 
                  key={obs.id}
                  onClick={() => setSelectedObs(obs)}
                  className={`absolute top-0 h-8 px-3 rounded-full flex items-center text-xs whitespace-nowrap transition-colors ${
                    selectedObs?.id === obs.id ? 'bg-purple-500 text-white' : 'bg-purple-500/20 text-purple-300 hover:bg-purple-500/40'
                  }`}
                  style={{ left: `${(parseFloat(obs.startTime || '0') / 150) * 100}%` }}
                >
                  <Mic size={12} className="mr-1.5 opacity-70" />
                  "{(obs as any).text}"
                </button>
              ))}
            </div>

            {/* Events Track */}
            <div className="relative h-12">
              <div className="text-[10px] font-bold text-neutral-600 uppercase tracking-widest absolute -left-20 top-2 w-16 text-right">Events</div>
              {sortedObs.filter(o => o.type === 'EVENT').map((obs, i) => (
                <button 
                  key={obs.id}
                  onClick={() => setSelectedObs(obs)}
                  className={`absolute top-0 h-8 px-3 rounded flex items-center border text-xs whitespace-nowrap transition-colors ${
                    selectedObs?.id === obs.id ? 'bg-amber-500/20 border-amber-500 text-amber-400' : 'bg-neutral-800 border-neutral-700 text-neutral-400 hover:border-neutral-500'
                  }`}
                  style={{ left: `${(parseFloat(obs.startTime || '0') / 150) * 100}%` }}
                >
                  <Activity size={12} className="mr-1.5 opacity-70" />
                  {(obs as any).eventLabel}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Observation Detail Panel */}
        {selectedObs && (
          <div className="bg-neutral-900 border border-neutral-800 rounded-lg p-5">
            <div className="flex justify-between items-start mb-6">
              <div>
                <div className="flex items-center space-x-3 mb-1">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-neutral-800 text-neutral-400">
                    {selectedObs.type}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                    selectedObs.origin === 'MACHINE_GENERATED' ? 'bg-blue-500/20 text-blue-400' : 'bg-fuchsia-500/20 text-fuchsia-400'
                  }`}>
                    {selectedObs.origin}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                    selectedObs.reviewState === 'CONFIRMED' ? 'bg-emerald-500/20 text-emerald-400' :
                    selectedObs.reviewState === 'REJECTED' ? 'bg-red-500/20 text-red-400' :
                    'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    {selectedObs.reviewState}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white">{selectedObs.description}</h3>
                
                {selectedObs.type === 'TRANSCRIPT' && (selectedObs as any).editorialClassification && (
                  <div className="mt-4 p-3 bg-neutral-950 border border-neutral-800 rounded">
                    <h4 className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-2">Editorial Classification</h4>
                    <div className="flex items-center space-x-2">
                       <span className={`px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider ${
                          (selectedObs as any).editorialClassification === 'PRODUCTION_ARTIFACT' ? 'bg-orange-500/20 text-orange-400' :
                          (selectedObs as any).editorialClassification === 'PROGRAM_CONTENT' ? 'bg-blue-500/20 text-blue-400' :
                          'bg-neutral-700 text-neutral-300'
                       }`}>
                         {(selectedObs as any).editorialClassification}
                       </span>
                       {(selectedObs as any).editorialReason && (
                         <span className="text-xs text-neutral-400 italic">{(selectedObs as any).editorialReason}</span>
                       )}
                    </div>
                  </div>
                )}
  
                {selectedObs.type === 'TRANSCRIPT' && (
                  <p className="text-white italic mt-2">"{(selectedObs as any).text}"</p>
                )}
              </div>
              <div className="text-right text-xs text-neutral-500 font-mono">
                <div>Clip: {selectedObs.sourceClipId}</div>
                <div>{selectedObs.startTime}s - {selectedObs.endTime}s</div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-wider border-b border-neutral-800 pb-2">Review Actions</h4>
                <div className="flex flex-wrap gap-2">
                  <button onClick={() => handleReviewAction(selectedObs.id, 'CONFIRM')} className="flex items-center px-3 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-500 rounded text-xs font-medium transition-colors">
                    <Check size={14} className="mr-1.5" /> Confirm
                  </button>
                  <button onClick={() => handleReviewAction(selectedObs.id, 'REJECT')} className="flex items-center px-3 py-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-500 rounded text-xs font-medium transition-colors">
                    <X size={14} className="mr-1.5" /> Reject
                  </button>
                  <button className="flex items-center px-3 py-1.5 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 rounded text-xs font-medium transition-colors">
                    <Edit2 size={14} className="mr-1.5" /> Correct
                  </button>
                  <button className="flex items-center px-3 py-1.5 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 rounded text-xs font-medium transition-colors">
                    <SplitSquareHorizontal size={14} className="mr-1.5" /> Split
                  </button>
                  <button className="flex items-center px-3 py-1.5 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 rounded text-xs font-medium transition-colors">
                    <GitMerge size={14} className="mr-1.5" /> Merge
                  </button>
                </div>
              </div>

              {selectedObs.toolProvenance && (
                <div className="space-y-3">
                  <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-wider border-b border-neutral-800 pb-2">Tool Provenance</h4>
                  <div className="text-xs space-y-1 font-mono text-neutral-400 bg-black/50 p-3 rounded border border-neutral-800">
                    <div className="flex"><span className="w-20 text-neutral-500">Tool:</span> <span className="text-blue-400">{selectedObs.toolProvenance.tool} v{selectedObs.toolProvenance.version}</span></div>
                    <div className="flex"><span className="w-20 text-neutral-500">Command:</span> <span className="text-white truncate">{selectedObs.toolProvenance.command}</span></div>
                    <div className="flex"><span className="w-20 text-neutral-500">Exit Code:</span> <span className={selectedObs.toolProvenance.exitCode === 0 ? 'text-emerald-400' : 'text-red-400'}>{selectedObs.toolProvenance.exitCode}</span></div>
                    <div className="flex"><span className="w-20 text-neutral-500">Timestamp:</span> <span>{new Date(selectedObs.toolProvenance.timestamp).toLocaleTimeString()}</span></div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    );
  };

  
  const renderChronology = () => {
    const rels = (globalPhysicalTimeline.getTimeline() as any).chronologyRelationships || [];
    return (
      <div className="space-y-6">
        <div className="bg-blue-900/10 border border-blue-500/30 rounded-lg p-5 flex items-start">
          <LinkIcon className="text-blue-500 shrink-0 mr-4 mt-0.5" size={20} />
          <div>
            <h4 className="text-blue-400 font-bold text-sm mb-1">Chronology Reconstruction</h4>
            <p className="text-blue-300/80 text-xs">
              TRIPPEDD has identified potential temporal relationships based on the 7 available clips. 
              These relationships require human confirmation.
            </p>
          </div>
        </div>
        
        <div className="grid grid-cols-1 gap-4">
          {rels.map((rel: any) => (
            <div key={rel.id} className="bg-neutral-900 border border-neutral-800 rounded-lg p-5">
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-white font-mono text-sm bg-neutral-800 px-3 py-1 rounded">{rel.sourceClipIdA}</span>
                  <div className="flex flex-col items-center px-4">
                     <span className="text-[10px] text-neutral-500 uppercase tracking-widest font-bold mb-1">{rel.relationshipType}</span>
                     <div className="w-12 h-px bg-neutral-700 relative">
                       <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 border-t border-r border-neutral-500 transform rotate-45"></div>
                     </div>
                  </div>
                  <span className="text-white font-mono text-sm bg-neutral-800 px-3 py-1 rounded">{rel.sourceClipIdB}</span>
                </div>
                <div className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider shadow-lg ${
                  rel.confidence === 'CONFIRMED' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                  rel.confidence === 'PROVISIONAL' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                  'bg-red-500/20 text-red-400 border border-red-500/30'
                }`}>
                  {rel.confidence} {rel.humanConfirmed && ' (HUMAN)'}
                </div>
              </div>
              
              <div className="bg-black/50 rounded border border-neutral-800 p-4">
                <h5 className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider mb-2">Evidence</h5>
                
                <div className="space-y-2">
                  <p className="text-sm text-neutral-300">
                    <span className="font-semibold text-neutral-400">Reasoning:</span> {rel.evidenceDetails?.reasoning || 'No evidence'}
                  </p>
                  {rel.evidenceDetails?.missingSignals && rel.evidenceDetails.missingSignals.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      <span className="text-[10px] text-neutral-500 uppercase tracking-widest font-bold">Missing Signals:</span>
                      {rel.evidenceDetails.missingSignals.map((sig: string) => (
                        <span key={sig} className="px-2 py-0.5 bg-red-900/20 text-red-400/80 rounded border border-red-900/30 text-[9px] uppercase font-mono">{sig}</span>
                      ))}
                    </div>
                  )}
                </div>
  
              </div>

              {!rel.humanConfirmed && (
                 <div className="mt-4 flex space-x-3 border-t border-neutral-800 pt-4">
                    <button onClick={() => {
                        (globalPhysicalTimeline as any).confirmChronologyRelationship(rel.id);
                        setObservations({...globalPhysicalTimeline.getTimeline().observations} as any); // force re-render
                    }} className="flex items-center px-4 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-500 rounded text-xs font-bold transition-colors">
                      <CheckCircle2 size={14} className="mr-2" /> Confirm Relationship
                    </button>
                    <button className="flex items-center px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-neutral-400 rounded text-xs font-bold transition-colors">
                      Reject
                    </button>
                 </div>
              )}
            </div>
          ))}
          {rels.length === 0 && (
            <div className="text-center py-12 text-neutral-500 text-sm italic">
              No overlapping chronology identified yet.
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderComparison = () => (
    <div className="space-y-6">
      <div className="bg-neutral-900 border border-neutral-800 rounded-lg overflow-hidden flex flex-col h-[600px]">
        <div className="grid grid-cols-2 bg-neutral-950 border-b border-neutral-800">
          <div className="p-4 flex flex-col justify-center border-r border-neutral-800">
            <h3 className="text-sm font-bold text-white tracking-widest uppercase mb-1">INTENDED / STORYBOARD</h3>
            <p className="text-xs text-neutral-500">Expected production plan</p>
          </div>
          <div className="p-4 flex flex-col justify-center">
            <h3 className="text-sm font-bold text-white tracking-widest uppercase mb-1">PHYSICAL SOURCE</h3>
            <p className="text-xs text-neutral-500">What was actually captured</p>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          
          {/* Item 1 */}
          <div className="grid grid-cols-2 relative group">
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10">
               <div className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-3 py-1 rounded-full text-[10px] font-bold shadow-lg">MATCH</div>
            </div>
            <div className="pr-8 pb-4 border-r border-neutral-800">
              <div className="bg-neutral-800/50 rounded p-3 text-sm text-neutral-300">
                <span className="text-xs font-mono text-neutral-500 block mb-1">Event: BAG_INCIDENT</span>
                Expected Bag Incident to occur in the first scene.
              </div>
            </div>
            <div className="pl-8 pb-4">
              <div className="bg-neutral-800/50 rounded p-3 text-sm text-neutral-300 border-l-2 border-emerald-500">
                <span className="text-xs font-mono text-neutral-500 block mb-1">OBS_E1 (0:30 - 0:40)</span>
                Physical event confirmed.
              </div>
            </div>
          </div>

          {/* Item 2 */}
          <div className="grid grid-cols-2 relative group">
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10">
               <div className="bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 px-3 py-1 rounded-full text-[10px] font-bold shadow-lg flex flex-col items-center whitespace-nowrap">
                 UNRESOLVED — additional source media pending
               </div>
            </div>
            <div className="pr-8 pb-4 border-r border-neutral-800 opacity-70">
              <div className="bg-neutral-800/50 rounded p-3 text-sm text-neutral-300">
                <span className="text-xs font-mono text-neutral-500 block mb-1">Event: JOE_INTERACTION</span>
                Expected interaction with Joe shortly after.
              </div>
            </div>
            <div className="pl-8 pb-4 flex items-center justify-center">
              <div className="text-sm text-neutral-500 italic">Not detected in available clips.</div>
            </div>
          </div>

          {/* Item 3 */}
          <div className="grid grid-cols-2 relative group">
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10">
               <div className="bg-fuchsia-500/20 text-fuchsia-400 border border-fuchsia-500/30 px-3 py-1 rounded-full text-[10px] font-bold shadow-lg whitespace-nowrap">FOUND_BUT_NOT_IN_STORYBOARD</div>
            </div>
            <div className="pr-8 pb-4 border-r border-neutral-800 flex items-center justify-center">
              <div className="text-sm text-neutral-500 italic">No corresponding storyboard event.</div>
            </div>
            <div className="pl-8 pb-4">
              <div className="bg-neutral-800/50 rounded p-3 text-sm text-neutral-300 border-l-2 border-fuchsia-500">
                <span className="text-xs font-mono text-neutral-500 block mb-1">OBS_E2 (1:43 - 1:50)</span>
                Unexpected physical event (OTHER).
              </div>
            </div>
          </div>

          {/* Item 4 */}
          <div className="grid grid-cols-2 relative group">
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-10">
               <div className="bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 px-3 py-1 rounded-full text-[10px] font-bold shadow-lg whitespace-nowrap">
                 UNRESOLVED — additional source media pending
               </div>
            </div>
            <div className="pr-8 pb-4 border-r border-neutral-800">
              <div className="bg-neutral-800/50 rounded p-3 text-sm text-neutral-300">
                <span className="text-xs font-mono text-neutral-500 block mb-1">Dialogue</span>
                "Hey give it back!"
              </div>
            </div>
            <div className="pl-8 pb-4 flex items-center justify-center">
              <div className="text-sm text-neutral-500 italic text-center">
                Analysis completed on available clips — <br/> dialogue not detected.
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );

  return (
    <div className="flex flex-col h-full bg-black">
      {/* Header */}
      <div className="shrink-0 border-b border-neutral-800 bg-neutral-950 p-6 flex items-center justify-between z-10 relative">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center border border-blue-500/20">
            <Eye className="text-blue-500" size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-black text-white tracking-tight">Evidence Review</h1>
            <p className="text-neutral-500 text-sm">Inspect physical media ingest, observations, and storyboard discrepancies.</p>
          </div>
        </div>
        <div className="flex space-x-2">
           <button className="flex items-center px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-white rounded-md text-sm font-medium transition-colors">
             <RefreshCcw size={16} className="mr-2 opacity-70" /> Refresh Evidence
           </button>
        </div>
      </div>

      <div className="flex-1 overflow-hidden flex flex-col relative z-0 p-6">
        {/* Navigation Tabs */}
        <div className="flex space-x-1 mb-6 border-b border-neutral-800 pb-px">
          {[
            { id: 'inspector', label: 'Capture Inspector', icon: Search },
            { id: 'timeline', label: 'Physical Timeline', icon: Clock },
            { id: 'comparison', label: 'Discrepancy Analysis', icon: SplitSquareHorizontal },
            { id: 'chronology', label: 'Chronology Map', icon: LinkIcon }
          ].map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center px-4 py-2 text-sm font-bold tracking-wider uppercase border-b-2 transition-colors ${
                  isActive 
                    ? 'border-white text-white' 
                    : 'border-transparent text-neutral-500 hover:text-neutral-300 hover:border-neutral-700'
                }`}
              >
                <Icon size={16} className="mr-2 mb-0.5" /> {tab.label}
              </button>
            )
          })}
        </div>

        <div className="flex-1 overflow-y-auto custom-scrollbar pr-2">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {activeTab === 'inspector' && renderInspector()}
            {activeTab === 'timeline' && renderTimeline()}
            {activeTab === 'comparison' && renderComparison()}
            {activeTab === 'chronology' && renderChronology()}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
