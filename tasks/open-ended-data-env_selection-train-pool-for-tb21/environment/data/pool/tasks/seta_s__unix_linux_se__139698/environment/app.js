// Application entry point
(function() {
    'use strict';

    var App = {
        version: '2.4.1',
        initialized: false,

        init: function() {
            if (this.initialized) return;
            this.initialized = true;
            this.bindEvents();
            console.log('Application v' + this.version + ' started');
        },

        bindEvents: function() {
            document.addEventListener('DOMContentLoaded', function() {
                var menuToggle = document.querySelector('.menu-toggle');
                if (menuToggle) {
                    menuToggle.addEventListener('click', App.toggleMenu);
                }
            });
        },

        toggleMenu: function() {
            var nav = document.querySelector('nav');
            if (nav) {
                nav.classList.toggle('open');
            }
        }
    };

    window.App = App;
    App.init();
})();
