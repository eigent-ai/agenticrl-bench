const fs = require('fs');
const STORAGE_PATH = '/app/.storage.json';

function saveEvents(events) {
  fs.writeFileSync(STORAGE_PATH, events);
}

function loadEvents() {
  try {
    const data = fs.readFileSync(STORAGE_PATH, 'utf-8');
    return data;
  } catch (e) {
    return [];
  }
}

module.exports = { saveEvents, loadEvents };
