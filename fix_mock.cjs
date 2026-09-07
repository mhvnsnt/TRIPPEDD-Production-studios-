const fs = require('fs');
let testCode = fs.readFileSync('src/core/pipeline/__tests__/mediaIngest.test.ts', 'utf8');

testCode = testCode.replace(
  "ToolchainOrchestrator: vi.fn().mockImplementation(() => {",
  "ToolchainOrchestrator: class { constructor() {}"
);
testCode = testCode.replace(
  "analyzeFile: vi.fn().mockImplementation(async (filePath: string) => {",
  "async analyzeFile(filePath: string) {"
);
testCode = testCode.replace(
  "});\n      };\n    })",
  "}\n    }"
);

fs.writeFileSync('src/core/pipeline/__tests__/mediaIngest.test.ts', testCode);
