;; Site-wide backup and auto-save configuration
;; Route all backup and auto-save files to /var/tmp for centralized storage
(setq backup-directory-alist '(("." . "/var/tmp")))
(setq auto-save-file-name-transforms '((".*" "/var/tmp/" t)))
