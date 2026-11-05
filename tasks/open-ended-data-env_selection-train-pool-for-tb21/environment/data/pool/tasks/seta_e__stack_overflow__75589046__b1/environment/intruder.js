const { Vec2 } = require('./physics');

class Intruder {
  constructor(position, active = true) {
    this.position = new Vec2(...position);
    this.active = active;
  }
}

module.exports = { Intruder };
