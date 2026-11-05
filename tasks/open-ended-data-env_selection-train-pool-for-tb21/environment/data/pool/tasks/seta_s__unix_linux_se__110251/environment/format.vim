" Strip trailing whitespace from all lines
%s/\s\+$//e

" Collapse runs of 2+ blank lines into a single blank line
%s/\n\{3,}/\r\r/e

" Remove trailing blank lines at end of file
%s/\n\+\%$//e

" Go to top
1
