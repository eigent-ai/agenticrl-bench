const fs = require('fs');
const path = require('path');

function writeReport(outputDir, results) {
    var report = {
        dataset_count: Object.keys(results).length,
        generated_at: new Date().toISOString(),
        datasets: results
    };

    var reportPath = path.join(outputDir, 'report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log('Report written to ' + reportPath);
}

module.exports = { writeReport };
