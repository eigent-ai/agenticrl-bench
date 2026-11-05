'use strict';

var EventTypes = require('../event_types');

// Handles keyboard shortcuts from keydown events
module.exports = {
  name: 'keyboard_handler',
  eventType: EventTypes.KEYDOWN,
  handleEvent: function(event) {
    return {
      action: 'shortcut',
      key: event.key
    };
  }
};
