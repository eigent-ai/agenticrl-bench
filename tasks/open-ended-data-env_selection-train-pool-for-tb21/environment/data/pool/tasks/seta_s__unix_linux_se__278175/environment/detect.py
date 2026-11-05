#!/usr/bin/env python3
"""Terminal capability detection and reporting tool.

Reports installed programming fonts and terminal color support.
Writes a JSON report to OUTPUT_PATH.
"""

import json
import os
import subprocess

# Font families to check for
FONT_FAMILIES = ["FiraCode", "Iosevka", "Monoid"]

# Output path for the generated report
OUTPUT_PATH = "/var/lib/termcap-report/report.json"

# Terminal type used when probing color depth via tput
TERM_OVERRIDE = "dumb"


def get_installed_font_families():
    """Return the set of all font family names known to fontconfig."""
    result = subprocess.run(
        ["fc-list"],
        capture_output=True,
        text=True,
        check=True,
    )
    families = set()
    for line in result.stdout.splitlines():
        # fc-list standard output format:
        #   /path/to/font.ttf: Family Name:style=Style
        if ":" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                for fam in parts[1].split(","):
                    families.add(fam.strip())
    return families


def get_font_styles(family):
    """Return a sorted list of style variants available for *family*."""
    result = subprocess.run(
        ["fc-list", f":family={family}"],
        capture_output=True,
        text=True,
    )
    styles = set()
    for line in result.stdout.splitlines():
        if "style=" in line:
            style_val = line.split("style=", 1)[1].strip()
            styles.add(style_val)
    return sorted(styles)


def detect_font_support():
    """Return mapping of found font families to their style lists."""
    installed = get_installed_font_families()
    found = {}
    for family in FONT_FAMILIES:
        if family in installed:
            found[family] = get_font_styles(family)
    return found


def detect_color_support():
    """Probe terminal color depth using tput with TERM_OVERRIDE."""
    env = os.environ.copy()
    env["TERM"] = TERM_OVERRIDE

    tput_result = subprocess.run(
        ["tput", "colors"],
        capture_output=True,
        text=True,
        env=env,
    )
    try:
        num_colors = int(tput_result.stdout.strip())
    except (ValueError, AttributeError):
        num_colors = 8

    colorterm = os.environ.get("COLORTERM", "")

    return {
        "num_colors": num_colors,
        "supports_256color": num_colors >= 256,
        "supports_truecolor": colorterm in ("truecolor", "24bit"),
    }


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    fonts = detect_font_support()
    colors = detect_color_support()

    report = {
        "fonts": fonts,
        "color_capabilities": colors,
        "font_count": len(fonts),
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
