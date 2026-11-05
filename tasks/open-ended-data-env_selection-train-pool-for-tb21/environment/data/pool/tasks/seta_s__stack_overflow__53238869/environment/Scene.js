'use strict';

const STATUS = {
  PENDING:   'PENDING',
  RUNNING:   'RUNNING',
  SLEEPING:  'SLEEPING',
  PAUSED:    'PAUSED',
  DESTROYED: 'DESTROYED',
};

class Scene {
  constructor(key) {
    this.key = key;
    this.status = STATUS.PENDING;
    this.data = {};
    this.initCallCount    = 0;
    this.preloadCallCount = 0;
    this.createCallCount  = 0;
  }

  init(data) {
    this.initCallCount++;
    this.data = data || {};
    this.status = 'INIT';
  }

  preload() {
    this.preloadCallCount++;
    this.status = 'PRELOAD';
  }

  create() {
    this.createCallCount++;
    this.status = STATUS.RUNNING;
  }
}

module.exports = { Scene, STATUS };
