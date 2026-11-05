function normalize(str) {
  return str.replace(/\n/g, "\r\n");
}

module.exports = normalize;
