"""
Log file viewer utilities.

Provides functions for reading the tail of log files with pagination support.
"""


def tail(f, n, offset=None):
    """Reads n lines from f with an offset of offset lines from the end.

    The return value is a tuple (lines, has_more) where has_more is True
    if there are more lines in the file before the returned window.

    Args:
        f: file object opened in text mode for reading
        n: number of lines to return
        offset: number of lines to skip from the end for pagination (None or 0 = no skip)

    Returns:
        tuple: (list of str lines, bool indicating if earlier lines exist)

    Example:
        For a file with lines [A, B, C, D, E, F, G, H, I, J] (10 lines):
          tail(f, 3, 0)  -> (["H", "I", "J"], True)
          tail(f, 3, 3)  -> (["D", "E", "F"], True)
          tail(f, 3, 7)  -> (["A", "B", "C"], False)
    """
    avg_line_length = 74
    to_read = n + (offset or 0)

    while True:
        try:
            f.seek(-(avg_line_length * to_read), 2)
        except IOError:
            f.seek(0)
        pos = f.tell()
        lines = f.read().splitlines()
        if len(lines) >= to_read or pos == 0:
            result_lines = lines[-n:]
            has_more = len(lines) > to_read
            return result_lines, has_more
        avg_line_length = int(avg_line_length * 1.3)
