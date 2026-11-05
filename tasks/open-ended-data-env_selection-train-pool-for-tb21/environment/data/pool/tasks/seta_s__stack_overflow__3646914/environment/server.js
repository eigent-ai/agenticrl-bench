const express = require('express');
const path = require('path');
const config = require('./config.json');

const app = express();

// Static file serving
app.use('/static', express.static('./public'));

// Routes
app.use('/api', require('./routes/check-file'));
app.use('/api', require('./routes/theme-manifest'));
app.use('/health', require('./routes/health'));

// Fallback middleware for missing theme assets
app.use(require('./routes/fallback'));

app.listen(config.port, () => {
    console.log(`Asset server running on port ${config.port}`);
});

module.exports = app;
