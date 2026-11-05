" Syntax highlighting for application log files (.applog)
" Apply this filetype to *.applog files
if exists("b:current_syntax")
  finish
endif

syntax match applogTimestamp /\d\{4}-\d\{2}-\d\{2} \d\{2}:\d\{2}:\d\{2}/
syntax match applogError /\[ERROR\].*/
syntax match applogWarn  /\[WARN\].*/
syntax match applogInfo  /\[INFO\].*/

highlight applogTimestamp ctermfg=cyan guifg=cyan
highlight applogError ctermfg=red guifg=red
highlight applogWarn  ctermfg=yellow guifg=yellow
highlight applogInfo  ctermfg=blue guifg=blue

let b:current_syntax = "applog"
