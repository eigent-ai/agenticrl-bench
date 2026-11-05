const adminSecurityMiddleware = (req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'none'; script-src 'self'; style-src 'self'"
  );
  next();
};

module.exports = adminSecurityMiddleware;
