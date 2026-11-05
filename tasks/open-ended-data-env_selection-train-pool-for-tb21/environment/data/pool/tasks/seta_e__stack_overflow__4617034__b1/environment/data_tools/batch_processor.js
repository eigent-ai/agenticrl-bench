/**
 * Merge a variable list of batch data files into one combined output.
 */
const path = require('path');
const fs = require('fs');
const glob = require('glob');

const BATCH_DIR = path.join(__dirname, 'data', 'batch');
const BATCH_OUT = path.join(__dirname, 'output', 'batch_combined.txt');

function mergeBatch(filenames, outfile = BATCH_OUT) {
    let combined = '';
    for (const f of filenames) {
        combined += fs.readFileSync(f, 'utf-8');
    }
    fs.writeFileSync(outfile, combined, 'utf-8');
}

function run() {
    const files = glob.sync(path.join(BATCH_DIR, '*.txt')).sort();
    mergeBatch(files);
}

module.exports = { mergeBatch, run };
