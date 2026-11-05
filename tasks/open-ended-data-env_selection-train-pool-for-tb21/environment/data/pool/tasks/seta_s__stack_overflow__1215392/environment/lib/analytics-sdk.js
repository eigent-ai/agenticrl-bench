'use strict';

function track(eventName) {
    console.log('[analytics] Sending event: ' + eventName);
    console.log('[analytics] Payload serialized');
    console.warn('[analytics] deprecation: use trackV2() instead');
}

module.exports = { track: track };
