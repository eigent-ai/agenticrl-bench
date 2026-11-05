function fixedPoint(f, start, tolerance = 1e-9, maxIter = 10000) {
  let x = Number(start);
  let nextX;
  for (let i = 0; i < maxIter; i++) {
    nextX = f(x);
    if (Math.abs(nextX - x) < tolerance) {
      return nextX;
    }
    x = nextX;
  }
  throw new Error(
    `fixedPoint did not converge after ${maxIter} iterations ` +
    `(last two values: ${x.toFixed(6)}, ${nextX.toFixed(6)})`
  );
}

function sqrtViaFixedPoint(n) {
  if (n < 0) {
    throw new RangeError("sqrt undefined for negative numbers");
  }
  return fixedPoint((x) => n / x, 1.0);
}

function cubeRootViaFixedPoint(n) {
  return fixedPoint((x) => n / (x * x), n >= 0 ? 1.0 : -1.0);
}

module.exports = { fixedPoint, sqrtViaFixedPoint, cubeRootViaFixedPoint };
