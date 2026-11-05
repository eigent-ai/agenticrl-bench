document.addEventListener('DOMContentLoaded', function() {
    console.log('Site loaded successfully');
    var title = document.querySelector('h1');
    if (title) {
        title.style.cursor = 'pointer';
    }
});
