document.addEventListener('DOMContentLoaded', function() {
    console.log('Application initialized');
    fetch('/api/data')
        .then(function(response) { return response.json(); })
        .then(function(data) { console.log('API data:', data); });
});
