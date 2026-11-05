"""
Logging configuration linter.

Validates Log4j2/Logback XML configuration files and reports issues
such as invalid log levels, missing required elements, and
inappropriate settings for production environments.
"""

import xml.etree.ElementTree as ET
import os
import re


VALID_LEVELS = {'TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL', 'OFF', 'ALL'}


def lint_config(filepath):
    """Lint a logging configuration XML file.

    Args:
        filepath: Path to the XML configuration file

    Returns:
        List of issue dicts with keys: line, severity, message
    """
    issues = []

    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.splitlines()

    # Validate XML structure before parsing
    for i, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if stripped_line.startswith('<?xml'):
            continue
        if not stripped_line.startswith('<') or stripped_line.startswith('<!--'):
            issues.append({
                'line': i,
                'severity': 'error',
                'message': 'XML parse error: invalid content before root element'
            })
            return issues
        break

    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        issues.append({
            'line': 1,
            'severity': 'error',
            'message': f'XML parse error: {e}'
        })
        return issues

    # Check all level attributes
    for i, line in enumerate(lines, start=1):
        level_match = re.search(r'level\s*=\s*"([^"]+)"', line, re.IGNORECASE)
        if level_match:
            level = level_match.group(1).upper()
            if level not in VALID_LEVELS:
                issues.append({
                    'line': i,
                    'severity': 'error',
                    'message': f'Invalid log level: {level_match.group(1)}'
                })

    # Check for appender references
    for appender_ref in root.iter():
        if appender_ref.tag.lower() in ('appender-ref', 'appenderref'):
            ref = appender_ref.get('ref')
            if ref:
                found = False
                for appender in root.iter():
                    if appender.tag.lower() in ('appender', 'console', 'file', 'rollingfile'):
                        if appender.get('name') == ref:
                            found = True
                            break
                if not found:
                    issues.append({
                        'line': 1,
                        'severity': 'warning',
                        'message': f'Appender reference "{ref}" not found'
                    })

    return issues
