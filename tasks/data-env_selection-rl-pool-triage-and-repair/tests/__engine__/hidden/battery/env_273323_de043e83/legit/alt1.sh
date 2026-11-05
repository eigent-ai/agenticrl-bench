#!/bin/bash
set -eu
BIN=/usr/local/bin/file-opener
SYSCONF=/etc/file-opener/associations.ini
mkdir -p "$(dirname "$BIN")" "$(dirname "$SYSCONF")"
cat > "$SYSCONF" <<'INI'
; file-opener associations
; Per-user overrides: ${XDG_CONFIG_HOME:-~/.config}/file-opener/associations.ini
; An explicit file can be given with FILE_OPENER_CONFIG=/path/to/file.ini
; Values are shell commands; %f is replaced by the file path (otherwise the path is appended).
;
; [extensions]
; md = less
; log = tail -n 50
;
; [mime]
; application/json = cat
; image/* = identify -verbose
[extensions]

[mime]
INI
chmod 0644 "$SYSCONF"
cat > "$BIN" <<'OPENER'
#!/bin/bash
PROG=${0##*/}
SYSCONF=/etc/file-opener/associations.ini
USERCONF=${XDG_CONFIG_HOME:-$HOME/.config}/file-opener/associations.ini

err() { printf '%s: %s\n' "$PROG" "$*" >&2; }

usage() {
cat <<EOF
Usage: $PROG [--dry-run] FILE...
       $PROG --list
       $PROG --help

Opens each FILE with the handler associated with its type.
Lookup order: user/system INI associations by extension, then by MIME type,
then built-in defaults. In a graphical session xdg-open is used for the
built-in defaults; without a display text-mode handlers are used:
  text      -> less (cat when output is not a terminal)
  pdf       -> pdftotext | pager
  html      -> lynx -dump (tag stripping if lynx is missing)
  images    -> ImageMagick identify (file if missing)

Config files (later wins): $SYSCONF, $USERCONF, \$FILE_OPENER_CONFIG
Exit codes: 0 ok, 1 usage, 2 file missing/unreadable, 3 unsupported type, 4 handler missing, other: handler status
EOF
}

declare -A EXT_MAP=() MIME_MAP=()

