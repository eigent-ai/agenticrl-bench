// @camera: rear
// Rear-facing camera module for barcode scanning

navigator.getUserMedia = navigator.getUserMedia ||
  navigator.webkitGetUserMedia ||
  navigator.mozGetUserMedia ||
  navigator.msGetUserMedia;

function startRearCamera() {
  navigator.getUserMedia(
    {video: true},
    function(stream) {
      var video = document.getElementById('rear-preview');
      video.src = window.URL.createObjectURL(stream);
      video.play();
    },
    function(err) {
      console.error('Rear camera error:', err);
    }
  );
}

module.exports = { startRearCamera };
