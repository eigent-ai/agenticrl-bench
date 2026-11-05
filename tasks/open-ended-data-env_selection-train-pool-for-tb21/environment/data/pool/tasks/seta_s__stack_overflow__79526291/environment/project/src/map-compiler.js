import { readFileSync } from 'fs';
import { join } from 'path';

export class MapCompiler {
  constructor(config) {
    this.config = config;
    this.tileWidth = config.tileWidth;
    this.tileHeight = config.tileHeight;
  }

  loadMap(filePath) {
    const data = JSON.parse(readFileSync(filePath, 'utf-8'));
    return this.compile(data);
  }

  compile(mapData) {
    const compiled = {
      name: mapData.name,
      width: mapData.width,
      height: mapData.height,
      pixelWidth: mapData.width * this.tileWidth,
      pixelHeight: mapData.height * this.tileHeight,
      tileSize: this.tileWidth,
      layers: [],
      animatedPositions: {}
    };

    for (const layer of mapData.layers) {
      const compiledLayer = {
        name: layer.name,
        sheet: layer.sheet,
        animated: layer.animated || false,
        tiles: []
      };

      if (layer.data && layer.data.length > 0) {
        compiledLayer.tiles = layer.data;
      } else {
        compiledLayer.tiles = this.generateDefaultTiles(
          mapData.width,
          mapData.height,
          layer.sheet
        );
      }

      compiled.layers.push(compiledLayer);
    }

    if (mapData.animatedTiles) {
      for (const [animName, positions] of Object.entries(mapData.animatedTiles)) {
        compiled.animatedPositions[animName] = positions.map(([row, col]) => ({
          x: row * this.tileWidth,
          y: col * this.tileHeight,
          row,
          col
        }));
      }
    }

    return compiled;
  }

  generateDefaultTiles(width, height, sheetName) {
    const tiles = [];
    for (let row = 0; row < height; row++) {
      for (let col = 0; col < width; col++) {
        let tileIndex;
        if (sheetName === 'terrain') {
          tileIndex = ((row + col) % 8) + (Math.floor(row / 5) % 4) * 8;
        } else {
          tileIndex = -1;
        }
        tiles.push({
          row,
          col,
          tileIndex,
          x: row * this.tileWidth,
          y: col * this.tileHeight
        });
      }
    }
    return tiles;
  }

  getMapInfo(compiled) {
    const animationInfo = {};
    for (const [name, positions] of Object.entries(compiled.animatedPositions)) {
      animationInfo[name] = {
        positions: positions.length,
        config: this.config.animations[name] || null
      };
    }

    return {
      name: compiled.name,
      width: compiled.width,
      height: compiled.height,
      pixelWidth: compiled.pixelWidth,
      pixelHeight: compiled.pixelHeight,
      tileCount: compiled.width * compiled.height,
      layerCount: compiled.layers.length,
      animations: animationInfo
    };
  }
}
