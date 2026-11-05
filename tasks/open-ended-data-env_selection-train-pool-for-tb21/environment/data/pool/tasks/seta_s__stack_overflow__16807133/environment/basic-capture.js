// Basic camera capture module

function onCaptureSuccess(stream) {
  var video = document.getElementById('camera-preview');
  video.src = window.URL.createObjectURL(stream);
  video.play();
}

function onCaptureError(err) {
  console.error('Camera error:', err);
}

function startCapture() {
  navigator.getUserMedia({video: true}, onCaptureSuccess, onCaptureError);
}

module.exports = { startCapture };
