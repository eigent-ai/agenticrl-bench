#!/usr/bin/env python3
"""Compare two assembly blocks for equivalence."""

import re


def compare_asm(asm_a, asm_b):
    """Compare two assembly text blocks from objdump output.

    Returns True if the assembly is functionally equivalent.
    Strips address prefixes before comparison.
    """
    def clean_lines(asm):
        lines = []
        for line in asm.strip().split('\n'):
            line = line.strip()
            # Remove the address prefix (e.g., "   0:   ")
            line = re.sub(r'^[0-9a-f]+:\s+', '', line)
            if line:
                lines.append(line)
        return lines

    lines_a = clean_lines(asm_a)
    lines_b = clean_lines(asm_b)

    return lines_a == lines_b
