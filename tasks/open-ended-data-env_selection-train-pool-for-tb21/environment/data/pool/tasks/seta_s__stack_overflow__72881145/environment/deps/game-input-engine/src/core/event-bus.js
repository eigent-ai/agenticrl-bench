'use strict';

class EventBus {
  constructor() {
    this._listeners = new Map();
  }

  on(event, callback) {
    if (!this._listeners.has(event)) {
      this._listeners.set(event, []);
    }
    this._listeners.get(event).push(callback);
    return () => this.off(event, callback);
  }

  off(event, callback) {
    const listeners = this._listeners.get(event);
    if (!listeners) return;
    const idx = listeners.indexOf(callback);
    if (idx !== -1) listeners.splice(idx, 1);
  }

  emit(event, data) {
    const listeners = this._listeners.get(event);
    if (!listeners || listeners.length === 0) return;

    for (const listener of listeners) {
      listener(data);
    }
  }

  removeAllListeners(event) {
    if (event) {
      this._listeners.delete(event);
    } else {
      this._listeners.clear();
    }
  }

  listenerCount(event) {
    const listeners = this._listeners.get(event);
    return listeners ? listeners.length : 0;
  }
}

module.exports = { EventBus };
