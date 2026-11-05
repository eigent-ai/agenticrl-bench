function createValidationMiddleware(validatorFn) {
  return (req, res, next) => {
    const errors = validatorFn(req.body);
    next();
    if (errors.length > 0) {
      return res.status(400).json({ errors: errors });
    }
  };
}

module.exports = { createValidationMiddleware };
