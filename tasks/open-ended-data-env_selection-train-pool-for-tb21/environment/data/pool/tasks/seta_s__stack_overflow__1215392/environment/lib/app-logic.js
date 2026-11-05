'use strict';

function processData() {
    console.log('[app] Processing...');
    console.log('[app] Done.');
    console.warn('[app] Low memory warning');
}

module.exports = { processData: processData };
