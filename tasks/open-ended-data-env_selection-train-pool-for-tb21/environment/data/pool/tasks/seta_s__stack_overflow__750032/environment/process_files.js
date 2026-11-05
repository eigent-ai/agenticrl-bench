'use strict';

const fs = require('fs');
const path = require('path');

const DATA_DIR = './data';
const OUTPUT_FILE = './output/report.json';

function processTextFile(filePath) {
  const content = fs.readFileSync(filePath);
  const lines = content.split('\n').filter(l => l.trim() !== '');
  const words = lines.flatMap(l => l.trim().split(/\s+/).filter(w => w !== ''));
  const longest_word = words.reduce((max, w) => w.length > max.length ? w : max);
  return { lines: lines.length, words: words.length, longest_word };
}

function processCsvFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const rows = content.trim().split('\n').map(r => r.split(','));
  const total = rows.reduce((sum, row) => sum + parseFloat(row[1]), 0);
  return { rows: rows.length, total };
}

const report = { txt_files: {}, csv_files: {} };
const files = fs.readdirSync(DATA_DIR).sort();

for (const file of files) {
  const filePath = path.join(DATA_DIR, file);
  const ext = path.extname(file);
  if (ext === '.txt') {
    report.txt_files[file] = processTextFile(filePath);
  } else if (ext === '.csv') {
    report.csv_files[file] = processCsvFile(filePath);
  }
}

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(report, null, 2));
console.log('Report written to', OUTPUT_FILE);
