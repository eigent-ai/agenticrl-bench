"""Binary file analysis CLI tool.

Provides subcommands for analyzing binary files:
  hexdump - Display hex dump of file contents
  freq    - Show byte frequency histogram
  search  - Search for byte patterns
"""

import argparse
import sys
from bintools.hexdump import hexdump
from bintools.frequency import frequency
from bintools.search import search


def cmd_hexdump(args):
    """Run hexdump subcommand."""
    hexdump(args.file)


def cmd_freq(args):
    """Run frequency analysis subcommand."""
    frequency(args.file)


def cmd_search(args):
    """Run pattern search subcommand."""
    pattern = bytes.fromhex(args.pattern) if args.hex else args.pattern.encode()
    search(args.file, pattern)


def main():
    """Main entry point for the binary analysis toolkit."""
    parser = argparse.ArgumentParser(
        description="Binary file analysis toolkit"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    p_hex = subparsers.add_parser("hexdump", help="Display hex dump of file")
    p_hex.add_argument("file", help="Path to binary file")
    p_hex.set_defaults(func=cmd_hexdump)

    p_freq = subparsers.add_parser("freq", help="Byte frequency histogram")
    p_freq.add_argument("file", help="Path to binary file")
    p_freq.set_defaults(func=cmd_freq)

    p_search = subparsers.add_parser("search", help="Search for byte pattern")
    p_search.add_argument("file", help="Path to binary file")
    p_search.add_argument("pattern", help="Pattern to search for")
    p_search.add_argument("--hex", action="store_true",
                          help="Interpret pattern as hex string")
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


main()
