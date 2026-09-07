const fs = require('fs');
let types = fs.readFileSync('src/core/types.ts', 'utf8');

types = types.replace(
  "parentObservationIds?: string[]; // For split/merge lineage",
  "parentObservationIds?: string[]; // For split/merge lineage\n  toolProvenance?: import('./adapters/types').ToolExecutionResult; // Metadata on the actual tool run that generated this"
);

fs.writeFileSync('src/core/types.ts', types);
console.log("Types updated with toolProvenance.");
