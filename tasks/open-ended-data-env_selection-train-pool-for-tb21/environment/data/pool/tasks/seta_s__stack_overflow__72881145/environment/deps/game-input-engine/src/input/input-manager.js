'use strict';

class InputManager {
  constructor(eventBus) {
    this._eventBus = eventBus;
    this._pressed = new Set();
    this._justPressed = new Set();
    this._justReleased = new Set();

    this._eventBus.on('keydown', (evt) => this._onKeyDown(evt));
    this._eventBus.on('keyup', (evt) => this._onKeyUp(evt));
  }

  _onKeyDown(evt) {
    const code = evt.code;
    this._justPressed.add(code);
    this._pressed.add(code);
  }

  _onKeyUp(evt) {
    const code = evt.code;
    this._pressed.delete(code);
    this._justReleased.add(code);
  }

  isPressed(code) {
    return this._pressed.has(code);
  }

  isJustPressed(code) {
    return this._justPressed.has(code);
  }

  isJustReleased(code) {
    return this._justReleased.has(code);
  }

  getPressedKeys() {
    return new Set(this._pressed);
  }

  endFrame() {
    this._justPressed.clear();
    this._justReleased.clear();
  }

  clear() {
    this._pressed.clear();
    this._justPressed.clear();
    this._justReleased.clear();
  }
}

module.exports = { InputManager };
