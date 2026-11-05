const fs = require('fs');
const path = require('path');
const { createChart } = require('./src/chart');
const { addAxis } = require('./src/axis');
const config = require('./config.json');

const outputDir = path.join(__dirname, 'output');
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

const { svg, scale, dom } = createChart(config);
addAxis(svg, scale, config);

const svgEl = dom.window.document.querySelector('svg');
const serializer = new dom.window.XMLSerializer();
const svgContent = serializer.serializeToString(svgEl);
const outputPath = path.join(outputDir, 'calendar.svg');
fs.writeFileSync(outputPath, svgContent);

console.log('Chart generated at:', outputPath);
