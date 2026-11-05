function wrap(text, width) {
  var lines = text.split('\n');
  var result = [];
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (line.length <= width) {
      result.push(line);
    } else {
      var chunks = line.match(new RegExp("/.{" + width + "}/", "g"));
      if (chunks) {
        result = result.concat(chunks);
      }
      var remainder = line.slice((chunks ? chunks.length : 0) * width);
      if (remainder) {
        result.push(remainder);
      }
    }
  }
  return result.join('\n');
}

module.exports = wrap;
