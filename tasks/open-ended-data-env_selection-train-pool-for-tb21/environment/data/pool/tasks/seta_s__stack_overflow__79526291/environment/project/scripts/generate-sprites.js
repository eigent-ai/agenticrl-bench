import { createCanvas } from 'canvas';
import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const appDir = join(__dirname, '..');
const spritesDir = join(appDir, 'assets', 'sprites');

if (!existsSync(spritesDir)) {
  mkdirSync(spritesDir, { recursive: true });
}

const TILE_SIZE = 32;
const COLS = 8;
const ROWS = 4;

function generateTerrainSheet() {
  const canvas = createCanvas(COLS * TILE_SIZE, ROWS * TILE_SIZE);
  const ctx = canvas.getContext('2d');

  const terrainColors = [
    ['#228B22', '#2E8B57', '#32CD32', '#006400', '#90EE90', '#3CB371', '#2E8B57', '#228B22'],
    ['#8B4513', '#A0522D', '#D2691E', '#CD853F', '#DEB887', '#F4A460', '#D2B48C', '#8B4513'],
    ['#808080', '#A9A9A9', '#696969', '#778899', '#B0C4DE', '#708090', '#C0C0C0', '#808080'],
    ['#4169E1', '#1E90FF', '#00BFFF', '#87CEEB', '#ADD8E6', '#B0E0E6', '#AFEEEE', '#4169E1']
  ];

  for (let row = 0; row < ROWS; row++) {
    for (let col = 0; col < COLS; col++) {
      const x = col * TILE_SIZE;
      const y = row * TILE_SIZE;
      const color = terrainColors[row][col];

      ctx.fillStyle = color;
      ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);

      ctx.fillStyle = shiftColor(color, 20);
      ctx.fillRect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8);

      ctx.fillStyle = shiftColor(color, -20);
      ctx.beginPath();
      ctx.arc(x + TILE_SIZE / 2, y + TILE_SIZE / 2, 6, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = '#00000033';
      ctx.strokeRect(x, y, TILE_SIZE, TILE_SIZE);
    }
  }

  const buffer = canvas.toBuffer('image/png');
  writeFileSync(join(spritesDir, 'terrain.png'), buffer);
  console.log('Generated terrain.png');
}

function generateObjectsSheet() {
  const canvas = createCanvas(COLS * TILE_SIZE, ROWS * TILE_SIZE);
  const ctx = canvas.getContext('2d');

  ctx.fillStyle = '#00000000';
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const waterFrameColors = ['#0066CC', '#0077DD', '#0088EE', '#0099FF'];
  for (let i = 0; i < 4; i++) {
    const x = i * TILE_SIZE;
    const y = 0;
    ctx.fillStyle = waterFrameColors[i];
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);

    ctx.fillStyle = '#FFFFFF44';
    for (let w = 0; w < 3; w++) {
      const wx = x + 4 + w * 10 + i * 3;
      const wy = y + 10 + Math.sin(i + w) * 5;
      ctx.beginPath();
      ctx.arc(wx % (x + TILE_SIZE - 4), wy, 3, 0, Math.PI);
      ctx.fill();
    }

    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x, y, TILE_SIZE, TILE_SIZE);
  }

  for (let i = 4; i < 8; i++) {
    const x = i * TILE_SIZE;
    ctx.fillStyle = '#333333';
    ctx.fillRect(x, 0, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x, 0, TILE_SIZE, TILE_SIZE);
  }

  const lavaFrameColors = ['#FF4500', '#FF6347', '#FF7F50', '#FF8C00'];
  for (let i = 0; i < 4; i++) {
    const x = i * TILE_SIZE;
    const y = TILE_SIZE;
    ctx.fillStyle = lavaFrameColors[i];
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);

    ctx.fillStyle = '#FFD70066';
    ctx.beginPath();
    ctx.arc(x + 16 + i * 2, y + 16, 8 + i, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x, y, TILE_SIZE, TILE_SIZE);
  }

  for (let i = 4; i < 8; i++) {
    const x = i * TILE_SIZE;
    ctx.fillStyle = '#444444';
    ctx.fillRect(x, TILE_SIZE, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x, TILE_SIZE, TILE_SIZE, TILE_SIZE);
  }

  const torchFrameColors = ['#FFD700', '#FFAA00', '#FF8800'];
  for (let i = 0; i < 3; i++) {
    const x = i * TILE_SIZE;
    const y = 2 * TILE_SIZE;
    ctx.fillStyle = '#555555';
    ctx.fillRect(x, y, TILE_SIZE, TILE_SIZE);

    ctx.fillStyle = '#8B4513';
    ctx.fillRect(x + 13, y + 12, 6, 18);

    ctx.fillStyle = torchFrameColors[i];
    ctx.beginPath();
    ctx.arc(x + 16, y + 10 - i, 6 + i, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x, y, TILE_SIZE, TILE_SIZE);
  }

  for (let i = 3; i < 8; i++) {
    const x = i * TILE_SIZE;
    ctx.fillStyle = '#333333';
    ctx.fillRect(x, 2 * TILE_SIZE, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x, 2 * TILE_SIZE, TILE_SIZE, TILE_SIZE);
  }

  for (let i = 0; i < 8; i++) {
    const x = i * TILE_SIZE;
    ctx.fillStyle = '#222222';
    ctx.fillRect(x, 3 * TILE_SIZE, TILE_SIZE, TILE_SIZE);
    ctx.strokeStyle = '#00000033';
    ctx.strokeRect(x, 3 * TILE_SIZE, TILE_SIZE, TILE_SIZE);
  }

  const buffer = canvas.toBuffer('image/png');
  writeFileSync(join(spritesDir, 'objects.png'), buffer);
  console.log('Generated objects.png');
}

function shiftColor(hex, amount) {
  const r = Math.min(255, Math.max(0, parseInt(hex.slice(1, 3), 16) + amount));
  const g = Math.min(255, Math.max(0, parseInt(hex.slice(3, 5), 16) + amount));
  const b = Math.min(255, Math.max(0, parseInt(hex.slice(5, 7), 16) + amount));
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

console.log('Generating sprite sheets...');
generateTerrainSheet();
generateObjectsSheet();
console.log('Done!');
