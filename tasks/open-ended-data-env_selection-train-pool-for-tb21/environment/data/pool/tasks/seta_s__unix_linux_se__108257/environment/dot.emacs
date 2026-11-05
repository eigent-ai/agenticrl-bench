;;; ~/.emacs - Emacs initialization file

(setq inhibit-startup-message t)
(setq inhibit-startup-echo-area-message "user")

(setq-default font-lock-maximum-decoration t
(global-font-lock-mode 0)

(defun count-python-defs (file)
  "Count def statements in FILE."
  (with-temp-buffer
    (insert-file-contents file)
    (let ((count 0))
      (goto-char (point-min))
      (while (re-search-forward "^def " nil t)
        (setq count (1+ count)))
      count)))