load_ini() {
    local f=$1 section="" line key val
    [ -r "$f" ] || return 0
    while IFS= read -r line || [ -n "$line" ]; do
        line=${line%$'\r'}
        line=${line#"${line%%[![:space:]]*}"}
        case $line in
            ''|\;*|\#*) continue ;;
            \[*\]) section=${line#[}; section=${section%]}; section=${section,,}; continue ;;
        esac
        [[ $line == *=* ]] || continue
        key=${line%%=*}; val=${line#*=}
        key=${key%"${key##*[![:space:]]}"}; key=${key,,}
        val=${val#"${val%%[![:space:]]*}"}
        [ -n "$key" ] && [ -n "$val" ] || continue
        case $section in
            extensions|extension|ext) EXT_MAP[${key#.}]=$val ;;
            mime|mimetypes|types) MIME_MAP[$key]=$val ;;
        esac
    done < "$f"
}

load_all_config() {
    load_ini "$SYSCONF"
    load_ini "$USERCONF"
    if [ -n "${FILE_OPENER_CONFIG:-}" ]; then
        [ -r "$FILE_OPENER_CONFIG" ] || { err "config file not readable: $FILE_OPENER_CONFIG"; exit 1; }
        load_ini "$FILE_OPENER_CONFIG"
    fi
}

have() { command -v "$1" >/dev/null 2>&1; }

gui_available() { [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ] && have xdg-open; }

pager_cmd() {
    if [ -t 1 ] && have less; then echo 'less'; else echo 'cat'; fi
}

builtin_handler() {
    local ext=$1 mime=$2 kind=""
    case $ext in
        txt|text|md|log|csv|conf|ini|sh|py) kind=text ;;
        pdf) kind=pdf ;;
        html|htm|xhtml) kind=html ;;
        jpg|jpeg|png|gif|bmp|webp|tif|tiff) kind=image ;;
    esac
    if [ -z "$kind" ]; then
        case $mime in
            application/pdf) kind=pdf ;;
            text/html|application/xhtml+xml) kind=html ;;
            image/*) kind=image ;;
            text/*|application/json|application/xml|inode/x-empty) kind=text ;;
        esac
    fi
    [ -n "$kind" ] || return 1
    if gui_available; then echo 'xdg-open'; return 0; fi
    case $kind in
        text)  pager_cmd ;;
        pdf)   if have pdftotext; then echo "pdftotext -layout %f - | $(pager_cmd)"; else echo 'MISSING:pdftotext'; fi ;;
        html)  if have lynx; then echo 'lynx -dump -force_html %f'
               elif have w3m; then echo 'w3m -dump -T text/html %f'
               else echo "sed -e 's/<[^>]*>//g' %f"; fi ;;
        image) if have identify; then echo 'identify'
               elif have file; then echo 'file'
               else echo 'MISSING:identify'; fi ;;
    esac
}

resolve_handler() {
    local path=$1 base ext mime
    base=${path##*/}
    ext=""
    [[ $base == *.* ]] && ext=${base##*.} && ext=${ext,,}
    mime=$(file -b --mime-type -- "$path" 2>/dev/null || true)
    if [ -n "$ext" ] && [ -n "${EXT_MAP[$ext]+x}" ]; then echo "${EXT_MAP[$ext]}"; return 0; fi
    if [ -n "$mime" ] && [ -n "${MIME_MAP[$mime]+x}" ]; then echo "${MIME_MAP[$mime]}"; return 0; fi
    if [ -n "$mime" ] && [ -n "${MIME_MAP[${mime%%/*}/*]+x}" ]; then echo "${MIME_MAP[${mime%%/*}/*]}"; return 0; fi
    builtin_handler "$ext" "$mime"
}

open_one() {
    local path=$1 dry=$2 handler prog script
    if [ ! -e "$path" ]; then err "file not found: $path"; return 2; fi
    if [ -d "$path" ]; then err "is a directory: $path"; return 2; fi
    if [ ! -r "$path" ]; then err "file not readable: $path"; return 2; fi
    if ! handler=$(resolve_handler "$path"); then
        err "unsupported file type: $path ($(file -b --mime-type -- "$path" 2>/dev/null || echo unknown))"
        return 3
    fi
    if [[ $handler == MISSING:* ]]; then
        err "no handler installed for $path (need ${handler#MISSING:})"
        return 4
    fi
    prog=${handler%% *}
    if ! have "$prog"; then
        err "handler '$prog' for $path is not installed"
        return 4
    fi
    if [[ $handler == *%f* ]]; then
        script=${handler//%f/\"\$1\"}
    else
        script="$handler \"\$1\""
    fi
    if [ "$dry" = 1 ]; then
        printf '%s -> %s\n' "$path" "$handler"
        return 0
    fi
    bash -c "$script" "$PROG" "$path"
}

dry=0
files=()
while [ $# -gt 0 ]; do
    case $1 in
        -h|--help) usage; exit 0 ;;
        -n|--dry-run) dry=1 ;;
        --list)
            load_all_config
            for k in "${!EXT_MAP[@]}"; do printf 'ext  .%s = %s\n' "$k" "${EXT_MAP[$k]}"; done
            for k in "${!MIME_MAP[@]}"; do printf 'mime %s = %s\n' "$k" "${MIME_MAP[$k]}"; done
            exit 0 ;;
        --) shift; files+=("$@"); break ;;
        -*) err "unknown option: $1"; usage >&2; exit 1 ;;
        *) files+=("$1") ;;
    esac
    shift
done

[ ${#files[@]} -gt 0 ] || { usage >&2; exit 1; }
load_all_config
status=0
for f in "${files[@]}"; do
    open_one "$f" "$dry" || status=$?
done
exit "$status"
OPENER
chmod 0755 "$BIN"
