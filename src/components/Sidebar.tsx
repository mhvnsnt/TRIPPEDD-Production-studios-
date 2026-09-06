import {
  Film,
  LayoutDashboard,
  BookOpen,
  Wand2,
  Video,
  MonitorPlay,
  Settings,
  FolderOpen
} from 'lucide-react';

export function Sidebar({ currentView, setCurrentView }: { currentView: string, setCurrentView: (v: string) => void }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'production', label: 'Active Production', icon: Film },
    { id: 'bible', label: 'Show Bible', icon: BookOpen },
    { id: 'ailab', label: 'AI Lab', icon: Wand2 },
    { id: 'ue5', label: 'Virtual Production', icon: MonitorPlay },
    { id: 'assets', label: 'Asset Library', icon: FolderOpen },
  ];

  return (
    <div className="w-64 h-screen bg-neutral-900 border-r border-neutral-800 flex flex-col text-neutral-300">
      <div className="p-6 border-b border-neutral-800">
        <h1 className="text-2xl font-black tracking-tighter text-white uppercase flex flex-col">
          <span>TRIPPEDD</span>
          <span className="text-xs text-neutral-500 font-medium tracking-[0.2em] mt-1">REALITY IS OPTIONAL.</span>
        </h1>
      </div>
      
      <nav className="flex-1 py-6 px-4 space-y-1 overflow-y-auto">
        <div className="text-xs font-bold text-neutral-600 mb-4 tracking-widest px-3 mt-4">STUDIO OS</div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentView(item.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-md transition-colors ${
                isActive 
                  ? 'bg-neutral-800 text-white' 
                  : 'hover:bg-neutral-800/50 hover:text-white'
              }`}
            >
              <Icon size={18} className={isActive ? 'text-blue-500' : 'text-neutral-400'} />
              <span className="font-medium text-sm">{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-neutral-800">
        <button className="w-full flex items-center space-x-3 px-3 py-2 text-neutral-400 hover:text-white transition-colors">
          <Settings size={18} />
          <span className="font-medium text-sm">Settings</span>
        </button>
      </div>
    </div>
  );
}
