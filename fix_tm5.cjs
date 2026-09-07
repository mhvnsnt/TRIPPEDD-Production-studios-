const fs = require('fs');

let tm = fs.readFileSync('src/components/ToolManager.tsx', 'utf8');

// There are probably multiple cases of AVAILABLE or NOT_AVAILABLE or something. We need to be careful with replace
// Let's just rewrite the switch statement for getStatusBadge
tm = tm.replace(/switch \(status\) \{[\s\S]*?default:/, `switch (status) {
      case 'AVAILABLE':
        return <span className="bg-emerald-500/10 text-emerald-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-emerald-500/20"><CheckCircle2 size={12} /> {status}</span>;
      case 'INSTALLING':
        return <span className="bg-blue-500/10 text-blue-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-blue-500/20"><RefreshCw className="animate-spin" size={12} /> {status}</span>;
      case 'ERROR':
      case 'VERSION_UNSUPPORTED':
        return <span className="bg-neutral-800 text-neutral-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-neutral-700"> {status}</span>;
      case 'UNAVAILABLE':
        return <span className="bg-amber-500/10 text-amber-500 px-2 py-1 rounded text-xs font-bold flex items-center gap-1 border border-amber-500/20"><AlertCircle size={12} /> NOT AVAILABLE</span>;
      default:`);
      
fs.writeFileSync('src/components/ToolManager.tsx', tm);
