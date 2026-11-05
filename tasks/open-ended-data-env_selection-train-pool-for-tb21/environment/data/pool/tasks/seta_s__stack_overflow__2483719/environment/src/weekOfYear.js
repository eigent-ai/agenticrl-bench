/**
 * Get the ISO 8601 week-of-year number for a given date.
 * @param {string} dateStr - ISO date string (e.g. "2024-12-30")
 * @returns {number} ISO week number (1-53)
 */
function getWeekOfYear(dateStr) {
  const parts = dateStr.split('-');
  const date = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));

  const jan1 = new Date(date.getFullYear(), 0, 1);
  const dayOfYear = Math.floor((date - jan1) / 86400000) + 1;

  return Math.ceil((dayOfYear + jan1.getDay() + 1) / 7);
}

module.exports = { getWeekOfYear };
