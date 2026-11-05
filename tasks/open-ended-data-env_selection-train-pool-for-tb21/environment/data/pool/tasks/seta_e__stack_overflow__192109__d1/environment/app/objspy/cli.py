"""CLI entry point for the objspy introspection library."""
import sys

from objspy.inspector import inspect_object
from objspy.formatter import format_report
from objspy.models import Base, Config, Vehicle, PluginRegistry


def demo():
    """Run the demo inspection on sample objects."""
    objects = [
        ("Base instance", Base("example")),
        ("Config instance", Config("app-config")),
        ("Vehicle instance", Vehicle("Toyota", "Camry", 2024, ["GPS", "Bluetooth"])),
        ("PluginRegistry instance", PluginRegistry()),
    ]

    for label, obj in objects:
        print(f"\n{'=' * 60}")
        print(f"  {label}")
        print(f"{'=' * 60}")
        report = inspect_object(obj)
        output = format_report(report)
        print(output)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        print("Usage: python -m objspy.cli demo")
        sys.exit(1)


if __name__ == "__main__":
    main()
