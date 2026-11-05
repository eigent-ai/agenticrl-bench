'use strict';

var EventTypes = require('../event_types');

// Handles mouseover events for hover highlighting
module.exports = {
  name: 'mouse_handler',
  eventType: EventTypes.MOUSEOVER,
  handleEvent: function(event) {
    return {
      action: 'highlighted',
      target: event.target
    };
  }
};
