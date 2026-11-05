const { DateTime } = require('luxon');
const { EAST_TZ } = require('../config/timezone_config');

/**
 * Convert a UTC DateTime to Australian Eastern local time.
 * @param {DateTime} utcDt - A Luxon DateTime object in UTC.
 * @returns {DateTime} A DateTime in the Eastern Australian timezone.
 */
function convertToEastern(utcDt) {
    return utcDt.setZone(EAST_TZ);
}

module.exports = { convertToEastern };
