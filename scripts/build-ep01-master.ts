import { buildEp01FinalMaster } from '../src/server/ep01Master';

const manifest = await buildEp01FinalMaster();
console.log(JSON.stringify(manifest, null, 2));
process.exitCode = manifest.status === 'FINAL_MASTER_READY' ? 0 : 2;
