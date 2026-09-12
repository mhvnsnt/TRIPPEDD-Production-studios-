import fs from 'fs/promises';
import path from 'path';

const root = process.cwd();
const lockPath = path.join(root, 'production', 'EP01', 'EDITORIAL-LOCK.json');
const qcPath = path.join(root, 'production', 'EP01', 'QC-PASS.json');
const outputPath = path.join(root, 'production', 'EP01', 'SHOWRUNNER-GREENLIGHT.json');

if (process.env.CONFIRM_EP01 !== 'YES') {
  console.error('EP01 greenlight requires explicit confirmation: CONFIRM_EP01=YES');
  process.exitCode = 2;
} else {
  const lock = JSON.parse(await fs.readFile(lockPath, 'utf8'));
  const qc = JSON.parse(await fs.readFile(qcPath, 'utf8'));
  if (!lock.approved || qc.status !== 'PASS') {
    console.error('EP01 cannot be greenlit: editorial lock must be approved and QC must PASS.');
    process.exitCode = 2;
  } else {
    const greenlight = {
      episodeId: 'EP01',
      status: 'GREENLIT',
      approvedBy: 'SHOWRUNNER',
      approvedAt: new Date().toISOString(),
      editorialLock: path.relative(root, lockPath),
      qcRecord: path.relative(root, qcPath),
      note: 'Explicit showrunner authorization for final render. This does not alter physical source evidence.'
    };
    await fs.writeFile(outputPath, JSON.stringify(greenlight, null, 2));
    console.log(JSON.stringify(greenlight, null, 2));
  }
}
