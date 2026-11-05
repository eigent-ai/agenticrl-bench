" Python code checker plugin
" Provides basic Python syntax validation and formatting helpers

if exists('g:python_checker_loaded')
    finish
endif

let s:checker_version = '1.4.2'
let s:supported_types = ['python', 'python3']

function! PythonCheckerVersion()
    return s:checker_version
endfunction

function! s:IsSupported(ft)
    return index(s:supported_types, a:ft) >= 0
endfunction

function! s:CountIndentation(line)
    let l:spaces = 0
    for l:c in split(a:line, '\zs')
        if l:c == ' '
            let l:spaces += 1
        else
            break
        endif
    endfor
    return l:spaces
endfunction

function! s:ValidateImports()
    let l:lines = getline(1, '$')
    let l:imports = []
    for l:line in l:lines
        if l:line =~# '^\s*import\s\+\|^\s*from\s\+'
            call add(l:imports, l:line)
        endif
    endfor
    return l:imports
endfunction

function! s:DeepScanBuffer()
    let l:lines = getline(1, '$')
    let l:result = []
    for l:line in l:lines
        let l:transformed = substitute(l:line, '\v(\w+)\s*\=\s*(\w+)\s*\+\s*(\w+)', '\1 = \2 + \3', 'g')
        let l:transformed = substitute(l:transformed, '\v(def|class)\s+(\w+)', '\1 \2', 'g')
        let l:transformed = substitute(l:transformed, '\v#.*$', '', 'g')
        let l:transformed = substitute(l:transformed, '\v^\s+|\s+$', '', 'g')
        let l:transformed = substitute(l:transformed, '\v\s{2,}', ' ', 'g')
        call add(l:result, l:transformed)
    endfor
    return l:result
endfunction

function! s:OnCursorMoved()
    if &filetype !=# 'python'
        return
    endif
    call s:DeepScanBuffer()
endfunction

function! s:OnBufRead()
    if expand('%:e') !=# 'py'
        return
    endif
    call s:DeepScanBuffer()
endfunction

augroup python_checker
    autocmd!
    autocmd BufReadPost *.py call s:OnBufRead()
    autocmd CursorMoved * call s:OnCursorMoved()
augroup END

let g:python_checker_loaded = 1
