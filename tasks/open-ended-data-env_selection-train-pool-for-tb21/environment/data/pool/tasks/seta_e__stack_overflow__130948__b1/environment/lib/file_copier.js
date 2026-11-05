const fs = require('fs');

function copyFile(src, dest) {
  const content = fs.readFileSync(src, 'utf-8');
  fs.writeFileSync(dest, content, 'utf-8');
}

module.exports = { copyFile };
