'use strict';

/**
 * AABB overlap test.
 * Returns true if object1 and object2 overlap.
 */
function collision(o1, o2) {
  return !(
    o1.x > o2.x + o2.w ||
    o1.x + o1.w < o2.x ||
    o1.y > o2.y + o2.h ||
    o1.y + o1.h < o2.y
  );
}

/**
 * Returns the side of object2 that object1 is hitting, using the
 * minimum-penetration-depth heuristic.
 *
 * Returns: 'left' | 'right' | 'top' | 'bottom' | null
 */
function detectSide(player, enemy) {
  if (!collision(player, enemy)) return null;

  var playerCenterX = player.x + player.w / 2;
  var playerCenterY = player.y + player.h / 2;
  var enemyCenterX  = enemy.x  + enemy.w  / 2;
  var enemyCenterY  = enemy.y  + enemy.h  / 2;

  var diffX = playerCenterX - enemyCenterX;
  var diffY = playerCenterY - enemyCenterY;

  var minXDist = player.w / 2 + enemy.w / 2;
  var minYDist = player.h / 2 + enemy.h / 2;

  var depthX = diffX > 0 ? minXDist - diffX : -minXDist - diffX;
  var depthY = diffY > 0 ? minYDist - diffY : -minYDist - diffY;

  if (depthX !== 0 && depthY !== 0) {
    if (Math.abs(depthX) > Math.abs(depthY)) {
      return depthX > 0 ? 'right' : 'left';
    } else {
      return depthY > 0 ? 'bottom' : 'top';
    }
  }
  return null;
}

module.exports = { collision, detectSide };
