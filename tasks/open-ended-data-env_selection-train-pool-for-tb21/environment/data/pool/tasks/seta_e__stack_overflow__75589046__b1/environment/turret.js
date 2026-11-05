const { Vec2, clamp } = require('./physics');

class Turret {
  static MIN_SPEED = 30;
  static MAX_SPEED = 200;
  static MAX_RANGE = 400;
  static LAUNCH_ANGLE_Y = -120;

  constructor(position, facing = 1) {
    this.position = new Vec2(...position);
    this.velocity = new Vec2(0, 0);
    // facing: +1 = facing right, -1 = facing left
    this.facing = facing;
    this._target = null;
  }

  setTarget(target) {
    this._target = target;
  }

  computeFireVelocity() {
    const targetPos = this._target.position;

    const fireDirection = this.position.directionTo(targetPos);
    const distance = this.position.distanceTo(targetPos);

    const projectileSpeed =
      Turret.MIN_SPEED +
      (distance / Turret.MAX_RANGE) * (Turret.MAX_SPEED - Turret.MIN_SPEED);

    const velocityX = fireDirection.x * projectileSpeed * this.facing;
    const velocityY = Turret.LAUNCH_ANGLE_Y;

    return new Vec2(velocityX, velocityY);
  }
}

module.exports = { Turret };
