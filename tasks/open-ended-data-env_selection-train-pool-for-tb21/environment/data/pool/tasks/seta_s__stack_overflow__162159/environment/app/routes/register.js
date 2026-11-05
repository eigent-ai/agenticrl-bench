const express = require('express');
const router = express.Router();
const { createValidationMiddleware } = require('../middleware/validate');
const { validateRegistration } = require('../validators/register');
const store = require('../store');

router.post('/register', createValidationMiddleware(validateRegistration), (req, res) => {
  const user = store.addUser(req.body);
  res.status(200).json({ message: 'Registration successful', user });
});

module.exports = router;
