'use strict';

var EventTypes = require('../event_types');

// Handles navigation clicks on interactive elements
module.exports = {
  name: 'click_handler',
  eventType: EventTypes.CLICK,
  handleEvent: function(event) {
    return {
      action: 'navigated',
      target: event.target
    };
  }
};
