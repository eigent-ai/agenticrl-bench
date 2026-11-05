const _Math = Math;

class Vec2 {
  constructor(x = 0, y = 0) {
    this.x = Number(x);
    this.y = Number(y);
  }

  normalized() {
    const mag = _Math.sqrt(this.x ** 2 + this.y ** 2);
    if (mag === 0) return new Vec2(0, 0);
    return new Vec2(this.x / mag, this.y / mag);
  }

  directionTo(other) {
    return new Vec2(other.x - this.x, other.y - this.y).normalized();
  }

  distanceTo(other) {
    return _Math.sqrt((other.x - this.x) ** 2 + (other.y - this.y) ** 2);
  }

  toString() {
    return `Vec2(${this.x.toFixed(3)}, ${this.y.toFixed(3)})`;
  }
}

function clamp(value, minVal, maxVal) {
  return Math.max(minVal, Math.min(maxVal, value));
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

module.exports = { Vec2, clamp, lerp };
