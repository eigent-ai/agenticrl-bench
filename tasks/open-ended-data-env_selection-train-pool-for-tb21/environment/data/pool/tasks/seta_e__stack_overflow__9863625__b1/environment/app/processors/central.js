const { DateTime } = require('luxon');

const CENTRAL_TZ = "Australia/Darwin";  // Central Australia timezone

/**
 * Convert a UTC DateTime to Australian Central local time.
 * @param {DateTime} utcDt - A Luxon DateTime object in UTC.
 * @returns {DateTime} A DateTime in the Central Australian timezone.
 */
function convertToCentral(utcDt) {
    return utcDt.setZone(CENTRAL_TZ);
}

module.exports = { convertToCentral };
