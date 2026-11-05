#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const normalize = require('./lib/normalize');
const collapse = require('./lib/collapse');
const wordwrap = require('./lib/wordwrap');

function printHelp() {
  console.log([
    'Usage: node format-text.js [--width N] <file>',
    '',
    'Processes a plain-text document through three stages:',
    '  1. Normalize all line endings to \\r\\n',
    '  2. Collapse excessive blank lines:',
    '     - 4+ consecutive newlines become 2 (one blank line)',
    '     - Exactly 2 consecutive newlines become 1 (no blank line)',
    '     - Single newlines are preserved',
    '  3. Word-wrap lines to the specified width at word boundaries',
    '',
    'Options:',
    '  --width N   Set the wrap width (default: 72)',
    '  --help      Show this help message'
  ].join('\n'));
}

var args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  printHelp();
  process.exit(0);
}

var width = 72;
var filePath = null;

for (var i = 0; i < args.length; i++) {
  if (args[i] === '--width' && i + 1 < args.length) {
    width = parseInt(args[i + 1], 10);
    i++;
  } else if (!args[i].startsWith('--')) {
    filePath = args[i];
  }
}

if (!filePath) {
  console.error('Error: No input file specified.');
  printHelp();
  process.exit(1);
}

var resolvedPath = path.resolve(filePath);
if (!fs.existsSync(resolvedPath)) {
  console.error('Error: File not found: ' + resolvedPath);
  process.exit(1);
}

var text = fs.readFileSync(resolvedPath, 'utf8');

text = wordwrap(text, width);
text = normalize(text);
text = collapse(text);

process.stdout.write(text);
