'use strict';

var logFilter = require('./lib/log-filter');
var config = require('./config/log-config.json');

logFilter.init(config);

var noisyVendor = require('./lib/noisy-vendor');
var analyticsSdk = require('./lib/analytics-sdk');
var appLogic = require('./lib/app-logic');

noisyVendor.init();
analyticsSdk.track('page_view');
appLogic.processData();

console.log('[main] Application started successfully');
console.warn('[main] Running in development mode');
console.error('[main] Error handler registered');

logFilter.restoreAll();
