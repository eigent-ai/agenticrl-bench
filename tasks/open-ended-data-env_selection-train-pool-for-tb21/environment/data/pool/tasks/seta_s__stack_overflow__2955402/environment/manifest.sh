#!/bin/bash
# Manifest and template rendering

MANIFEST_FILE=""

init_manifest() {
    MANIFEST_FILE="$1"
    : > "$MANIFEST_FILE"
}

add_to_manifest() {
    local path="$1"
    echo "$path" >> "$MANIFEST_FILE"
}

render_article() {
    local title="$1"
    local body="$2"
    local template_content
    template_content=$(cat "templates/article.html")
    template_content="${template_content//\{\{TITLE\}\}/$title}"
    template_content="${template_content//\{\{BODY\}\}/$body}"
    echo "$template_content"
}
