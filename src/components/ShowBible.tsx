import { Users, MapPin, Film } from 'lucide-react';

export function ShowBible() {
  return (
    <div className="p-8 max-w-6xl mx-auto w-full space-y-8">
      <header className="border-b border-neutral-800 pb-6 flex justify-between items-end">
        <div>
          <h2 className="text-4xl font-black tracking-tight text-white mb-2">SHOW BIBLE</h2>
          <p className="text-neutral-400">The TRIPPEDD universe database.</p>
        </div>
        <button className="bg-neutral-800 hover:bg-neutral-700 text-white px-4 py-2 rounded font-bold text-sm transition-colors border border-neutral-700">
          + ADD ENTRY
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Characters */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-white font-bold tracking-widest border-b border-neutral-800 pb-2">
            <Users size={18} />
            CHARACTERS
          </div>
          <div className="space-y-3">
            <EntryCard 
              title="YOU" 
              subtitle="Main Character"
              desc="Chaotic. Overconfident. Deadpan when appropriate." 
            />
            <EntryCard 
              title="TYNESHIA" 
              subtitle="Main Character"
              desc="Grounded. Unimpressed. Escalates selectively." 
            />
          </div>
        </div>

        {/* Locations */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-white font-bold tracking-widest border-b border-neutral-800 pb-2">
            <MapPin size={18} />
            LOCATIONS
          </div>
          <div className="space-y-2">
            {['MOTEL 6', 'GAS STATION', 'CARTWRIGHT ST', 'RIVERGATE', 'FAST FOOD STRIP', 'UE5 CYBERPUNK CITY', 'HORROR WOODS', 'ANIME ARENA'].map(loc => (
              <div key={loc} className="bg-neutral-900 border border-neutral-800 p-3 rounded text-sm font-mono text-neutral-300">
                {loc}
              </div>
            ))}
          </div>
        </div>

        {/* Genres */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-white font-bold tracking-widest border-b border-neutral-800 pb-2">
            <Film size={18} />
            GENRE PRESETS
          </div>
          <div className="space-y-3">
            <PresetCard title="HORROR" items={['ColorGrade', 'Sound', 'Camera', 'FilmGrain', 'Transitions']} />
            <PresetCard title="ANIME" items={['ColorGrade', 'ImpactFrames', 'SpeedLines', 'SFX']} />
            <PresetCard title="WRESTLING" items={['ArenaLighting', 'Crowd', 'Graphics', 'SFX']} />
            <PresetCard title="SITCOM" items={['Lighting', 'Camera', 'LaughTrack', 'TitleCard']} />
          </div>
        </div>

      </div>
    </div>
  );
}

function EntryCard({ title, subtitle, desc }: any) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 p-4 rounded-lg">
      <h4 className="text-white font-black text-lg">{title}</h4>
      <div className="text-blue-500 text-xs font-mono mb-2">{subtitle}</div>
      <p className="text-neutral-400 text-sm leading-relaxed">{desc}</p>
    </div>
  );
}

function PresetCard({ title, items }: any) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 p-4 rounded-lg">
      <h4 className="text-white font-black tracking-wider mb-3">{title}</h4>
      <div className="flex flex-wrap gap-2">
        {items.map((item: string) => (
          <span key={item} className="bg-neutral-950 border border-neutral-800 text-neutral-400 px-2 py-1 rounded text-xs font-mono">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}
