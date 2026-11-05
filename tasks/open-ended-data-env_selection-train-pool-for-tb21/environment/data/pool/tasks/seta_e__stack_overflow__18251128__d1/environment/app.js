var API_BASE = 'http://' + window.location.host + '/api';

document.addEventListener('DOMContentLoaded', function() {
    console.log('WebApp initialized');
    console.log('API endpoint: ' + API_BASE);

    var statusEl = document.querySelector('.app-status');
    if (statusEl) {
        statusEl.textContent = 'Connected to ' + API_BASE;
    }
});

function fetchData(endpoint) {
    return fetch(API_BASE + '/' + endpoint)
        .then(function(response) {
            return response.json();
        })
        .catch(function(error) {
            console.error('API Error:', error);
        });
}
