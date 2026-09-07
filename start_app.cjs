const { exec } = require('child_process');

console.log("Building app...");
const build = exec("npm run build");
build.stdout.on("data", (data) => console.log(data.toString()));
build.stderr.on("data", (data) => console.error(data.toString()));
build.on("exit", (code) => {
  if (code === 0) {
    console.log("Build successful. Triggering restart_dev_server...");
    // Let the main agent process trigger the restart.
  }
});
