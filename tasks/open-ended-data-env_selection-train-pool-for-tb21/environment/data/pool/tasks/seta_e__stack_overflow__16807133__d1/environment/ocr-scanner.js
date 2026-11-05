// @camera: rear
// OCR scanner module - selects rear camera by device source

function onScanStream(stream) {
  var video = document.getElementById('scanner-preview');
  video.src = window.URL.createObjectURL(stream);
  startOCR(video);
}

function onScanError(err) {
  console.error('Scanner error:', err);
}

function initScanner() {
  MediaStreamTrack.getSources(function(sources) {
    var rearCameraId = null;
    sources.forEach(function(source) {
      if (source.kind === 'video' && source.facing === 'environment') {
        rearCameraId = source.id;
      }
    });

    var constraints = {video: true};
    if (rearCameraId) {
      constraints.video = {optional: [{sourceId: rearCameraId}]};
    }

    navigator.getUserMedia(constraints, onScanStream, onScanError);
  });
}

module.exports = { initScanner };
