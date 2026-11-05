import { createCanvas } from 'canvas';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import GIFEncoder from 'gif-encoder-2';

export class Renderer {
  constructor(spriteProcessor, animationSequencer, config) {
    this.spriteProcessor = spriteProcessor;
    this.animationSequencer = animationSequencer;
    this.config = config;
    this.tileCache = null;
    this.initialized = false;
  }

  async init(assetsDir) {
    await this.spriteProcessor.loadAndSliceAll(assetsDir);
    this.tileCache = {};

    for (const [sheetName, tiles] of Object.entries(this.spriteProcessor.tiles)) {
      this.tileCache[sheetName] = tiles;
    }

    this.initialized = true;
  }

  renderStaticMap(compiledMap, outputPath) {
    if (!this.initialized) throw new Error('Renderer not initialized');

    const canvas = createCanvas(compiledMap.pixelWidth, compiledMap.pixelHeight);
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, compiledMap.pixelWidth, compiledMap.pixelHeight);

    for (const layer of compiledMap.layers) {
      for (const tile of layer.tiles) {
        if (tile.tileIndex < 0) continue;

        const srcTile = this.spriteProcessor.getTile(layer.sheet, tile.tileIndex);
        if (!srcTile) continue;

        ctx.drawImage(srcTile.canvas, tile.x, tile.y);
      }
    }

    const buffer = canvas.toBuffer('image/png');
    writeFileSync(outputPath, buffer);
    return { width: compiledMap.pixelWidth, height: compiledMap.pixelHeight, path: outputPath };
  }

  renderAnimatedPreview(compiledMap, outputPath, duration) {
    if (!this.initialized) throw new Error('Renderer not initialized');

    const previewWidth = Math.min(compiledMap.pixelWidth, 320);
    const previewHeight = Math.min(compiledMap.pixelHeight, 240);
    const scale = Math.min(previewWidth / compiledMap.pixelWidth, previewHeight / compiledMap.pixelHeight);

    const maxFrameCount = Math.max(
      ...Object.values(this.config.animations).map(a => a.frameCount)
    );

    const totalFrames = maxFrameCount * 2;

    const encoder = new GIFEncoder(previewWidth, previewHeight);
    encoder.setDelay(200);
    encoder.setRepeat(0);
    encoder.start();

    for (const animName of Object.keys(compiledMap.animatedPositions)) {
      this.animationSequencer.startAnimation(animName);
    }

    for (let frame = 0; frame < totalFrames; frame++) {
      const canvas = createCanvas(previewWidth, previewHeight);
      const ctx = canvas.getContext('2d');

      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, previewWidth, previewHeight);
      ctx.save();
      ctx.scale(scale, scale);

      for (const layer of compiledMap.layers) {
        for (const tile of layer.tiles) {
          if (tile.tileIndex < 0) continue;
          const srcTile = this.spriteProcessor.getTile(layer.sheet, tile.tileIndex);
          if (!srcTile) continue;
          ctx.drawImage(srcTile.canvas, tile.x, tile.y);
        }
      }

      for (const [animName, positions] of Object.entries(compiledMap.animatedPositions)) {
        const tileIndex = this.animationSequencer.getFrame(animName);
        if (tileIndex === null) continue;

        const anim = this.config.animations[animName];
        if (!anim) continue;

        const srcTile = this.spriteProcessor.getTile(anim.sheet, tileIndex);
        if (!srcTile) continue;

        for (const pos of positions) {
          ctx.drawImage(srcTile.canvas, pos.x, pos.y);
        }
      }

      ctx.restore();
      encoder.addFrame(ctx);

      for (const animName of Object.keys(compiledMap.animatedPositions)) {
        this.animationSequencer.advanceFrame(animName);
      }
    }

    this.animationSequencer.stopAll();

    encoder.finish();
    const buffer = encoder.out.getData();
    writeFileSync(outputPath, buffer);

    return { frames: totalFrames, width: previewWidth, height: previewHeight, path: outputPath };
  }

  getMapInfo(compiledMap) {
    if (!this.tileCache) throw new Error('Renderer not initialized — call init() first');
    return {
      tileCache: Object.keys(this.tileCache),
      totalTiles: Object.values(this.tileCache).reduce((sum, t) => sum + t.length, 0)
    };
  }
}
