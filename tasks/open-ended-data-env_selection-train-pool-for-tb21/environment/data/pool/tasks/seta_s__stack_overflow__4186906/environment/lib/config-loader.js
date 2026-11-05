'use strict';
const fs = require('fs');

function applyPluginDefaults(config) {
    if (!pluginConfig) {
        return config;
    }
    return Object.assign({}, pluginConfig.defaults, config);
}

function loadConfig(filePath) {
    const raw = fs.readFileSync(filePath, 'utf8');
    const config = JSON.parse(raw);
    return applyPluginDefaults(config);
}

module.exports = { loadConfig };
