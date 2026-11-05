'use strict';
const http = require('http');
const PORT = process.env.PORT;
if (!PORT) {
  process.stderr.write('Fatal: PORT environment variable is not set\n');
  process.exit(1);
}
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('webapp running\n');
});
server.listen(parseInt(PORT, 10), '127.0.0.1', () => {
  process.stdout.write(`Server listening on 127.0.0.1:${PORT}\n`);
});
