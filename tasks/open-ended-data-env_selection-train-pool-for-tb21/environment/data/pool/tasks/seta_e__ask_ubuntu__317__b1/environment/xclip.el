;;; xclip.el --- Use xclip/xsel to access the system clipboard in terminal  -*- lexical-binding: t; -*-

;; Copyright (C) 2007-2022  Free Software Foundation, Inc.
;; Author: Leo Liu <sdl.web@gmail.com>
;; Version: 1.11
;; Keywords: convenience, tools
;; URL: https://elpa.gnu.org/packages/xclip.html

;;; Commentary:
;; This package allows Emacs to copy to and paste from the GUI clipboard
;; when running in a text terminal.

;;; Code:

(defvar xclip-program nil
  "Name of the clipboard program.")

(defvar xclip-select-enable-clipboard t
  "Non-nil means cutting and pasting uses the clipboard.")

(defvar xclip--original-gui-get nil)
(defvar xclip--original-gui-set nil)

(defun xclip--find-program ()
  "Find a suitable clipboard program."
  (or xclip-program
      (cl-find-if #'executable-find '("xclip" "xsel" "pbcopy" "wl-copy"))))

(defun xclip-get-selection (&optional type)
  "Get the system clipboard selection.
TYPE is the selection type, defaults to CLIPBOARD."
  (let ((prog (xclip--find-program)))
    (when prog
      (with-output-to-string
        (cond
         ((string-match "xclip" prog)
          (call-process prog nil standard-output nil
                        "-selection" (or (and type (symbol-name type)) "clipboard")
                        "-o"))
         ((string-match "xsel" prog)
          (call-process prog nil standard-output nil
                        (if (eq type 'PRIMARY) "-o" "--clipboard" )))
         ((string-match "pbpaste" prog)
          (call-process "pbpaste" nil standard-output nil))
         ((string-match "wl-paste" prog)
          (call-process "wl-paste" nil standard-output nil "-n")))))))

(defun xclip-set-selection (type data)
  "Set the system clipboard selection to DATA.
TYPE is the selection type."
  (let ((prog (xclip--find-program)))
    (when (and prog data)
      (cond
       ((string-match "xclip" prog)
        (let ((process-connection-type nil))
          (let ((proc (start-process "xclip" nil prog
                                     "-selection"
                                     (or (and type (symbol-name type)) "clipboard")
                                     "-i")))
            (process-send-string proc data)
            (process-send-eof proc))))
       ((string-match "xsel" prog)
        (let ((process-connection-type nil))
          (let ((proc (start-process "xsel" nil prog
                                     (if (eq type 'PRIMARY) "-i" "--clipboard"))))
            (process-send-string proc data)
            (process-send-eof proc))))
       ((string-match "pbcopy" prog)
        (let ((process-connection-type nil))
          (let ((proc (start-process "pbcopy" nil "pbcopy")))
            (process-send-string proc data)
            (process-send-eof proc))))
       ((string-match "wl-copy" prog)
        (let ((process-connection-type nil))
          (let ((proc (start-process "wl-copy" nil "wl-copy")))
            (process-send-string proc data)
            (process-send-eof proc))))))))

(defun xclip-gui-set-selection (type data)
  "Xclip implementation of `gui-set-selection'."
  (if (not data)
      (when xclip--original-gui-set
        (funcall xclip--original-gui-set type data))
    (xclip-set-selection type data)
    data))

(defun xclip-gui-get-selection (type &optional data-type)
  "Xclip implementation of `gui-get-selection'."
  (or (xclip-get-selection type)
      (when xclip--original-gui-get
        (funcall xclip--original-gui-get type data-type))))

;;;###autoload
(define-minor-mode xclip-mode
  "Minor mode to use the system clipboard in terminal Emacs.
When this mode is enabled, Emacs uses xclip, xsel, or similar
tools to interface with the system clipboard for copy and paste."
  :global t
  :lighter " XClip"
  (if xclip-mode
      (progn
        (setq xclip--original-gui-set (symbol-function 'gui-set-selection))
        (setq xclip--original-gui-get (symbol-function 'gui-selection-exists-p))
        ;; In batch mode or when display is not available, just activate
        (when (and (not (display-graphic-p))
                   (not noninteractive))
          (advice-add 'gui-set-selection :override #'xclip-gui-set-selection)
          (advice-add 'gui-get-selection :override #'xclip-gui-get-selection)))
    (advice-remove 'gui-set-selection #'xclip-gui-set-selection)
    (advice-remove 'gui-get-selection #'xclip-gui-get-selection)))

(provide 'xclip)

;;; xclip.el ends here
