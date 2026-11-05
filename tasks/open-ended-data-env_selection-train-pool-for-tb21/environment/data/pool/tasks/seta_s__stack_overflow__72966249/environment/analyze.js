// analyze.js
const fs = require('fs');
const path = require('path');
const { isoToCar } = require('./lib/isometric');

const sessionPath = path.join(__dirname, 'data', 'session.json');
const outputPath  = path.join(__dirname, 'data', 'output.json');

const session = JSON.parse(fs.readFileSync(sessionPath, 'utf8'));

const results = session.map(click => {
  const [col, row] = isoToCar(click.screenX, click.screenY);
  return { id: click.id, col, row };
});

fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
console.log(`Processed ${results.length} clicks -> ${outputPath}`);
