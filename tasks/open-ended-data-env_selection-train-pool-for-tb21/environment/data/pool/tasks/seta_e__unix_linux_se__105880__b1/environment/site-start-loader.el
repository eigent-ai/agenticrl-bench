;; Ensure site-start.d files are loaded
(when (file-directory-p "/etc/emacs/site-start.d")
  (mapc 'load (directory-files "/etc/emacs/site-start.d" t "^[0-9].*\\.el$")))
