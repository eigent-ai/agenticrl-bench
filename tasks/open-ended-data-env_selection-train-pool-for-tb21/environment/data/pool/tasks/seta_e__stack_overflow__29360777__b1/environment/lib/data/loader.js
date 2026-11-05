/**
 * Load measurement and price datasets.
 */
const fs = require('fs');
const { parse } = require('csv-parse/sync');

const measurementsRaw = fs.readFileSync('measurements.csv', 'utf-8');
const measurements = parse(measurementsRaw, { columns: true, cast: true });

const pricesRaw = fs.readFileSync('prices.csv', 'utf-8');
const prices = parse(pricesRaw, { columns: true, cast: true });

module.exports = { measurements, prices };
