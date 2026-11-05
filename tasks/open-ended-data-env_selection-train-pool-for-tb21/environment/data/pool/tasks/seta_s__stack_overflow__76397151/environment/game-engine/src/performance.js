export class Performance {
  constructor(targetFps) {
    this.targetFps = targetFps;
    this.updateTimeStep = 1000 / targetFps;
    this.delta = 0;
    this.lastUpdateTimeMs = 0;
    this.frameCount = 0;
    this.ups = 0;
    this.lastUpsTime = 0;
    this.updateCount = 0;
  }

  updateUps(timestamp) {
    this.updateCount++;
    if (timestamp - this.lastUpsTime >= 1000) {
      this.ups = this.updateCount;
      this.updateCount = 0;
      this.lastUpsTime = timestamp;
    }
  }
}
