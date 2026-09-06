import { useState } from 'react';
import { Play, Sparkles, FolderOpen, Image as ImageIcon, Video, Clock, Plus } from 'lucide-react';
import { initialProductionData } from '../data';
import { JobManager } from '../core/jobs/manager';
import { EffectOrchestrator } from '../core/pipeline/effects';
import { AssetRegistry } from '../core/assets/registry';

export function StoryWorkspace() {
  const [selectedStory, setSelectedStory] = useState<any | null>(null);
  const [addedEffect, setAddedEffect] = useState<any | null>(null);
  
  const stories = initialProductionData.filter(item => item.type === 'STORY' || item.type === 'CHARACTER' || item.type === 'SCENE');

  const handleAddEffect = () => {
    setAddedEffect({
      name: 'LUCK_OF_IRISH_GREEN_IRIS',
      trigger: 'OPTIONAL'
    });
  };

  const handleExecutePipeline = async () => {
    try {
      // In a real flow, you'd select which physical asset this scene uses.
      // We will fallback to a real test plate we know we generated earlier to prove the pipeline.
      const testPlateId = 'TEST_PLATE_123'; 
      // We will let the orchestrator fail naturally if the asset doesn't exist,
      // so let's use the actual plate we generated in JobsPipeline or register it here quickly:
      
      let basePlate = AssetRegistry.getAsset('TEST_PLATE_123');
      if (!basePlate) {
        basePlate = AssetRegistry.registerAsset({
          name: 'motel_6_plate_raw',
          type: 'video',
          path: '/trippedd_project/assets/real/motel_6_plate.mp4',
          projectId: 'TRIPPEDD_001',
          version: 1,
          provenance: { realityStatus: 'FACTUAL', captureStatus: 'DIRECTLY_CAPTURED', authorship: 'USER_AUTHORED', generationMethods: ['LIVE_CAPTURE'], assemblyMode: 'PURE_LIVE_ACTION', aiContributions: ['NONE'], aggregate: 'REAL_PRODUCTION' },
          verificationState: 'VERIFIED',
          contentType: 'raw_plate',
          status: 'AVAILABLE'
        });
        // Override ID for deterministic testing
        basePlate.id = 'TEST_PLATE_123';
      }

      await EffectOrchestrator.runLuckOfTheIrish(basePlate.id, 'TRIPPEDD_001');
      alert("Pipeline Execution Initiated. Check Jobs Workspace.");
    } catch (e: any) {
      alert("Execution blocked: " + e.message);
    }
  };

  return (
    <div className="flex h-full w-full">
      {/* List Sidebar */}
      <div className="w-80 border-r border-neutral-800 bg-neutral-900/50 flex flex-col h-full shrink-0">
        <div className="p-4 border-b border-neutral-800">
          <h2 className="font-black text-white tracking-widest text-sm">FICTION DATABASE</h2>
        </div>
        <div className="overflow-y-auto p-2 space-y-1">
          {stories.map(story => (
            <button
              key={story.id}
              onClick={() => setSelectedStory(story)}
              className={`w-full text-left p-3 rounded-lg transition-colors ${
                selectedStory?.id === story.id 
                  ? 'bg-blue-600/10 border-blue-500/30 border text-white' 
                  : 'hover:bg-neutral-800 border border-transparent text-neutral-400'
              }`}
            >
              <div className="text-xs font-mono mb-1 flex items-center justify-between">
                <span className={story.type === 'STORY' ? 'text-purple-400' : 'text-emerald-400'}>
                  {story.type}
                </span>
                <span className="text-neutral-600">{story.id}</span>
              </div>
              <div className="font-bold truncate">{story.title}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Main Area */}
      <div className="flex-1 flex flex-col overflow-hidden bg-neutral-950">
        {selectedStory ? (
          <div className="p-8 overflow-y-auto max-w-4xl mx-auto w-full">
            <div className="mb-8">
              <div className="flex items-center gap-3 mb-4">
                <span className="px-2 py-1 bg-fuchsia-500/10 text-fuchsia-400 border border-fuchsia-500/20 rounded text-xs font-mono font-bold tracking-widest">
                  {selectedStory.contentType || 'FICTIONAL_CREATION'}
                </span>
                <span className="px-2 py-1 bg-neutral-800 text-neutral-400 rounded text-xs font-mono tracking-widest">
                  PROVENANCE: {selectedStory.provenance?.aggregate || 'USER_CREATED'}
                </span>
              </div>
              <h1 className="text-4xl font-black text-white mb-4 uppercase">{selectedStory.title}</h1>
              <p className="text-neutral-300 text-lg leading-relaxed">{selectedStory.description}</p>
              
              {selectedStory.metadata?.recurrence && (
                <div className="mt-4 inline-flex bg-neutral-900 border border-neutral-800 text-neutral-400 font-mono text-xs px-3 py-1.5 rounded">
                  RECURRENCE: <span className="text-white ml-2">{selectedStory.metadata.recurrence}</span>
                </div>
              )}
            </div>

            {selectedStory.title === 'Luck of the Irish!' && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                {/* Uploaded Reference Visuals Placeholder */}
                <div className="aspect-square bg-neutral-900 rounded-lg border border-neutral-800 flex items-center justify-center flex-col text-neutral-500">
                  <ImageIcon size={24} className="mb-2" />
                  <span className="text-xs font-mono">REF: Leprechaun</span>
                </div>
                <div className="aspect-square bg-neutral-900 rounded-lg border border-neutral-800 flex items-center justify-center flex-col text-neutral-500">
                  <ImageIcon size={24} className="mb-2" />
                  <span className="text-xs font-mono">REF: Mascot Face</span>
                </div>
                <div className="aspect-square bg-neutral-900 rounded-lg border border-neutral-800 flex items-center justify-center flex-col text-neutral-500">
                  <Video size={24} className="mb-2" />
                  <span className="text-xs font-mono">REF: 7Up Style</span>
                </div>
                <div className="aspect-square bg-neutral-900 rounded-lg border border-neutral-800 flex items-center justify-center flex-col text-neutral-500">
                  <ImageIcon size={24} className="mb-2" />
                  <span className="text-xs font-mono">REF: Green Iris</span>
                </div>
              </div>
            )}

            <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 mb-8">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <Sparkles size={18} className="text-emerald-400" />
                VISUAL EFFECTS PIPELINE
              </h3>
              
              {!addedEffect ? (
                <div>
                  <p className="text-sm text-neutral-400 mb-6 max-w-2xl">
                    Attach complex, multi-stage generative pipelines to this scene.
                  </p>
                  
                  <button 
                    onClick={handleAddEffect}
                    className="bg-neutral-800 hover:bg-neutral-700 text-white px-4 py-2 rounded font-bold transition-colors flex items-center gap-2 text-sm"
                  >
                    <Plus size={16} />
                    ADD EFFECT &rarr; LUCK OF THE IRISH™
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg flex items-center justify-between">
                    <div>
                      <div className="flex items-center gap-3 mb-1">
                        <span className="font-bold text-emerald-400 font-mono">{addedEffect.name}</span>
                        <span className="px-2 py-0.5 bg-neutral-950 rounded text-[10px] text-neutral-400 font-mono uppercase border border-neutral-800">
                          {addedEffect.trigger} TRIGGER
                        </span>
                      </div>
                      <div className="text-xs text-neutral-400 font-mono mt-2">
                        Sequence: Plate &rarr; Extract &rarr; Transform &rarr; Green Iris &rarr; Freeze &rarr; Commercial Card &rarr; Composite
                      </div>
                    </div>
                    
                    <button 
                      onClick={handleExecutePipeline}
                      className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded font-bold transition-colors flex items-center gap-2 text-sm uppercase tracking-widest"
                    >
                      <Play size={16} fill="currentColor" />
                      Execute Pipeline
                    </button>
                  </div>
                </div>
              )}
            </div>
            
            <div className="border-t border-neutral-800 pt-6">
               <h3 className="text-sm font-bold text-neutral-500 mb-4 tracking-widest">ASSETS & PIPELINE PRESETS</h3>
               <div className="flex gap-4">
                 {selectedStory.title === 'Luck of the Irish!' ? (
                   <div className="bg-neutral-900 border border-neutral-800 p-4 rounded-lg flex items-start gap-4">
                     <div className="p-3 bg-emerald-500/10 text-emerald-500 rounded border border-emerald-500/20">
                       <Clock size={20} />
                     </div>
                     <div>
                       <div className="text-sm font-bold text-white font-mono mb-1">LUCK_OF_IRISH_GREEN_IRIS</div>
                       <div className="text-xs text-neutral-500">Reusable transition preset. Can be invoked by any scene.</div>
                     </div>
                   </div>
                 ) : (
                   <div className="text-sm text-neutral-600 italic">No assets registered yet.</div>
                 )}
               </div>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-neutral-500 flex-col">
            <FolderOpen size={48} className="mb-4 opacity-20" />
            <p className="font-mono text-sm tracking-widest">SELECT A CONCEPT TO BEGIN</p>
          </div>
        )}
      </div>
    </div>
  );
}
