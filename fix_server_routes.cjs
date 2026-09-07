const fs = require('fs');
let srv = fs.readFileSync('server.ts', 'utf8');

// The route wasn't in server.ts, it was queueManager routes?
// Actually in queueManager.ts, is there a Router?
// Wait, the API routes for queue are in server.ts currently!
// Oh, the user mentioned queueManager.ts handles queue logic. Let's see what's in server.ts for api/queue.

if(!srv.includes('app.get("/api/queue"')) {
   console.log('No /api/queue in server.ts? Let us add it.');
   srv = srv.replace('app.use(express.json());', 'app.use(express.json());\n\n  app.get("/api/queue", (req, res) => {\n    res.json(queueManager.getJobs());\n  });\n\n  app.post("/api/queue/scan", async (req, res) => {\n    const folderId = req.body.folderId;\n    const token = req.headers.authorization?.split(" ")[1];\n    if(!token) return res.status(401).send();\n    queueManager.startScan(folderId, token);\n    res.json({ status: "started" });\n  });\n\n  app.get("/api/tools", (req, res) => {\n    res.json(toolManager.getAllTools());\n  });');
}
fs.writeFileSync('server.ts', srv);
