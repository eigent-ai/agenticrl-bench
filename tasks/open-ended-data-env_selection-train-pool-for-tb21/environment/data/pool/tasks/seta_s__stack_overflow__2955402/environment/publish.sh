#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PUBLISH_DIR="/srv/publish"
CONTENT_DIR="${SCRIPT_DIR}/content"

source "${SCRIPT_DIR}/lib/mkpath.sh"
source "${SCRIPT_DIR}/lib/pathutil.sh"
source "${SCRIPT_DIR}/lib/safefile.sh"
source "${SCRIPT_DIR}/lib/manifest.sh"

init_manifest "$(join_path "$PUBLISH_DIR" "manifest.txt")"

for article_file in "${CONTENT_DIR}"/*.txt; do
    [ -f "$article_file" ] || continue

    title=""
    date_val=""
    slug=""
    body=""
    in_body=0

    while IFS= read -r line; do
        if [ "$in_body" -eq 0 ]; then
            if [ -z "$line" ]; then
                in_body=1
                continue
            fi
            key="${line%%:*}"
            val="${line#*: }"
            case "$key" in
                title) title="$val" ;;
                date)  date_val="$val" ;;
                slug)  slug="$val" ;;
            esac
        else
            if [ -n "$body" ]; then
                body="${body}
${line}"
            else
                body="$line"
            fi
        fi
    done < "$article_file"

    year="${date_val%%-*}"
    rest="${date_val#*-}"
    month="${rest%%-*}"

    article_dir=$(join_path "$PUBLISH_DIR" "${year}/${month}/${slug}")
    ensure_dir "$article_dir"

    output_file="${article_dir}/index.html"
    rendered=$(render_article "$title" "$body")
    safe_write "$output_file" "$rendered"

    rel_path="${year}/${month}/${slug}/index.html"
    add_to_manifest "$rel_path"
done

generate_feed() {
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<rss version="2.0">'
    echo '<channel>'
    echo '<title>Content Publisher Feed</title>'

    for article_file in "${CONTENT_DIR}"/*.txt; do
        [ -f "$article_file" ] || continue
        title=""
        while IFS= read -r line; do
            if [ -z "$line" ]; then break; fi
            key="${line%%:*}"
            val="${line#*: }"
            if [ "$key" = "title" ]; then title="$val"; fi
        done < "$article_file"
        echo "<item><title>${title}</title></item>"
    done

    echo '</channel>'
    echo '</rss>'
}

generate_feed > /srv/publish/feed.xml
