" Remove comment-only lines (lines starting with #)
g/^#/d
" Remove inline annotations (## and everything after)
g/##/normal dd
" Remove trailing whitespace
%s/\s\+$//e
