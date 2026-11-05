/**
 * Read names.txt, flag lines starting with a keyword, write annotated copy.
 */
const fs = require('fs');
const path = require('path');

const NAMES_IN = path.join(__dirname, 'data', 'names.txt');
const NAMES_OUT = path.join(__dirname, 'output', 'names_annotated.txt');
const KEYWORD = 'ERROR';

function annotateNames(keyword = KEYWORD, infile = NAMES_IN, outfile = NAMES_OUT) {
    const data = fs.readFileSync(infile);
    const lines = data.split('\n');
    const output = [];
    for (const line of lines) {
        if (line.startsWith(keyword)) {
            output.push(keyword + ' [FLAGGED]');
        } else {
            output.push(line);
        }
    }
    fs.writeFileSync(outfile, output.join('\n'), 'ascii');
}

module.exports = { annotateNames };
