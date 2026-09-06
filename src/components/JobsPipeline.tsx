import { useState, useEffect } from 'react';
import { MixedMediaOrchestrator, MixedMediaShot } from '../core/pipeline/mixed_media';
import { JobManager } from '../core/jobs/manager';
import { AssetRegistry } from '../core/assets/registry';
import { Job } from '../core/types';
import { Activity, CheckCircle2, Clock, XCircle, Terminal, Play, Film } from 'lucide-react';

export function JobsPipeline() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    // Subscribe to job updates
    const unsubscribe = JobManager.subscribe((updatedJobs) => {
      setJobs([...updatedJobs]);
    });
    return () => unsubscribe();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'COMPLETED': return <CheckCircle2 className="text-emerald-500" size={16} />;
      case 'RUNNING': return <Activity className="text-blue-500" size={16} />;
      case 'FAILED': return <XCircle className="text-red-500" size={16} />;
      default: return <Clock className="text-neutral-500" size={16} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLETED': return 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20';
      case 'RUNNING': return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'FAILED': return 'bg-red-500/10 text-red-500 border-red-500/20';
      default: return 'bg-neutral-800 text-neutral-400 border-neutral-700';
    }
  };

  const runJoeMotelTest = async () => {
    try {
      // 1. Register Location References (Photos)
      const locationRef = AssetRegistry.registerAsset({
        name: 'motel_6_location_reference',
        type: 'image',
        path: '/trippedd_project/assets/real/motel_6_ref_01.jpg',
        projectId: 'TRIPPEDD_01',
        version: 1,
        provenance: { realityStatus: 'FACTUAL', captureStatus: 'DIRECTLY_CAPTURED', authorship: 'USER_AUTHORED', generationMethods: ['LIVE_CAPTURE'], assemblyMode: 'PURE_LIVE_ACTION', aiContributions: ['NONE'], aggregate: 'REAL_PRODUCTION' },
        verificationState: 'VERIFIED',
        contentType: 'location_reference',
        status: 'AVAILABLE'
      });

      // 2. Register Joe Character Master
      const joeMaster = AssetRegistry.registerAsset({
        name: 'joe_character_master',
        type: 'image', // or model
        path: '/trippedd_project/assets/generated/joe_master.png',
        projectId: 'TRIPPEDD_01',
        version: 1,
        provenance: { realityStatus: 'FICTIONAL', captureStatus: 'NOT_CAPTURED', authorship: 'AI_AUTHORED', generationMethods: ['AI_GENERATED'], assemblyMode: 'PURE_GENERATED', aiContributions: ['AI_CO_GENERATED'], aggregate: 'FICTIONAL_CREATION' },
        verificationState: 'VERIFIED',
        contentType: 'character_master',
        status: 'AVAILABLE'
      });

      // 3. Define the shot graph for the scene
      const shots: MixedMediaShot[] = [
        {
          id: 'SHOT_01_ESTABLISHING',
          description: 'Establishing shot of motel walkway.',
          performances: {},
          environment: 'REAL_FOOTAGE',
          style: 'REALITY',
          baseAssetId: locationRef.id // Pretending this is the real footage
        },
        {
          id: 'SHOT_02_TRANSITION',
          description: 'Transition to watercolor reality.',
          performances: {},
          environment: 'REAL_FOOTAGE',
          style: 'REALITY_WATERCOLOR_TRANSITION',
          baseAssetId: locationRef.id
        },
        {
          id: 'SHOT_03_JOE_PASSES',
          description: 'Joe walks past and waves.',
          performances: {
            joe: { actorId: 'joe', sourceType: 'GENERATED_ANIMATION' }
          },
          environment: 'GENERATED_FROM_REFERENCE',
          style: 'TRIPPEDD_WATERCOLOR_REALITY',
          baseAssetId: locationRef.id
        },
        // We simulate a few key shots for the orchestration test
        {
          id: 'SHOT_12_HAND_CONTACT',
          description: 'Joe holds Mars and Tyneshia hands.',
          performances: {
            mars: { actorId: 'mars', sourceType: 'REAL_VIDEO' },
            tyneshia: { actorId: 'tyneshia', sourceType: 'REAL_VIDEO' },
            joe: { actorId: 'joe', sourceType: 'GENERATED_ANIMATION' }
          },
          environment: 'GENERATED_FROM_REFERENCE',
          style: 'TRIPPEDD_WATERCOLOR_REALITY',
          baseAssetId: locationRef.id
        },
        {
          id: 'SHOT_24_FINAL_TRANSITION',
          description: 'Transition back to reality.',
          performances: {},
          environment: 'REAL_FOOTAGE',
          style: 'WATERCOLOR_REALITY_TRANSITION',
          baseAssetId: locationRef.id
        }
      ];

      // 4. Execute Pipeline
      const shotAssetIds = [];
      for (const shot of shots) {
         const result = await MixedMediaOrchestrator.generateMixedMediaShot('TRIPPEDD_01', shot, joeMaster.id);
         if (result.assetId) shotAssetIds.push(result.assetId);
      }

      // 5. Assemble Final Scene
      await MixedMediaOrchestrator.assembleScene('TRIPPEDD_01', 'sc-joe', shotAssetIds);

    } catch (e) {
      console.error(e);
    }
  };

  const runLuckOfTheIrishTest = async () => {
    try {
      // 1. Register the base plate (simulating camera ingest)
      const basePlate = AssetRegistry.registerAsset({
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

      // 2. Trigger the complete Commercial Package pipeline
      const { EffectOrchestrator } = await import('../core/pipeline/effects');
      await EffectOrchestrator.generateCommercialPackage({
        sceneAssetId: basePlate.id,
        projectId: 'TRIPPEDD_001',
        luckParams: {
          irisColor: '#00FF00',
          irisThickness: 15,
          openingClosingDirection: 'in',
          centerPosition: { x: 960, y: 540 },
          timing: 2.5,
          easing: 'ease-in-out',
          freezeFrameTiming: 3.0,
          optionalSparkleGlow: true,
          optionalCommercialTitleReveal: true,
          characterPrompt: 'Hood Leprechaun, 8k, photorealistic, glowing green iris, wearing green track suit'
        },
        titlePrompt: "Commercial title card: LUCK OF THE IRISH™, bold emerald green typography, 4k resolution, transparent background",
        disclaimerPrompt: "Legal disclaimer screen, white text on black background, fine print: 'Leprechaun magic not guaranteed. Void where prohibited.'"
      });

    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto w-full h-full flex flex-col">
      <header className="border-b border-neutral-800 pb-6 mb-8 flex justify-between items-end shrink-0">
        <div>
          <h2 className="text-4xl font-black tracking-tight text-white mb-2">JOBS & PIPELINE</h2>
          <p className="text-neutral-400">Monitor active orchestration jobs across all integrated tools.</p>
        </div>
        <div className="flex gap-4">
          <button 
            onClick={runJoeMotelTest}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded font-bold uppercase tracking-wider text-sm transition-colors"
          >
            <Film size={16} fill="currentColor" />
            EP01 JOE MOTEL TEST
          </button>
          <button 
            onClick={runLuckOfTheIrishTest}
            className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded font-bold uppercase tracking-wider text-sm transition-colors"
          >
            <Play size={16} fill="currentColor" />
            LUCK OF THE IRISH TEST
          </button>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
        {jobs.length === 0 ? (
          <div className="text-center text-neutral-500 py-12 border border-dashed border-neutral-800 rounded-xl">
            <Activity size={48} className="mx-auto mb-4 opacity-20" />
            <p className="font-mono text-sm tracking-widest">NO ACTIVE JOBS</p>
          </div>
        ) : (
          jobs.map(job => (
            <div key={job.id} className="bg-neutral-900 border border-neutral-800 rounded-xl p-5">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  {getStatusIcon(job.status)}
                  <h3 className="text-lg font-bold text-white font-mono uppercase">
                    {job.toolId} <span className="text-neutral-500">/</span> {job.operation}
                  </h3>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-neutral-500">ID: {job.id}</span>
                  <span className={`px-2 py-1 rounded text-[10px] font-bold tracking-widest border ${getStatusColor(job.status)}`}>
                    {job.status}
                  </span>
                </div>
              </div>

              {job.status === 'RUNNING' && (
                <div className="mb-4">
                  <div className="flex justify-between text-xs text-neutral-400 mb-1 font-mono">
                    <span>PROGRESS</span>
                    <span>{job.progress}%</span>
                  </div>
                  <div className="h-1.5 w-full bg-neutral-800 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-blue-500 transition-all duration-300 ease-out"
                      style={{ width: `${job.progress}%` }}
                    />
                  </div>
                </div>
              )}

              <div className="bg-black rounded-lg border border-neutral-800 p-3 max-h-32 overflow-y-auto font-mono text-xs text-neutral-400 space-y-1">
                {job.logs.map((log, i) => (
                  <div key={i} className="flex gap-2">
                    <span className="text-neutral-600 shrink-0">&gt;</span>
                    <span className={log.includes('successfully') ? 'text-emerald-400' : ''}>{log}</span>
                  </div>
                ))}
              </div>
              
              {job.outputs && (
                <div className="mt-4 pt-4 border-t border-neutral-800 flex items-center justify-between">
                  <div className="text-sm">
                    <span className="text-neutral-500 mr-2">Result Asset:</span>
                    <span className="font-mono text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded">{job.outputs.assetId}</span>
                  </div>
                  <button className="text-xs bg-neutral-800 hover:bg-neutral-700 text-white px-3 py-1.5 rounded transition-colors">
                    VIEW ASSET
                  </button>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
