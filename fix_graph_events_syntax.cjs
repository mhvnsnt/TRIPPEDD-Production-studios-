const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

// The file currently has: this.events.push({ id: crypto.randomUUID(), ...{
// We want to change it to: this.events.push({ id: crypto.randomUUID(), ... (and then add ) at end? No, just id, then the rest.
// Wait, if it's:
// this.events.push({ id: crypto.randomUUID(), ...{
//   foo: 'bar'
// });
// We can change it to:
// this.events.push({ id: crypto.randomUUID(), 

content = content.replace(/this\.events\.push\(\{ id: crypto\.randomUUID\(\), \.\.\.\{/g, 'this.events.push({ id: crypto.randomUUID(), ');

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);

console.log("Fixed syntax");
