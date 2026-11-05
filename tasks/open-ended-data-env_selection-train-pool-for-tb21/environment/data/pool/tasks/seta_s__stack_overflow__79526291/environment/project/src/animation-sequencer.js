export class AnimationSequencer {
  constructor(config) {
    this.animations = {};
    this.config = config;

    for (const [name, anim] of Object.entries(config.animations)) {
      this.animations[name] = {
        sheet: anim.sheet,
        startTile: anim.startTile,
        frameCount: anim.frameCount,
        frameRate: anim.frameRate,
        currentFrame: 0,
        timer: null
      };
    }
  }

  startAnimation(name) {
    const anim = this.animations[name];
    if (!anim) throw new Error(`Animation '${name}' not defined`);

    anim.currentFrame = 0;
    if (anim.timer) clearInterval(anim.timer);

    anim.timer = setInterval(() => {
      anim.currentFrame++;
    }, anim.frameRate);

    return anim;
  }

  stopAnimation(name) {
    const anim = this.animations[name];
    if (anim && anim.timer) {
      clearInterval(anim.timer);
      anim.timer = null;
    }
  }

  stopAll() {
    for (const name of Object.keys(this.animations)) {
      this.stopAnimation(name);
    }
  }

  getFrame(name) {
    const anim = this.animations[name];
    if (!anim) return null;

    const frameIndex = anim.currentFrame;
    if (frameIndex < 0 || frameIndex >= anim.frameCount) {
      return anim.startTile;
    }
    return anim.startTile + frameIndex;
  }

  getFrameForIndex(name, frameIndex) {
    const anim = this.animations[name];
    if (!anim) return null;

    if (frameIndex < 0 || frameIndex >= anim.frameCount) {
      return anim.startTile;
    }
    return anim.startTile + frameIndex;
  }

  getAllFrames(name) {
    const anim = this.animations[name];
    if (!anim) return [];

    const frames = [];
    for (let i = 0; i < anim.frameCount; i++) {
      frames.push(anim.startTile + i);
    }
    return frames;
  }

  getAnimationInfo(name) {
    const anim = this.animations[name];
    if (!anim) return null;
    return {
      name,
      sheet: anim.sheet,
      frameCount: anim.frameCount,
      frameRate: anim.frameRate,
      currentFrame: anim.currentFrame
    };
  }

  advanceFrame(name) {
    const anim = this.animations[name];
    if (!anim) return;
    anim.currentFrame++;
  }

  getAllAnimationInfo() {
    const info = {};
    for (const name of Object.keys(this.animations)) {
      info[name] = this.getAnimationInfo(name);
    }
    return info;
  }
}
