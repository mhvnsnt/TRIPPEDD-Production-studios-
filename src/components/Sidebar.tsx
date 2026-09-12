import { Users, Film, LayoutDashboard, BookOpen, Wand2, Video, MonitorPlay, Settings, Search, FolderOpen, Wrench, PenTool, Image as ImageIcon, Mic, Clapperboard, Menu, ChevronLeft, ChevronRight, Activity, Layers, Scissors } from 'lucide-react';
import { useState, useEffect } from 'react';
import { motion } from 'motion/react';

export function Sidebar({ currentView, setCurrentView }: { currentView: string, setCurrentView: (v: string) => void }) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  useEffect(() => { const saved = localStorage.getItem('sidebar_collapsed'); if (saved) setIsCollapsed(saved === 'true'); }, []);
  const toggleCollapsed = () => { const next = !isCollapsed; setIsCollapsed(next); localStorage.setItem('sidebar_collapsed', String(next)); };
  const NavGroup = ({ title, items }: any) => <div className="mb-6">{!isCollapsed && <div className="text-[10px] font-bold text-neutral-600 mb-2 tracking-widest px-3 uppercase">{title}</div>}<div className="space-y-0.5">{items.map((item: any) => { const Icon = item.icon; const isActive = currentView === item.id; return <button key={item.id} onClick={() => setCurrentView(item.id)} title={isCollapsed ? item.label : undefined} className={`w-full flex items-center px-3 py-2.5 rounded-md transition-colors relative group ${isActive ? 'bg-neutral-800 text-white' : 'hover:bg-neutral-800/50 hover:text-white'} ${isCollapsed ? 'justify-center' : 'space-x-3'}`}><Icon size={18} className={isActive ? 'text-blue-500' : 'text-neutral-400'} />{!isCollapsed && <span className="font-medium text-sm">{item.label}</span>}{isCollapsed && <div className="absolute left-full ml-2 px-2 py-1 bg-neutral-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-50">{item.label}</div>}</button>; })}</div></div>;
  const studioItems = [
    { id: 'make_show', label: 'Make The Show', icon: Clapperboard },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'studio_ops', label: 'Studio Operations', icon: Users },
    { id: 'story', label: 'Story / Fiction', icon: PenTool },
    { id: 'episodes', label: 'Episode Pipeline', icon: Film },
    { id: 'bible', label: 'Show Bible', icon: BookOpen },
      { id: 'formats', label: 'Formats & Lore', icon: BookOpen },
    { id: 'production', label: 'Active Production', icon: Clapperboard },
    { id: 'ingest', label: 'Media Ingest', icon: Video },
    { id: 'physical_evidence', label: 'Evidence Review', icon: Search },
    { id: 'editorial_review', label: 'Editorial Review', icon: Scissors },
    { id: 'assets', label: 'Assets', icon: FolderOpen },
    { id: 'ailab', label: 'AI Lab', icon: Wand2 },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard }, { id: 'studio_ops', label: 'Studio Operations', icon: Users },
    { id: 'story', label: 'Story / Fiction', icon: PenTool }, { id: 'episodes', label: 'Episode Pipeline', icon: Film }, { id: 'bible', label: 'Show Bible', icon: BookOpen },
    { id: 'formats', label: 'Formats & Lore', icon: BookOpen }, { id: 'production', label: 'Active Production', icon: Clapperboard }, { id: 'pilot_build', label: 'EP01 Pilot Build', icon: Film },
    { id: 'ingest', label: 'Media Ingest', icon: Video }, { id: 'physical_evidence', label: 'Evidence Review', icon: Search }, { id: 'assets', label: 'Assets', icon: FolderOpen }, { id: 'ailab', label: 'AI Lab', icon: Wand2 },
  ];
  const toolItems = [
    { id: 'tool_video', label: 'Video Edit', icon: Clapperboard }, { id: 'tool_comfy', label: 'ComfyUI', icon: Layers }, { id: 'tool_blender', label: 'Blender', icon: MonitorPlay },
    { id: 'tool_unreal', label: 'Unreal', icon: MonitorPlay }, { id: 'tool_audio', label: 'Audio', icon: Mic }, { id: 'tool_capture', label: 'Capture', icon: Video }, { id: 'tool_2d', label: '2D / Graphics', icon: ImageIcon },
  ];
  const systemItems = [{ id: 'jobs', label: 'Jobs & Pipeline', icon: Activity }, { id: 'tool_manager', label: 'Tool Manager', icon: Wrench }, { id: 'settings', label: 'Settings', icon: Settings }];
  return <motion.div initial={false} animate={{ width: isCollapsed ? '64px' : '256px' }} transition={{ duration: 0.2, ease: 'easeInOut' }} className="h-screen bg-neutral-900 border-r border-neutral-800 flex flex-col text-neutral-300 relative z-20 shrink-0">
    <div className={`p-4 border-b border-neutral-800 flex items-center ${isCollapsed ? 'justify-center' : 'justify-between'}`}>{!isCollapsed && <h1 className="text-xl font-black tracking-tighter text-white uppercase flex flex-col overflow-hidden"><span>TRIPPEDD</span></h1>}<button onClick={toggleCollapsed} className="text-neutral-500 hover:text-white p-1 rounded hover:bg-neutral-800 transition-colors">{isCollapsed ? <Menu size={20} /> : <ChevronLeft size={20} />}</button></div>
    <nav className="flex-1 py-4 px-2 overflow-y-auto overflow-x-hidden custom-scrollbar"><NavGroup title="Studio" items={studioItems} /><NavGroup title="Tools" items={toolItems} /><NavGroup title="System" items={systemItems} /></nav>
  </motion.div>;
}
