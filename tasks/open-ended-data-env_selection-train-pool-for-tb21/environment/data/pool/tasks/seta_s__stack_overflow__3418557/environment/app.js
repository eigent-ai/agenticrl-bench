document.addEventListener('DOMContentLoaded', function() {
    console.log('Application loaded');
    fetch('/api/status')
        .then(response => response.json())
        .then(data => console.log('API status:', data.status));
});
