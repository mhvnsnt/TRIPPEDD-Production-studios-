const fs = require('fs');
let testCode = fs.readFileSync('src/core/adapters/__tests__/toolchain.test.ts', 'utf8');

testCode = testCode.replace("const fakeCsv = \\`Timecode List:", "const fakeCsv = `Timecode List:");
testCode = testCode.replace("2,240,00:00:10.000,10.0,480,00:00:20.000,20.0,240,00:00:10.000,10.0\\`;", "2,240,00:00:10.000,10.0,480,00:00:20.000,20.0,240,00:00:10.000,10.0`;");

fs.writeFileSync('src/core/adapters/__tests__/toolchain.test.ts', testCode);
