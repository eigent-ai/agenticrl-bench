'use strict';
const fs = require('fs');
const path = require('path');

const { loadConfig } = require('./lib/config-loader');
const { validateConfig } = require('./lib/validator');
const { mergeDefaults } = require('./lib/merger');
const { buildReportEntry } = require('./lib/reporter');

// Attempt to load global overrides — may not exist
try {
    require('./lib/global-overrides');
} catch (e) {
    // intentional: file may be absent
}

const configDir = path.join(__dirname, 'configs');
const files = fs.readdirSync(configDir)
    .filter(f => f.endsWith('.json'))
    .sort();

const result = {
    total: files.length,
    processed: 0,
    errors: [],
    services: {}
};

for (const file of files) {
    const serviceName = path.basename(file, '.json');
    try {
        const filePath = path.join(configDir, file);
        const config = loadConfig(filePath);
        const validated = validateConfig(config);
        const merged = mergeDefaults(validated);
        const entry = buildReportEntry(merged);
        result.services[serviceName] = entry;
        result.processed++;
    } catch (err) {
        result.errors.push({ service: serviceName, error: err.message });
    }
}

fs.writeFileSync(
    path.join(__dirname, 'report.json'),
    JSON.stringify(result, null, 2)
);

if (result.errors.length > 0) {
    console.error('Processing errors: ' + JSON.stringify(result.errors));
    process.exit(1);
}

console.log('Done. Processed ' + result.processed + '/' + result.total + ' services.');
