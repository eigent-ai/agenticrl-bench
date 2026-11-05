const math = require('mathjs');
const { matrixMultiply } = require('./lib/matmul');
const { parDot } = require('./lib/parallel_dot');
require('./config');  // applies UV_THREADPOOL_SIZE

async function run(n = 150) {
    const A = math.random([n, n]).toArray();
    const B = math.random([n, n]).toArray();
    const serial = matrixMultiply(A, B);
    const parallel = await parDot(A, B, 2, 2);
    return [serial, parallel];
}

if (require.main === module) {
    run().then(([s, p]) => {
        console.log(`simulation done  serial_norm=${math.norm(s).toFixed(4)}  parallel_norm=${math.norm(p).toFixed(4)}`);
    });
}

module.exports = { run };
