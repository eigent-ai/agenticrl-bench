#!/bin/bash

BASEDIR="$(cd "$(dirname "$0")" && pwd)"

source "$BASEDIR/lib/parse_config.sh"
source "$BASEDIR/lib/build_modeline.sh"
source "$BASEDIR/lib/color_temp.sh"
source "$BASEDIR/lib/apply_gamma.sh"

mkdir -p "$BASEDIR/output"
OUTPUT="$BASEDIR/output/setup.sh"

echo "#!/bin/bash" > "$OUTPUT"
echo "# Display setup script - auto-generated" >> "$OUTPUT"
echo "" >> "$OUTPUT"

generate_color_temp "$OUTPUT"

parse_monitors "$BASEDIR/monitors.conf"

echo "# Monitor output configuration" >> "$OUTPUT"
generate_modelines "$OUTPUT"

echo "" >> "$OUTPUT"
apply_gamma_settings "$OUTPUT"

echo "" >> "$OUTPUT"
echo "echo 'Display configuration applied.'" >> "$OUTPUT"

chmod +x "$OUTPUT"
