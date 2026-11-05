const { DateTime } = require('luxon');
const { WEST_TZ } = require('../config/timezone_config');

/**
 * Convert a UTC DateTime to Australian Western local time.
 * @param {DateTime} utcDt - A Luxon DateTime object in UTC.
 * @returns {DateTime} A DateTime in the Western Australian timezone.
 */
function convertToWestern(utcDt) {
    return utcDt.setZone(WEST_TZ);
}

module.exports = { convertToWestern };
