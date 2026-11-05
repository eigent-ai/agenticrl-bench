"""Errors plugin - extracts error entries from logs."""

NAME = "errors"
DESCRIPTION = "Extract and summarize error log entries (4xx/5xx)"


def process(lines):
    """Extract lines with error status codes."""
    error_lines = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 9:
            try:
                status = int(parts[8])
                if status >= 400:
                    error_lines.append(line.strip())
            except ValueError:
                pass
    return {"error_count": len(error_lines), "errors": error_lines}
