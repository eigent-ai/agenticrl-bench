'use strict';
const { getWeekNumber, getWeeksInMonth, getNext7Days } = require('./date-utils');

const [,, command, ...args] = process.argv;

switch (command) {
    case 'week': {
        if (!args[0]) { console.error('Usage: week <YYYY-MM-DD>'); process.exit(1); }
        console.log(JSON.stringify({ week: getWeekNumber(args[0]) }));
        break;
    }
    case 'weeks-in-month': {
        const year  = parseInt(args[0], 10);
        const month = parseInt(args[1], 10);
        if (!year || !month) { console.error('Usage: weeks-in-month <YYYY> <MM>'); process.exit(1); }
        console.log(JSON.stringify({ weeksInMonth: getWeeksInMonth(year, month) }));
        break;
    }
    case 'schedule': {
        if (!args[0]) { console.error('Usage: schedule <YYYY-MM-DD>'); process.exit(1); }
        console.log(JSON.stringify(getNext7Days(args[0])));
        break;
    }
    default:
        console.error('Commands: week | weeks-in-month | schedule');
        process.exit(1);
}
