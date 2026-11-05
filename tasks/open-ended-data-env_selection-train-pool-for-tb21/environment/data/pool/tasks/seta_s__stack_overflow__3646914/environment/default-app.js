// Default Theme JavaScript
(function() {
    'use strict';

    function initTheme() {
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Default theme initialized');
            applyThemeSettings();
        });
    }

    function applyThemeSettings() {
        var elements = document.querySelectorAll('[data-theme-toggle]');
        elements.forEach(function(el) {
            el.addEventListener('click', function() {
                document.body.classList.toggle('dark-mode');
            });
        });
    }

    initTheme();
})();
