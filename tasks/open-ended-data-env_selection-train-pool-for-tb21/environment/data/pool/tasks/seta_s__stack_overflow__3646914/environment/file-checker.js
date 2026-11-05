const http = require('http');

/**
 * Check if a file exists by making an HTTP HEAD request to the static endpoint.
 * This avoids direct filesystem access and leverages the existing static middleware.
 */
function checkFileExists(relativePath) {
    return new Promise((resolve) => {
        const options = {
            hostname: 'localhost',
            port: 3000,
            path: `/static/${relativePath}`,
            method: 'HEAD',
            timeout: 3000
        };

        const req = http.request(options, (res) => {
            resolve(res.statusCode === 200);
        });

        req.on('error', () => {
            resolve(false);
        });

        req.on('timeout', () => {
            req.destroy();
            resolve(false);
        });

        req.end();
    });
}

module.exports = { checkFileExists };
