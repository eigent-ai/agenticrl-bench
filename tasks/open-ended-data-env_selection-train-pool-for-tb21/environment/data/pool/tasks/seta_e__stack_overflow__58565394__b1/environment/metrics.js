/**
 * Classification metrics module.
 *
 * Provides functions for computing cross-entropy loss and accuracy
 * for multiclass and binary classification problems.
 */

const EPS = 1e-10;

/**
 * Categorical cross-entropy loss.
 *
 * @param {number[][]} yTrueOneHot - Array of one-hot encoded ground-truth labels,
 *   e.g. [[1,0,0,0], [0,0,1,0], ...]. Each inner array has length K (number of classes).
 * @param {number[][]} yPred - Array of predicted probability distributions,
 *   each row sums to 1. Shape: [N, K].
 * @returns {number} Scalar mean loss.
 */
function categoricalCrossentropy(yTrueOneHot, yPred) {
  const N = yTrueOneHot.length;
  let total = 0;
  for (let i = 0; i < N; i++) {
    total += yTrueOneHot[i].reduce((sum, val, j) => {
      return sum + val * Math.log(Math.max(Math.min(yPred[i][j], 1.0), EPS));
    }, 0);
  }
  return -total / N;
}

/**
 * Sparse categorical cross-entropy loss.
 *
 * @param {number[]} yTrueInt - Array of integer class indices, e.g. [2, 0, 3, 1, ...].
 * @param {number[][]} yPred - Array of predicted probability distributions,
 *   each row sums to 1. Shape: [N, K].
 * @returns {number} Scalar mean loss.
 */
function sparseCategoricalCrossentropy(yTrueInt, yPred) {
  const N = yTrueInt.length;
  let total = 0;
  for (let i = 0; i < N; i++) {
    const p = yPred[i][yTrueInt[i]];
    total += Math.log(Math.max(Math.min(p, 1.0), EPS));
  }
  return -total / N;
}

/**
 * Categorical accuracy.
 *
 * @param {number[][]} yTrueOneHot - Array of one-hot encoded ground-truth labels.
 *   Each inner array has length K.
 * @param {number[][]} yPred - Array of predicted probability distributions. Shape: [N, K].
 * @returns {number} Scalar accuracy in [0, 1].
 */
function categoricalAccuracy(yTrueOneHot, yPred) {
  const N = yTrueOneHot.length;
  let correct = 0;
  for (let i = 0; i < N; i++) {
    const trueIdx = yTrueOneHot[i].indexOf(Math.max(...yTrueOneHot[i]));
    const predIdx = yPred[i].indexOf(Math.max(...yPred[i]));
    if (trueIdx === predIdx) correct++;
  }
  return correct / N;
}

/**
 * Sparse categorical accuracy.
 *
 * @param {number[]} yTrueInt - Array of integer class indices.
 * @param {number[][]} yPred - Array of predicted probability distributions. Shape: [N, K].
 * @returns {number} Scalar accuracy in [0, 1].
 */
function sparseCategoricalAccuracy(yTrueInt, yPred) {
  const N = yTrueInt.length;
  let correct = 0;
  for (let i = 0; i < N; i++) {
    const predIdx = yPred[i].indexOf(Math.max(...yPred[i]));
    if (yTrueInt[i] === predIdx) correct++;
  }
  return correct / N;
}

/**
 * Binary cross-entropy loss.
 *
 * @param {number[]} yTrue - Array of binary labels (0 or 1).
 * @param {number[]} yPredProb - Array of predicted probabilities for the positive class
 *   (single number per sample, e.g. [0.7, 0.3, 0.9, ...]). NOT a 2D array.
 * @returns {number} Scalar mean loss.
 */
function binaryCrossentropy(yTrue, yPredProb) {
  const N = yTrue.length;
  let total = 0;
  for (let i = 0; i < N; i++) {
    const p = Math.min(Math.max(yPredProb[i], EPS), 1.0 - EPS);
    total += yTrue[i] * Math.log(p) + (1.0 - yTrue[i]) * Math.log(1.0 - p);
  }
  return -total / N;
}

module.exports = {
  categoricalCrossentropy,
  sparseCategoricalCrossentropy,
  categoricalAccuracy,
  sparseCategoricalAccuracy,
  binaryCrossentropy,
};
