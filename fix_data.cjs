const fs = require('fs');

function defaultProvenance(type) {
    if (type === 'USER_CREATED') {
        return `{
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'USER_AUTHORED',
      generationMethods: [],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['NONE'],
      aggregate: 'IDEA'
    }`;
    }
    if (type === 'AI_ASSISTED') {
        return `{
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_ASSISTED',
      generationMethods: ['AI_ASSISTED'],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['AI_ASSISTED'],
      aggregate: 'IDEA'
    }`;
    }
    if (type === 'AI_GENERATED') {
        return `{
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'AI_AUTHORED',
      generationMethods: ['AI_GENERATED'],
      assemblyMode: 'PURE_GENERATED',
      aiContributions: ['AI_CO_GENERATED'],
      aggregate: 'FICTIONAL_CREATION'
    }`;
    }
    return `{
      realityStatus: 'UNKNOWN',
      captureStatus: 'UNKNOWN',
      authorship: 'UNKNOWN',
      generationMethods: [],
      assemblyMode: 'MIXED_MEDIA',
      aiContributions: ['NONE'],
      aggregate: 'IDEA'
    }`;
}

let content = fs.readFileSync('src/data.ts', 'utf8');

content = content.replace(/provenance: '([^']+)'/g, (match, p1) => {
    return `provenance: ${defaultProvenance(p1)}`;
});

fs.writeFileSync('src/data.ts', content);
