const { DateTime } = require('luxon');
const { convertToEastern } = require('./processors/eastern');
const { convertToCentral } = require('./processors/central');
const { convertToWestern } = require('./processors/western');

/**
 * Process a log entry and add localized timestamps for each Australian region.
 * @param {Object} entry - An object with "timestamp" (ISO UTC string) and "event" keys.
 * @returns {Object} The entry augmented with "eastern", "central", and "western" ISO timestamps.
 */
function processLogEntry(entry) {
    const utcDt = DateTime.fromISO(entry.timestamp, { zone: 'utc' });
    return {
        event: entry.event,
        utc: entry.timestamp,
        eastern: convertToEastern(utcDt).toISO(),
        central: convertToCentral(utcDt).toISO(),
        western: convertToWestern(utcDt).toISO(),
    };
}

module.exports = { processLogEntry };
