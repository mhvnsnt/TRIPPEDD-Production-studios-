import { Play, Settings2, SlidersHorizontal, Wand2, ShieldAlert, Sparkles, Image as ImageIcon, Database } from 'lucide-react';
import { useState } from 'react';
import { useProduction } from '../context';

type LabMode = 'CREATE' | 'TRANSFORM' | 'PRODUCTION';

export function AILab() {
  const [activeMode, setActiveMode] = useState<LabMode>('CREATE');
  const [activePreset, setActivePreset] = useState('ANIME');
  const [prompt, setPrompt] = useState('');
  
  const { records } = useProduction();
  const presets = ['ANIME', 'HORROR', 'CLAY', 'COMIC', 'CYBERPUNK', 'VHS'];
  
  // Data access based on mode
  const verifiedShots = records.filter(r => r.type === 'SHOT' && r.verified && r.status === 'COMPLETED');
  const allMedia = records.filter(r => r.type === 'SHOT' || r.type === 'VFX');

  const canGenerate = 
    activeMode === 'CREATE' ? prompt.length > 0 :
    activeMode === 'TRANSFORM' ? allMedia.length > 0 :
    activeMode === 'PRODUCTION' ? verifiedShots.length > 0 : false;

  return (
    <div className="p-8 max-w-6xl mx-auto w-full space-y-8">
      <header className="border-b border-neutral-800 pb-6 flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black tracking-tight text-white mb-2">AI LAB</h2>
          <p className="text-neutral-400">Generative creation and transformation pipeline.</p>
        </div>
        
        <div className="flex bg-neutral-900 rounded-lg p-1 border border-neutral-800">
          <ModeTab 
            active={activeMode === 'CREATE'} 
            onClick={() => setActiveMode('CREATE')} 
            icon={Sparkles} 
            label="CREATE" 
          />
          <ModeTab 
            active={activeMode === 'TRANSFORM'} 
            onClick={() => setActiveMode('TRANSFORM')} 
            icon={ImageIcon} 
            label="TRANSFORM" 
          />
          <ModeTab 
            active={activeMode === 'PRODUCTION'} 
            onClick={() => setActiveMode('PRODUCTION')} 
            icon={Database} 
            label="PRODUCTION" 
          />
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Source & Preview */}
        <div className="lg:col-span-8 space-y-6">
          <div className="grid grid-cols-2 gap-4">
            
            <div className="space-y-2">
              <div className="text-xs font-bold text-neutral-500 tracking-widest flex items-center justify-between">
                {activeMode === 'CREATE' ? 'PROMPT / CONCEPT' : 'SOURCE MEDIA'}
                {activeMode === 'PRODUCTION' && <span className="bg-emerald-900/30 text-emerald-500 px-2 py-0.5 rounded border border-emerald-900/50">{verifiedShots.length} VERIFIED</span>}
              </div>
              
              <div className="aspect-video bg-neutral-900 border border-neutral-800 rounded-lg flex flex-col items-center justify-center p-6 text-center relative overflow-hidden">
                {activeMode === 'CREATE' ? (
                  <textarea 
                    className="absolute inset-0 w-full h-full bg-transparent p-6 text-white resize-none outline-none font-mono text-sm placeholder-neutral-700"
                    placeholder="Enter prompt for fictional generation... (e.g. 'A wide cinematic shot of two idiots in a demon-run convenience store, glowing neon, hyper-detailed')"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                  />
                ) : activeMode === 'PRODUCTION' ? (
                  verifiedShots.length > 0 ? (
                    <span className="text-neutral-600 font-mono">SELECT VERIFIED TAKE</span>
                  ) : (
                    <>
                      <ShieldAlert size={32} className="text-amber-500/50 mb-3" />
                      <p className="text-sm font-medium text-neutral-400">No verified footage exists.</p>
                      <p className="text-xs text-neutral-500 mt-1 max-w-xs">Production mode strictly requires raw footage uploaded to the Terminal with verified evidence.</p>
                    </>
                  )
                ) : (
                  // TRANSFORM MODE
                  allMedia.length > 0 ? (
                    <span className="text-neutral-600 font-mono">SELECT ANY MEDIA (REAL OR FICTION)</span>
                  ) : (
                    <span className="text-neutral-600 font-mono">NO MEDIA AVAILABLE</span>
                  )
                )}
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="text-xs font-bold text-fuchsia-500 tracking-widest flex items-center justify-between">
                PREVIEW
                <span className="text-[10px] bg-neutral-900 text-neutral-500 px-2 py-0.5 rounded border border-neutral-800">
                  {activeMode === 'PRODUCTION' ? 'HYBRID_PRODUCTION' : 'FICTIONAL_CREATION'}
                </span>
              </div>
              <div className="aspect-video bg-black border border-neutral-800 rounded-lg flex items-center justify-center relative overflow-hidden">
                <span className="text-neutral-700 font-mono z-10">WAITING FOR INPUT</span>
              </div>
            </div>
          </div>
          
          <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
            <h3 className="text-sm font-bold text-white tracking-widest mb-4 flex items-center gap-2">
              <Settings2 size={16} />
              PIPELINE CONFIG
            </h3>
            <div className={`flex items-center gap-4 text-xs font-mono text-neutral-400 overflow-x-auto pb-2 ${activeMode === 'CREATE' ? '' : 'opacity-50'}`}>
              {activeMode !== 'CREATE' && (
                <>
                  <div className="flex-shrink-0 bg-neutral-950 px-3 py-2 rounded border border-neutral-800">Preprocess</div>
                  <span>→</span>
                  <div className="flex-shrink-0 bg-neutral-950 px-3 py-2 rounded border border-neutral-800">Pose / Edge</div>
                  <span>→</span>
                </>
              )}
              <div className="flex-shrink-0 bg-blue-900/30 text-blue-400 px-3 py-2 rounded border border-blue-900/50">
                {activeMode === 'CREATE' ? 'Text Encoder' : 'ControlNet'}
              </div>
              <span>→</span>
              <div className="flex-shrink-0 bg-fuchsia-900/30 text-fuchsia-400 px-3 py-2 rounded border border-fuchsia-900/50">Generative Model</div>
              <span>→</span>
              <div className="flex-shrink-0 bg-neutral-950 px-3 py-2 rounded border border-neutral-800">Upscale</div>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="lg:col-span-4 space-y-6 flex flex-col">
          <button 
            disabled={!canGenerate}
            className="w-full bg-fuchsia-600 hover:bg-fuchsia-500 disabled:bg-neutral-800 disabled:text-neutral-500 disabled:cursor-not-allowed text-white px-6 py-4 rounded-xl font-bold tracking-wide transition-colors flex items-center justify-center gap-2"
          >
            <Play size={18} fill="currentColor" />
            GENERATE {activeMode === 'PRODUCTION' ? 'HYBRID' : 'FICTION'}
          </button>

          <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 flex-1">
            <h3 className="text-sm font-bold text-white tracking-widest mb-4 flex items-center gap-2">
              <Wand2 size={16} />
              STYLE PRESETS
            </h3>
            <div className="grid grid-cols-2 gap-2 mb-6">
              {presets.map(preset => (
                <button
                  key={preset}
                  onClick={() => setActivePreset(preset)}
                  className={`py-2 text-xs font-bold tracking-wider rounded border transition-colors ${
                    activePreset === preset 
                      ? 'bg-fuchsia-500/10 text-fuchsia-400 border-fuchsia-500/50' 
                      : 'bg-neutral-950 text-neutral-400 border-neutral-800 hover:border-neutral-700'
                  }`}
                >
                  {preset}
                </button>
              ))}
            </div>

            <div className={`space-y-6 ${activeMode === 'CREATE' ? 'opacity-50 pointer-events-none' : ''}`}>
              <SliderControl label="Motion Preservation" value={activeMode === 'CREATE' ? 0 : 90} />
              <SliderControl label="Identity Preservation" value={activeMode === 'CREATE' ? 0 : 75} />
              <SliderControl label="Style Intensity" value={100} color="bg-fuchsia-500" />
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

function ModeTab({ active, onClick, icon: Icon, label }: any) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-md text-xs font-bold tracking-wider transition-colors ${
        active 
          ? 'bg-neutral-800 text-white' 
          : 'text-neutral-500 hover:text-neutral-300'
      }`}
    >
      <Icon size={14} />
      {label}
    </button>
  );
}

function SliderControl({ label, value, color = 'bg-blue-500' }: { label: string, value: number, color?: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs font-mono text-neutral-400 mb-2">
        <span>{label}</span>
        <span>{value}%</span>
      </div>
      <div className="w-full bg-neutral-950 h-2 rounded-full overflow-hidden border border-neutral-800">
        <div className={`h-full ${color}`} style={{ width: `${value}%` }}></div>
      </div>
    </div>
  );
}
