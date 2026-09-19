"""Allow ``python -m promptlint``."""

import sys

from promptlint.cli import main

if __name__ == "__main__":
    sys.exit(main())
