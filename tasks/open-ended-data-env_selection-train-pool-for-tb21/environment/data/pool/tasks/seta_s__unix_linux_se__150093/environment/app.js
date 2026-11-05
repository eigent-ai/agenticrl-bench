const express = require('express');
const app = express();

app.get('/users', (req, res) => {
  res.json({ message: 'User list endpoint' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
