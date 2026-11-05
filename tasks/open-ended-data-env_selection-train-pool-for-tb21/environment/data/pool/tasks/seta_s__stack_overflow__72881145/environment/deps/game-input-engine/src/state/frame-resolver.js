'use strict';

class FrameStateResolver {
  constructor(inputManager) {
    this._inputManager = inputManager;
    this._state = {
      position: { x: 0, y: 0, z: 0 },
      velocity: { dx: 0, dy: 0, dz: 0 },
      frame: 0
    };

    this._keyBindings = {
      'KeyW': { axis: 'dz', value: -1 },
      'KeyS': { axis: 'dz', value: 1 },
      'KeyA': { axis: 'dx', value: -1 },
      'KeyD': { axis: 'dx', value: 1 },
      'Space': { axis: 'dy', value: 1 },
      'ShiftLeft': { axis: 'dy', value: -1 }
    };
  }

  resolveFrame() {
    for (const [key, binding] of Object.entries(this._keyBindings)) {
      if (this._inputManager.isPressed(key)) {
        this._state.velocity[binding.axis] += binding.value;
      }
    }

    this._state.position.x += this._state.velocity.dx;
    this._state.position.y += this._state.velocity.dy;
    this._state.position.z += this._state.velocity.dz;

    this._state.frame++;

    return this.getSnapshot();
  }

  getSnapshot() {
    return {
      position: { ...this._state.position },
      velocity: { ...this._state.velocity },
      frame: this._state.frame
    };
  }

  reset() {
    this._state.position = { x: 0, y: 0, z: 0 };
    this._state.velocity = { dx: 0, dy: 0, dz: 0 };
    this._state.frame = 0;
  }
}

module.exports = { FrameStateResolver };
