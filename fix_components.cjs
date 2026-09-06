const fs = require('fs');

function replaceInFile(file, regex, replacement) {
    let content = fs.readFileSync(file, 'utf8');
    content = content.replace(regex, replacement);
    fs.writeFileSync(file, content);
}

replaceInFile('src/components/ActiveProduction.tsx', /activeRecord\.provenance/g, "activeRecord.provenance.aggregate");
replaceInFile('src/components/Dashboard.tsx', /r\.provenance\.includes/g, "r.provenance.aggregate.includes");
replaceInFile('src/components/Dashboard.tsx', /r\.provenance === /g, "r.provenance.aggregate === ");
replaceInFile('src/components/StoryWorkspace.tsx', /selectedStory\.provenance \|\| 'USER_CREATED'/g, "selectedStory.provenance?.aggregate || 'USER_CREATED'");

replaceInFile('src/components/JobsPipeline.tsx', /provenance: 'REAL_PRODUCTION'/g, "provenance: { realityStatus: 'FACTUAL', captureStatus: 'DIRECTLY_CAPTURED', authorship: 'USER_AUTHORED', generationMethods: ['LIVE_CAPTURE'], assemblyMode: 'PURE_LIVE_ACTION', aiContributions: ['NONE'], aggregate: 'REAL_PRODUCTION' }");
replaceInFile('src/components/JobsPipeline.tsx', /provenance: 'FICTIONAL_CREATION'/g, "provenance: { realityStatus: 'FICTIONAL', captureStatus: 'NOT_CAPTURED', authorship: 'AI_AUTHORED', generationMethods: ['AI_GENERATED'], assemblyMode: 'PURE_GENERATED', aiContributions: ['AI_CO_GENERATED'], aggregate: 'FICTIONAL_CREATION' }");

replaceInFile('src/components/AssetWorkspace.tsx', /ProvenanceType/g, "AggregateClassification");
replaceInFile('src/components/AssetWorkspace.tsx', /filterProvenance === 'ALL' \|\| asset\.provenance === filterProvenance/g, "filterProvenance === 'ALL' || asset.provenance.aggregate === filterProvenance");
replaceInFile('src/components/AssetWorkspace.tsx', /asset\.provenance/g, "asset.provenance.aggregate");
replaceInFile('src/components/AssetWorkspace.tsx', /selectedAsset\.provenance\.aggregate/g, "selectedAsset.provenance.aggregate");

