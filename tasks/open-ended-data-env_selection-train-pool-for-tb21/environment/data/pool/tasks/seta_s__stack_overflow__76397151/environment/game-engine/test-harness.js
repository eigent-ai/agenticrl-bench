import { Engine } from './src/index.js';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function runDiagnostic() {
  console.log('=== Tile Engine Diagnostic ===\n');

  const engine = new Engine({
    tileSize: 64,
    targetFps: 60,
    viewportWidth: 640,
    viewportHeight: 480,
    startX: 64,
    startY: 64,
  });

  const tileSize = 64;
  const startX = engine.getPlayerPosition().x;
  const startY = engine.getPlayerPosition().y;

  console.log(`Initial position: (${startX}, ${startY})`);
  console.log(`Tile size: ${tileSize}`);
  console.log(`Player speed: ${engine.state.player.speed}`);
  console.log(`Update timestep: ${engine.state.performance.updateTimeStep}ms`);
  console.log();

  // Test 1: Simulate at 240Hz display (4x the 60Hz update rate)
  console.log('--- Test 1: Movement at 240Hz display rate ---');
  const displayInterval = 1000 / 240; // ~4.17ms per frame
  let timestamp = 0;

  // Run a few frames to initialize
  for (let i = 0; i < 10; i++) {
    timestamp += displayInterval;
    engine.tick(timestamp);
  }

  // Queue a RIGHT movement
  engine.queueInput('RIGHT');
  timestamp += displayInterval;
  engine.tick(timestamp);

  // Wait for movement to complete via setInterval
  const moveComplete = new Promise(resolve => {
    engine.state.player.onMoveComplete(() => resolve());
    setTimeout(() => resolve(), 5000); // timeout safety
  });

  // Keep ticking while movement happens
  const tickInterval = setInterval(() => {
    timestamp += displayInterval;
    engine.tick(timestamp);
  }, 4);

  await moveComplete;
  clearInterval(tickInterval);

  const finalPos = engine.getPlayerPosition();
  const expectedX = startX + tileSize;
  console.log(`Expected position after RIGHT: (${expectedX}, ${startY})`);
  console.log(`Actual position: (${finalPos.x}, ${finalPos.y})`);
  console.log(`Position correct: ${finalPos.x === expectedX && finalPos.y === startY}`);
  console.log();

  // Analyze frame log for judder
  const log = engine.frameLog;
  const renderWithoutUpdate = log.filter(f => !f.updated).length;
  const totalFrames = log.length;
  console.log(`Total frames: ${totalFrames}`);
  console.log(`Renders without update: ${renderWithoutUpdate}`);
  console.log(`Update efficiency: ${((totalFrames - renderWithoutUpdate) / totalFrames * 100).toFixed(1)}%`);
  console.log();

  // Check for position jitter (same position appearing in non-consecutive frames)
  let jitterCount = 0;
  for (let i = 2; i < log.length; i++) {
    if (log[i].playerX === log[i-2].playerX && log[i].playerX !== log[i-1].playerX) {
      jitterCount++;
    }
  }
  console.log(`Position jitter events: ${jitterCount}`);

  // Check camera smoothness
  let cameraJumps = 0;
  for (let i = 1; i < log.length; i++) {
    const dx = Math.abs(log[i].cameraX - log[i-1].cameraX);
    if (dx > engine.state.player.speed + 1) {
      cameraJumps++;
    }
  }
  console.log(`Camera jumps (>speed+1 px): ${cameraJumps}`);

  engine.destroy();

  // Test 2: Collision detection
  console.log('\n--- Test 2: Collision at boundaries ---');
  const engine2 = new Engine({
    tileSize: 64,
    targetFps: 60,
    startX: 64,
    startY: 64,
  });

  // Try to walk into wall at (0, 64) - column 0 is wall
  engine2.queueInput('LEFT');
  let ts2 = 0;
  for (let i = 0; i < 5; i++) {
    ts2 += 1000 / 60;
    engine2.tick(ts2);
  }

  const posAfterWall = engine2.getPlayerPosition();
  console.log(`After LEFT into wall: (${posAfterWall.x}, ${posAfterWall.y})`);
  console.log(`Blocked by wall: ${posAfterWall.x === 64}`);

  engine2.destroy();

  console.log('\n=== Diagnostic Complete ===');
}

runDiagnostic().catch(console.error);
