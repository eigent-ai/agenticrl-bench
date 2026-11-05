// Video chat module with cross-browser support

navigator.getUserMedia = navigator.getUserMedia ||
  navigator.webkitGetUserMedia ||
  navigator.mozGetUserMedia ||
  navigator.msGetUserMedia;

function onLocalStream(stream) {
  var localVideo = document.getElementById('local-video');
  localVideo.src = window.URL.createObjectURL(stream);
  localVideo.play();
  sendStreamToRemote(stream);
}

function onStreamError(err) {
  showError('Could not access camera: ' + err.message);
}

function startVideoChat() {
  navigator.getUserMedia({video: true, audio: true}, onLocalStream, onStreamError);
}

function sendStreamToRemote(stream) {
  console.log('Sending stream to remote peer');
}

function showError(msg) {
  document.getElementById('error-banner').textContent = msg;
}

module.exports = { startVideoChat };
