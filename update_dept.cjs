const fs = require('fs');
let content = fs.readFileSync('src/core/types.ts', 'utf8');

content = content.replace(
  "export type Department = \n  | 'DEVELOPMENT' | 'WRITING' | 'PRODUCTION' | 'CASTING' \n  | 'DIRECTING' | 'CAMERA' | 'LIGHTING' | 'SOUND' \n  | 'ART' | 'WARDROBE' | 'HAIR_MAKEUP' | 'EDITORIAL' \n  | 'ANIMATION' | 'VFX' | 'MUSIC' | 'COLOR' | 'GRAPHICS' \n  | 'DELIVERY' | 'PRODUCTION_MANAGEMENT' | 'LEGAL' | 'BUSINESS';",
  "export type Department = \n  | 'DEVELOPMENT' | 'WRITING' | 'PRODUCTION' | 'CASTING' \n  | 'DIRECTING' | 'CAMERA' | 'LIGHTING' | 'SOUND' \n  | 'ART' | 'PROPS' | 'WARDROBE' | 'HAIR_MAKEUP' | 'GRIP' | 'ELECTRIC' | 'SCRIPT' | 'EDITORIAL' \n  | 'ASSISTANT_EDITOR' | 'ANIMATION' | 'VFX' | 'MUSIC' | 'COLOR' | 'GRAPHICS' \n  | 'QC' | 'DELIVERY' | 'PRODUCTION_MANAGEMENT' | 'BUSINESS' | 'LEGAL';"
);

// We should also check ProductionEventType and append the new ones.
//  - WORK_ORDER_CREATED
//  - WORK_ORDER_SCHEDULED
//  - WORK_ORDER_STARTED
//  - WORK_ORDER_BLOCKED
//  - WORK_ORDER_COMPLETED
//  - WORK_ORDER_CANCELLED
//  - CREW_ASSIGNED
//  - CREW_CONFIRMED
//  - CREW_RELEASED
//  - SCHEDULE_CONFLICT_DETECTED

content = content.replace(
  "| 'TAKE_CREATED';",
  "| 'TAKE_CREATED'\n  | 'WORK_ORDER_CREATED' | 'WORK_ORDER_SCHEDULED' | 'WORK_ORDER_STARTED' | 'WORK_ORDER_BLOCKED' | 'WORK_ORDER_COMPLETED' | 'WORK_ORDER_CANCELLED'\n  | 'CREW_ASSIGNED' | 'CREW_CONFIRMED' | 'CREW_RELEASED' | 'SCHEDULE_CONFLICT_DETECTED';"
);

fs.writeFileSync('src/core/types.ts', content);
