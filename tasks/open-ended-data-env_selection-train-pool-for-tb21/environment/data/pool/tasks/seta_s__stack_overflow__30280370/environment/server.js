const express = require('express');
const path = require('path');
const securityMiddleware = require('./middleware/security');
const adminSecurityMiddleware = require('./middleware/admin-security');
const pagesRouter = require('./routes/pages');
const apiRouter = require('./routes/api');

const app = express();
const PORT = 3000;

app.use(securityMiddleware);

app.use('/admin', adminSecurityMiddleware);

app.use('/', pagesRouter);
app.use('/api', apiRouter);

app.listen(PORT, () => {
  console.log(`Dashboard server running on port ${PORT}`);
});

module.exports = app;
