#!/usr/bin/python
# Validation CGI endpoint

import sys
import os

def main():
    print("Content-type: text/html\n")
    print("<html><body>")
    print("<p>Validation: Checking environment...</p>")
    script_name = os.path.basename(sys.argv[0])
    print(f"<p>Script: {script_name}</p>")
    print("<p>Validation: OK</p>")
    print("</body></html>")
    return 0

if __name__ == "__main__":
    sys.exit(main())
