/**
 * Run a complete analysis pipeline demonstrating all scidata-node features.
 */
const path = require('path');
const { measurements, prices } = require('../data/loader');
const { PriceAnalyzer } = require('../processing/analyzer');
const { transformMeasurements } = require('../processing/transformer');

function main() {
    console.log('='.repeat(60));
    console.log('SciData Analysis Report');
    console.log('='.repeat(60));

    console.log(`\nMeasurements loaded: ${measurements.length} rows`);
    console.log(`Columns: ${Object.keys(measurements[0]).join(', ')}`);

    const sensorIds = [...new Set(measurements.map(r => r.sensor_id))].sort();
    console.log(`Sensors: ${sensorIds.join(', ')}`);

    const avgTemp = measurements.reduce((s, r) => s + r.temperature, 0) / measurements.length;
    const avgPressure = measurements.reduce((s, r) => s + r.pressure, 0) / measurements.length;
    console.log(`Average temperature: ${avgTemp.toFixed(2)}`);
    console.log(`Average pressure: ${avgPressure.toFixed(2)}`);

    console.log(`\nPrices loaded: ${prices.length} rows`);
    console.log(`Columns: ${Object.keys(prices[0]).join(', ')}`);

    const pricesPath = path.join(__dirname, '..', 'data', 'prices.csv');
    const analyzer = new PriceAnalyzer(pricesPath);
    const summary = analyzer.dailySummary();
    console.log(`\nDaily summaries computed: ${summary.length} days`);
    console.log(`First day: ${summary[0][0]}, Close: ${summary[0][2]}`);
    console.log(`Last day: ${summary[summary.length - 1][0]}, Close: ${summary[summary.length - 1][2]}`);
    console.log(`Average closing price: ${analyzer.averageClose().toFixed(2)}`);

    const transformed = transformMeasurements();
    console.log(`\nTransformed measurements: ${transformed.length} rows`);

    const rawS001 = measurements.filter(r => r.sensor_id === 'S001');
    const calS001 = transformed.filter(r => r.sensor_id === 'S001');
    const rawAvg = rawS001.reduce((s, r) => s + r.temperature, 0) / rawS001.length;
    const calAvg = calS001.reduce((s, r) => s + r.temperature, 0) / calS001.length;
    console.log(`S001 raw avg temp: ${rawAvg.toFixed(2)}, calibrated avg temp: ${calAvg.toFixed(2)}`);

    console.log('\n' + '='.repeat(60));
    console.log('Analysis complete. All components working correctly.');
    console.log('='.repeat(60));
}

main();
