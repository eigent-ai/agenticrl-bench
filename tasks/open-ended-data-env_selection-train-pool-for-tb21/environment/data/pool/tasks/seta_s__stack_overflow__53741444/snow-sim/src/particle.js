'use strict';

class Particle {
  constructor(x, y, speedY, lifespan) {
    this.x = x;
    this.y = y;
    this.speedY = speedY;  // pixels per second
    this.lifespan = lifespan; // ms
    this.age = 0;
    this.alive = true;
  }

  update(dt) {
    this.age += dt;
    this.y += (this.speedY * dt) / 1000;
    if (this.age >= this.lifespan) {
      this.alive = false;
    }
  }
}

module.exports = Particle;
