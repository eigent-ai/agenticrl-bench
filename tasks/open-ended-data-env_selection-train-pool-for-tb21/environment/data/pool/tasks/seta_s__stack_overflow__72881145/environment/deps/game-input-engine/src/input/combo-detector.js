'use strict';

class ComboDetector {
  constructor(eventBus, inputManager) {
    this._eventBus = eventBus;
    this._inputManager = inputManager;
    this._combos = [];
  }

  registerCombo(name, keys, action) {
    this._combos.push({
      name,
      keys: [...keys],
      action
    });
  }

  check() {
    const pressed = this._inputManager.getPressedKeys();

    for (const combo of this._combos) {
      const allPressed = combo.keys.every(k => pressed.has(k));
      const anyNew = combo.keys.some(k => this._inputManager.isJustPressed(k));

      if (allPressed && anyNew) {
        combo.action();
        this._eventBus.emit('combo:triggered', {
          name: combo.name,
          keys: combo.keys
        });
      }
    }
  }

  reset() {
  }
}

module.exports = { ComboDetector };
