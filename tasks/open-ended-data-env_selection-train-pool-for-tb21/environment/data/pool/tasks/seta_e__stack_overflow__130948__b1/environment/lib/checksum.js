const fs = require('fs');
const crypto = require('crypto');

function computeChecksum(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  return crypto.createHash('sha256').update(content, 'utf-8').digest('hex');
}

module.exports = { computeChecksum };
