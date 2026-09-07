const fs = require('fs');
let content = fs.readFileSync('src/core/types.ts', 'utf8');

content = content.replace(
  "| 'APPROVAL_GRANTED' | 'APPROVAL_REVOKED' | 'DELIVERY_CREATED'",
  "| 'APPROVAL_GRANTED' | 'APPROVAL_REVOKED' | 'DELIVERY_CREATED' | 'PRODUCTION_CREATED_FROM_SEED'"
);

fs.writeFileSync('src/core/types.ts', content);
