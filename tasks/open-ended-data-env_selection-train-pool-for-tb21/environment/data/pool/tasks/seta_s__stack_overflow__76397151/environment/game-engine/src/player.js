export class Player {
  constructor(x, y, w, h, tileSize) {
    this.dimensions = {
      width: w,
      height: h,
    };

    this.position = {
      x: x,
      y: y,
      nextX: x,
      nextY: y,
    };

    this.tileSize = tileSize;
    this.direction = null;
    this.moving = false;
    this.color = '#ff0000';
    this.speed = 5;
    this.allowMovement = true;
    this._moveInterval = null;
    this._moveCallbacks = [];
  }

  queueInput(direction) {
    if (!this.allowMovement) return false;
    this._pendingInput = direction;
    return true;
  }

  update(state) {
    if (!this.allowMovement) return;

    const dir = this._pendingInput;
    this._pendingInput = null;

    if (!dir) return;

    let nextX = this.position.x;
    let nextY = this.position.y;

    if (dir === 'UP') {
      this.direction = 'UP';
      nextY -= this.tileSize;
    }
    if (dir === 'DOWN') {
      this.direction = 'DOWN';
      nextY += this.tileSize;
    }
    if (dir === 'LEFT') {
      this.direction = 'LEFT';
      nextX -= this.tileSize;
    }
    if (dir === 'RIGHT') {
      this.direction = 'RIGHT';
      nextX += this.tileSize;
    }

    this.position.nextX = nextX;
    this.position.nextY = nextY;

    if (state.map.isTileWalkable(this.position.nextX, this.position.nextY)) {
      this.transitionMovement(state);
    } else {
      this.position.nextX = this.position.x;
      this.position.nextY = this.position.y;
    }
  }

  transitionMovement(state) {
    this.allowMovement = false;

    const step = () => {
      this.moving = this.position.x !== this.position.nextX || this.position.y !== this.position.nextY;

      if (this.position.nextX < this.position.x) {
        this.position.x -= this.speed;
      }

      if (this.position.nextX > this.position.x) {
        this.position.x += this.speed;
      }

      if (this.position.nextY < this.position.y) {
        this.position.y -= this.speed;
      }

      if (this.position.nextY > this.position.y) {
        this.position.y += this.speed;
      }

      if (this.position.nextX === this.position.x && this.position.nextY === this.position.y) {
        this.position.x = this.position.nextX;
        this.position.y = this.position.nextY;
        this.moving = false;
        this.allowMovement = true;
        clearInterval(this._moveInterval);
        this._moveInterval = null;
        this._fireCallbacks();
      }
    };

    this._moveInterval = setInterval(step, state.performance.updateTimeStep);
  }

  onMoveComplete(cb) {
    this._moveCallbacks.push(cb);
  }

  _fireCallbacks() {
    for (const cb of this._moveCallbacks) {
      cb();
    }
  }

  destroy() {
    if (this._moveInterval) {
      clearInterval(this._moveInterval);
      this._moveInterval = null;
    }
    this._moveCallbacks = [];
  }
}
