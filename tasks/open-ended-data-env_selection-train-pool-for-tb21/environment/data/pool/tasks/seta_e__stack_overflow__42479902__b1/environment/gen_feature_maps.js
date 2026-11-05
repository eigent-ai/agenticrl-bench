const fs = require('fs');
const data = new Float32Array(3200);
for (let i = 0; i < 3200; i++) data[i] = i;
fs.writeFileSync('/app/feature_maps.bin', Buffer.from(data.buffer));
