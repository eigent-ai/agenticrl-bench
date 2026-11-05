"""Counter plugin - counts requests by various dimensions."""

NAME = "counter"
DESCRIPTION = "Count log entries by HTTP method and status code"


def process(lines):
    """Count requests by method and status."""
    methods = {}
    statuses = {}
    for line in lines:
        parts = line.split('"')
        if len(parts) >= 2:
            request = parts[1]
            method = request.split()[0] if request.split() else "UNKNOWN"
            methods[method] = methods.get(method, 0) + 1
        parts2 = line.split()
        if len(parts2) >= 9:
            status = parts2[8]
            statuses[status] = statuses.get(status, 0) + 1
    return {"methods": methods, "statuses": statuses}
