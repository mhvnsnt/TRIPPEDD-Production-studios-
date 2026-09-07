const fs = require('fs');

let content = fs.readFileSync('src/core/pipeline/physicalTimeline.ts', 'utf8');

content = content.replace("import { episodes } from './episodes';", "import { EpisodeRegistry } from './episodes';");
content = content.replace("const episode = episodes.find(e => e.id === episodeId);", "const episode = EpisodeRegistry.getEpisode(episodeId);");

fs.writeFileSync('src/core/pipeline/physicalTimeline.ts', content);
