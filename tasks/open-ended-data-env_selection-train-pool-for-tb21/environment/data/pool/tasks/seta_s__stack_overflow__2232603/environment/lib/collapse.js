function collapse(str) {
  return str.replace(/\n\n\s*\n\n/g, "\n");
}

module.exports = collapse;
