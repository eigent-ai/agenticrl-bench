import { createCanvas, loadImage } from 'canvas';
import { readFileSync } from 'fs';
import { join } from 'path';

export class SpriteProcessor {
  constructor(config) {
    this.config = config;
    this.tileWidth = config.tileWidth;
    this.tileHeight = config.tileHeight;
    this.sheets = {};
    this.tiles = {};
  }

  async loadSheet(name, filePath) {
    const image = await loadImage(filePath);
    this.sheets[name] = {
      image,
      width: image.width,
      height: image.height,
      columns: this.config.spriteSheets[name].columns,
      rows: this.config.spriteSheets[name].rows
    };
    return this.sheets[name];
  }

  sliceSheet(sheetName) {
    const sheet = this.sheets[sheetName];
    if (!sheet) throw new Error(`Sheet '${sheetName}' not loaded`);

    const tiles = [];
    for (let row = 0; row < sheet.rows; row++) {
      for (let col = 0; col < sheet.columns; col++) {
        const canvas = createCanvas(this.tileWidth, this.tileHeight);
        const ctx = canvas.getContext('2d');

        const srcX = col * (this.tileWidth + 1);
        const srcY = row * this.tileHeight;

        ctx.drawImage(
          sheet.image,
          srcX, srcY,
          this.tileWidth, this.tileHeight,
          0, 0,
          this.tileWidth, this.tileHeight
        );

        const tileIndex = row * sheet.columns + col;
        tiles.push({
          index: tileIndex,
          canvas,
          row,
          col,
          srcX,
          srcY
        });
      }
    }

    this.tiles[sheetName] = tiles;
    return tiles;
  }

  getTile(sheetName, index) {
    const tiles = this.tiles[sheetName];
    if (!tiles) return null;
    return tiles[index] || null;
  }

  getTileAt(sheetName, row, col) {
    const sheet = this.sheets[sheetName];
    if (!sheet) return null;
    const index = row * sheet.columns + col;
    return this.getTile(sheetName, index);
  }

  async loadAndSliceAll(assetsDir) {
    const results = {};
    for (const [name, info] of Object.entries(this.config.spriteSheets)) {
      const filePath = join(assetsDir, 'sprites', info.file);
      await this.loadSheet(name, filePath);
      results[name] = this.sliceSheet(name);
    }
    return results;
  }
}
