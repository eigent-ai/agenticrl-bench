'use strict';

function buildReportEntry(config) {
    let descriptionStatus;
    if (config.description == null) {
        descriptionStatus = 'missing';
    } else {
        descriptionStatus = 'set';
    }

    return {
        status: 'ok',
        env: config.env,
        maxRetries: config.maxRetries,
        descriptionStatus,
    };
}

module.exports = { buildReportEntry };
