#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

    from django.core.management import execute_from_command_line

    # Allow starting the app without installing the module.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

    execute_from_command_line(sys.argv)
