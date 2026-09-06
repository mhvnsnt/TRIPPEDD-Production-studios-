import { Play, CheckCircle2, Circle, Clock, Camera, Scissors, Sparkles, Box, Volume2, FileQuestion, Lightbulb, CalendarClock, Database, Clapperboard, PenTool } from 'lucide-react';
import { useProduction } from '../context';

export function Dashboard({ setCurrentView }: { setCurrentView: (v: string) => void }) {
  const { records } = useProduction();

  // REALITY DATABASE (Evidence-controlled production truth)
  const realityRecords = records.filter(r => r.contentType === 'REAL_PRODUCTION' || (r.contentType === 'HYBRID_PRODUCTION' && r.verified === true));
  const verifiedReality = realityRecords.filter(r => r.verified === true);
  const unverifiedReality = realityRecords.filter(r => r.verified === false);

  // FICTION DATABASE (Unrestricted creative generation)
  const fictionRecords = records.filter(r => r.contentType === 'FICTIONAL_CREATION');
  const generatedFiction = fictionRecords.filter(r => r.provenance.aggregate.includes('AI') || r.provenance.aggregate === 'GENERATED_FROM_FICTION');
  const userFiction = fictionRecords.filter(r => r.provenance.aggregate === 'USER_CREATED');

  // PLANNING & IDEATION
  const planningRecords = records.filter(r => r.contentType === 'PLAN' || r.contentType === 'IDEA');
  const plannedItems = planningRecords.filter(r => r.contentType === 'PLAN');
  const ideaItems = planningRecords.filter(r => r.contentType === 'IDEA');

  return (
    <div className="p-8 max-w-6xl mx-auto w-full space-y-8">
      <header className="flex justify-between items-end border-b border-neutral-800 pb-6">
        <div>
          <h2 className="text-4xl font-black tracking-tight text-white mb-2">STUDIO HUB</h2>
          <p className="text-neutral-400">Separate ledgers for Reality and Fiction.</p>
        </div>
        <button 
          onClick={() => setCurrentView('production')}
          className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded font-bold tracking-wide transition-colors flex items-center gap-2"
        >
          <Play size={18} fill="currentColor" />
          ENTER TRIPPEDD MODE
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* REALITY DATABASE Widget */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <div className="text-xs font-bold text-emerald-500 tracking-widest mb-1 flex items-center gap-2">
                <Database size={14} /> REALITY DATABASE
              </div>
              <h3 className="text-2xl font-bold text-white">EPISODE 01 — THE WALK</h3>
              <p className="text-xs text-neutral-500 mt-1">Evidence-controlled production truth.</p>
            </div>
            <div className="text-right">
              <div className="text-xl font-black text-white">
                {verifiedReality.length > 0 ? `${verifiedReality.length} VERIFIED` : '0 VERIFIED SHOTS'}
              </div>
              <div className="text-xs text-neutral-500">
                {verifiedReality.length > 0 ? 'PROGRESS ESTABLISHED' : 'PROGRESS NOT YET VERIFIED'}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <CategoryCard 
              icon={CheckCircle2} 
              title="VERIFIED PRODUCTION" 
              color="text-emerald-400"
              items={[
                `${verifiedReality.filter(r => r.type === 'SHOT').length} real shots`,
                `${verifiedReality.filter(r => r.type === 'EDIT').length} final edits`
              ]}
            />
            <CategoryCard 
              icon={ShieldAlertIcon} 
              title="AWAITING EVIDENCE" 
              color="text-amber-400"
              items={[
                `${unverifiedReality.length} claims pending`,
                `Requires raw uploads`
              ]}
            />
          </div>
        </div>

        {/* FICTION DATABASE Widget */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <div className="flex justify-between items-start mb-6">
            <div>
              <div className="text-xs font-bold text-fuchsia-500 tracking-widest mb-1 flex items-center gap-2">
                <Sparkles size={14} /> FICTION DATABASE
              </div>
              <h3 className="text-2xl font-bold text-white">ANTHOLOGY LORE</h3>
              <p className="text-xs text-neutral-500 mt-1">Unrestricted creative generation.</p>
            </div>
            <div className="text-right">
              <div className="text-xl font-black text-fuchsia-400">
                100% CREATED
              </div>
              <div className="text-xs text-neutral-500">
                NO EVIDENCE REQUIRED
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <CategoryCard 
              icon={PenTool} 
              title="STORY & LORE" 
              color="text-blue-400"
              items={[
                `${userFiction.filter(r => r.type === 'STORY' || r.type === 'CHARACTER').length} characters & stories`,
                `${fictionRecords.filter(r => r.type === 'WORLD').length} worlds defined`
              ]}
            />
            <CategoryCard 
              icon={Clapperboard} 
              title="GENERATED ASSETS" 
              color="text-fuchsia-400"
              items={[
                `${generatedFiction.filter(r => r.type === 'SCENE' || r.type === 'SHOT').length} generated scenes`,
                `${generatedFiction.length} total AI items`
              ]}
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Planner / Ideas */}
        <div className="md:col-span-2 bg-neutral-900 border border-neutral-800 rounded-xl p-6">
          <div className="flex justify-between items-end mb-6">
            <div>
              <h3 className="text-lg font-bold text-white mb-1">PLANNING & BLUEPRINTS</h3>
              <p className="text-xs text-neutral-500">Not tracked as completion until verified or generated.</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <CategoryCard 
              icon={CalendarClock} 
              title="PLANNED SHOOTS" 
              color="text-blue-400"
              items={[
                `${plannedItems.filter(r => r.type === 'SHOT').length} shots on call sheet`,
                `${plannedItems.filter(r => r.type === 'SCENE').length} scenes planned`
              ]}
            />
            <CategoryCard 
              icon={Lightbulb} 
              title="BRAINSTORM IDEAS" 
              color="text-amber-400"
              items={[
                `${ideaItems.length} ideas logged`
              ]}
            />
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 flex flex-col">
           <h3 className="text-lg font-bold text-white mb-4">QUICK ACTIONS</h3>
           <div className="space-y-3 flex-1">
             <ActionBtn label="+ VERIFY REAL TAKE" />
             <ActionBtn label="+ GENERATE FICTION" onClick={() => setCurrentView('ailab')} />
             <ActionBtn label="+ ADD IDEA" onClick={() => setCurrentView('bible')} />
           </div>
        </div>
      </div>

    </div>
  );
}

// Minimal missing icon placeholder
function ShieldAlertIcon({ size, className }: any) {
  return <FileQuestion size={size} className={className} />;
}

function CategoryCard({ icon: Icon, title, items, color }: any) {
  return (
    <div className="flex flex-col bg-neutral-950 p-4 rounded-lg border border-neutral-800">
      <div className="flex items-center gap-2 mb-3">
        <Icon size={16} className={color} />
        <div className={`text-[10px] font-bold tracking-widest ${color}`}>{title}</div>
      </div>
      <ul className="space-y-1">
        {items.map((item: string, i: number) => (
          <li key={i} className="text-xs text-neutral-400 font-mono">
            - {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ActionBtn({ label, onClick }: { label: string, onClick?: () => void }) {
  return (
    <button onClick={onClick} className="w-full text-left px-4 py-3 bg-neutral-950 hover:bg-neutral-800 border border-neutral-800 rounded font-mono text-sm text-neutral-300 transition-colors">
      {label}
    </button>
  );
}
