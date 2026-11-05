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
        process.nextTick(() => {
          inputCallback(entry.event);
        });
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
