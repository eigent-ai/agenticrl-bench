'use strict';

class WatchpointManager {
  constructor(inputManager) {
    this._inputManager = inputManager;
    this._watchpoints = new Map();
    this._intervals = new Map();
  }

  watch(name, keys, callback, intervalMs = 100) {
    const keysCopy = [...keys];
    const cb = callback;

    this._watchpoints.set(name, { keys: keysCopy, callback: cb });

    const id = setInterval(() => {
      const allHeld = keysCopy.every(k => this._inputManager.isPressed(k));
      if (allHeld) {
        cb();
      }
    }, intervalMs);

    this._intervals.set(name, id);
  }

  unwatch(name) {
    this._watchpoints.delete(name);
    this._intervals.delete(name);
  }

  unwatchAll() {
    for (const name of [...this._intervals.keys()]) {
      this.unwatch(name);
    }
  }

  isWatching(name) {
    return this._watchpoints.has(name);
  }
}

module.exports = { WatchpointManager };
