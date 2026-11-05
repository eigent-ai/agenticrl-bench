#!/bin/bash
set -e

cd /home/user/game-input-engine

# Fix 1: EventBus - clone event data for each listener to prevent cross-listener mutation
cat > src/core/event-bus.js << 'ENDOFFILE'
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
      listener({ ...data });
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
ENDOFFILE

# Fix 2: InputManager - guard against re-pressing already-held keys
cat > src/input/input-manager.js << 'ENDOFFILE'
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
    if (this._pressed.has(code)) return;
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
ENDOFFILE

# Fix 3: ComboDetector - sort combos by length (longest first) and suppress sub-combos
cat > src/input/combo-detector.js << 'ENDOFFILE'
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
    this._combos.sort((a, b) => b.keys.length - a.keys.length);
  }

  check() {
    const pressed = this._inputManager.getPressedKeys();
    const consumedKeys = new Set();

    for (const combo of this._combos) {
      const allPressed = combo.keys.every(k => pressed.has(k));
      const anyNew = combo.keys.some(k => this._inputManager.isJustPressed(k));
      const subsumed = combo.keys.every(k => consumedKeys.has(k));

      if (allPressed && anyNew && !subsumed) {
        combo.action();
        combo.keys.forEach(k => consumedKeys.add(k));
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
ENDOFFILE

# Fix 4: FrameStateResolver - reset velocity to zero at start of each frame
cat > src/state/frame-resolver.js << 'ENDOFFILE'
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
    this._state.velocity.dx = 0;
    this._state.velocity.dy = 0;
    this._state.velocity.dz = 0;

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
ENDOFFILE

# Fix 5: CooldownTracker - use frame-based timing instead of wall-clock
cat > src/systems/cooldown-tracker.js << 'ENDOFFILE'
'use strict';

class CooldownTracker {
  constructor() {
    this._cooldowns = new Map();
    this._activeCooldowns = new Map();
    this._frameCount = 0;
  }

  register(actionName, cooldownFrames) {
    this._cooldowns.set(actionName, cooldownFrames);
  }

  tryFire(actionName) {
    if (!this._cooldowns.has(actionName)) {
      return false;
    }

    if (this._activeCooldowns.has(actionName)) {
      const startFrame = this._activeCooldowns.get(actionName);
      const cooldownFrames = this._cooldowns.get(actionName);
      if (this._frameCount - startFrame < cooldownFrames) {
        return false;
      }
    }

    this._activeCooldowns.set(actionName, this._frameCount);
    return true;
  }

  tick() {
    this._frameCount++;
  }

  isOnCooldown(actionName) {
    if (!this._activeCooldowns.has(actionName)) {
      return false;
    }
    const startFrame = this._activeCooldowns.get(actionName);
    const cooldownFrames = this._cooldowns.get(actionName);
    return (this._frameCount - startFrame) < cooldownFrames;
  }

  reset() {
    this._activeCooldowns.clear();
    this._frameCount = 0;
  }
}

module.exports = { CooldownTracker };
ENDOFFILE

# Fix 6: ReplaySystem - make replay dispatch synchronous (not process.nextTick)
cat > src/replay/replay-system.js << 'ENDOFFILE'
'use strict';

class ReplaySystem {
  constructor(eventBus, frameResolver) {
    this._eventBus = eventBus;
    this._frameResolver = frameResolver;
    this._recording = false;
    this._replaying = false;
    this._events = [];
    this._snapshots = [];
    this._currentFrame = 0;
  }

  startRecording() {
    this._recording = true;
    this._events = [];
    this._snapshots = [];
    this._currentFrame = 0;
  }

  recordEvent(event) {
    if (!this._recording) return;
    this._events.push({
      frame: this._currentFrame,
      event: { ...event }
    });
  }

  recordFrame(snapshot) {
    if (!this._recording) return;
    this._snapshots.push({
      frame: this._currentFrame,
      state: snapshot
    });
    this._currentFrame++;
  }

  stopRecording() {
    this._recording = false;
    return {
      events: [...this._events],
      snapshots: [...this._snapshots],
      totalFrames: this._currentFrame
    };
  }

  replay(recording, inputCallback) {
    this._replaying = true;
    const replaySnapshots = [];

    this._frameResolver.reset();

    for (let frame = 0; frame < recording.totalFrames; frame++) {
      const frameEvents = recording.events.filter(e => e.frame === frame);

      for (const entry of frameEvents) {
        inputCallback(entry.event);
      }

      const snapshot = this._frameResolver.resolveFrame();
      replaySnapshots.push({
        frame,
        state: snapshot
      });
    }

    this._replaying = false;
    return replaySnapshots;
  }
}

module.exports = { ReplaySystem };
ENDOFFILE

# Fix 7: WatchpointManager - actually clear intervals in unwatch, add null-check in callback
cat > src/input/watchpoint-manager.js << 'ENDOFFILE'
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
      if (!this._watchpoints.has(name)) return;
      const allHeld = keysCopy.every(k => this._inputManager.isPressed(k));
      if (allHeld) {
        cb();
      }
    }, intervalMs);

    this._intervals.set(name, id);
  }

  unwatch(name) {
    const id = this._intervals.get(name);
    if (id !== undefined) {
      clearInterval(id);
      this._intervals.delete(name);
    }
    this._watchpoints.delete(name);
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
ENDOFFILE
