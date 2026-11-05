'use strict';

const DEFAULTS = { env: 'development', priority: 0 };

function mergeDefaults(config) {
    const merged = Object.create(null);
    Object.assign(merged, DEFAULTS, config);

    if (merged.hasOwnProperty('priority')) {
        merged.priority = Number(merged.priority);
    }
    if (merged.hasOwnProperty('maxRetries')) {
        merged.maxRetries = Number(merged.maxRetries);
    }

    return merged;
}

module.exports = { mergeDefaults };
