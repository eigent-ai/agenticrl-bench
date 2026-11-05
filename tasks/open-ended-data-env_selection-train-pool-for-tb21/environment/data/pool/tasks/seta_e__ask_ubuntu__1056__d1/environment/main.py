"""
Main entry point for the terminal text input widget.
"""

from terminal_handler import create_handler


def main():
    print("Terminal Text Input Widget")
    print("Type text and press Enter to submit. Ctrl-C to cancel.")
    print("-" * 40)

    handler = create_handler()
    result = handler.run()

    print(f"\nYou entered: {result}")


if __name__ == "__main__":
    main()
