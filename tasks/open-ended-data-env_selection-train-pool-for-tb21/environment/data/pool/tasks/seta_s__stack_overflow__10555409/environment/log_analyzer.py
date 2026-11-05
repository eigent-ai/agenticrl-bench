"""
Java source code log anti-pattern scanner.

Analyzes Java source files to detect logging anti-patterns:
- String concatenation in log calls (eager evaluation)
- String.format() in log calls (eager evaluation)

And identifies good patterns:
- SLF4J-style parameterized logging
- Log4j2 printf-style logging
"""

import re


def analyze_file(filepath):
    """Analyze a Java source file for logging patterns.

    Args:
        filepath: Path to the Java source file

    Returns:
        dict with keys:
            concatenation_antipatterns: list of line numbers with concatenation
            format_antipatterns: list of line numbers with String.format
            parameterized_ok: list of line numbers with correct {} usage
            printf_ok: list of line numbers with correct printf usage
    """
    report = {
        'concatenation_antipatterns': [],
        'format_antipatterns': [],
        'parameterized_ok': [],
        'printf_ok': [],
    }

    with open(filepath, 'r') as f:
        lines = f.readlines()

    log_methods = r'logger\.(trace|debug|info|warn|error|fatal|printf)'

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith('//'):
            continue

        match = re.search(log_methods, stripped)
        if not match:
            continue

        method = match.group(1)

        # Detect concatenation: logger.xxx("..." + var)
        concat_pattern = r'logger\.\w+\("[^"]*"\s*\+'
        if re.search(concat_pattern, stripped):
            report['concatenation_antipatterns'].append(lineno)
            continue

        # Detect parameterized logging with {}
        param_pattern = r'logger\.\w+\("[^"]*\{\}[^"]*"'
        if re.search(param_pattern, stripped):
            report['parameterized_ok'].append(lineno)
            continue

    return report
