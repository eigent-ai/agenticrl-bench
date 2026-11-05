'use strict';

class CooldownTracker {
  constructor() {
    this._cooldowns = new Map();
    this._activeCooldowns = new Map();
  }

  register(actionName, cooldownFrames) {
    this._cooldowns.set(actionName, cooldownFrames);
  }

  tryFire(actionName) {
    if (!this._cooldowns.has(actionName)) {
      return false;
    }

    if (this._activeCooldowns.has(actionName)) {
      const startTime = this._activeCooldowns.get(actionName);
      const cooldownMs = this._cooldowns.get(actionName);
      if (Date.now() - startTime < cooldownMs) {
        return false;
      }
    }

    this._activeCooldowns.set(actionName, Date.now());
    return true;
  }

  tick() {
    // advance frame
  }

  isOnCooldown(actionName) {
    if (!this._activeCooldowns.has(actionName)) {
      return false;
    }
    const startTime = this._activeCooldowns.get(actionName);
    const cooldownMs = this._cooldowns.get(actionName);
    return (Date.now() - startTime) < cooldownMs;
  }

  reset() {
    this._activeCooldowns.clear();
  }
}

module.exports = { CooldownTracker };
