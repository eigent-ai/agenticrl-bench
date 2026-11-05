// Dual camera module - switches between front and rear cameras

// @camera: front
function startFrontCamera() {
  navigator.getUserMedia(
    {video: true},
    function(stream) {
      var video = document.getElementById('front-view');
      video.src = window.URL.createObjectURL(stream);
      video.play();
    },
    function(err) {
      console.error('Front camera error:', err);
    }
  );
}

// @camera: rear
function startRearCamera() {
  navigator.getUserMedia(
    {video: true},
    function(stream) {
      var video = document.getElementById('rear-view');
      video.src = window.URL.createObjectURL(stream);
      video.play();
    },
    function(err) {
      console.error('Rear camera error:', err);
    }
  );
}

module.exports = { startFrontCamera, startRearCamera };
