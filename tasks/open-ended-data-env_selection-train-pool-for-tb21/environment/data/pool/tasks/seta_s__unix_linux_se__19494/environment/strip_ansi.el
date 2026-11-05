;; strip_ansi.el
;; Strips ANSI escape sequences from a file
;; Usage: emacs --batch -l strip_ansi.el -- input.col output.txt

(defun strip-ansi-from-file (infile outfile)
  "Strip ANSI escape sequences from INFILE and write clean text to OUTFILE."
  (with-temp-buffer
    (insert-file-contents infile)
    (ansi-color-apply-on-region beg end)
    (write-region (point-min) (point-max) outfile)))

(let ((args command-line-args-left))
  (when (= (length args) 2)
    (strip-ansi-from-file (nth 0 args) (nth 1 args))
    (setq command-line-args-left nil)))
