#!/usr/bin/env node
/**
 * Log analysis pipeline: reads input log files and produces a summary report.
 */
const fs = require('fs');
const path = require('path');

const INPUT_DIR = '/srv/pipeline/input/';
const OUTPUT_DIR = '/srv/pipeline/output/processed/results/';

function findInputFiles(directory) {
    return fs.readdirSync(directory)
        .filter(f => f.endsWith('.log'))
        .map(f => path.join(directory, f));
}

function computeTotalSize(fileList) {
    return fileList.reduce((sum, f) => sum + fs.statSync(f).size, 0);
}

function main() {
    const files = findInputFiles(INPUT_DIR);
    const totalSize = computeTotalSize(files);

    fs.mkdirSync(OUTPUT_DIR, { recursive: true });

    const summary = {
        processed_files: files.length,
        total_size_bytes: totalSize
    };

    const outputPath = path.join(OUTPUT_DIR, 'summary.json');
    fs.writeFileSync(outputPath, JSON.stringify(summary, null, 2));

    console.log(`Processed ${files.length} files, ${totalSize} bytes total.`);
    console.log(`Report written to: ${outputPath}`);
}

main();
