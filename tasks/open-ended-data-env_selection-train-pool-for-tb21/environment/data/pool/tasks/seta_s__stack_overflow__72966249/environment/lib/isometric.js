// lib/isometric.js
const GRID = {
  gridRows: 10,
  gridCols: 10,
  tileSize: 40,
};

const canvasOffset = GRID.tileSize * GRID.gridRows * Math.sqrt(3) / 2;

// Forward transform: Cartesian grid coords → canvas screen coords
function carToIso(x, y) {
  return [
    (x - y) * Math.sqrt(3) / 2 + canvasOffset,
    (x + y) / 2,
  ];
}

// Inverse transform: canvas screen coords → grid tile [col, row]
function isoToCar(a, b) {
  const xMinusY = (a - canvasOffset) * Math.sqrt(3) / 2;
  const xPlusY  = b * 2;
  const x = (xMinusY + xPlusY) / 2;
  const y = xPlusY - x;
  return [
    Math.floor(x / GRID.tileSize),
    Math.floor(y / GRID.tileSize),
  ];
}

module.exports = { carToIso, isoToCar, GRID, canvasOffset };
