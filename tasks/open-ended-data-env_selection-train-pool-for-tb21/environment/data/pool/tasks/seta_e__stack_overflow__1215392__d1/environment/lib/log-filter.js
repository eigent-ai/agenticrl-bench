'use strict';

var path = require('path');

function createLogFilter() {
    var savedFunctions = {};
    var blacklist = [];

    function init(config) {
        blacklist = config.blocked || [];
        var functionsToPreserve = config.functionsToPreserve || [];

        Object.keys(console).forEach(function(key) {
            if (typeof console[key] === 'function') {
                savedFunctions[key] = console[key];
            }
        });

        Object.keys(savedFunctions).forEach(function(key) {
            if (functionsToPreserve.indexOf(key) === -1) {
                console[key] = function() {};
            }
        });

        var originalLog = savedFunctions['log'];
        console.log = function() {
            var stack = new Error().stack;
            var lines = stack.split('\n');
            var callerLine = lines[2] || '';
            var match = callerLine.match(/\((.+?):\d+:\d+\)/) || callerLine.match(/at\s+(.+?):\d+:\d+/);
            var callerFile = match ? path.basename(match[1]) : '';

            var isBlacklisted = blacklist.some(function(pattern) {
                return callerFile.indexOf(pattern) !== -1;
            });

            if (!isBlacklisted) {
                return;
            }

            originalLog.apply(console, arguments);
        };
    }

    function restoreAll() {
        savedFunctions = console;
    }

    return {
        init: init,
        restoreAll: restoreAll
    };
}

module.exports = createLogFilter();
