from util import get_modules_from_directory
import sys

if __name__ == "__main__":
    excluded_files = ["venv"]

    if len(sys.argv) < 2:
        directory = "."
    else:
        # Input arguments to the function
        directory = sys.argv[1]
        excluded_files = excluded_files + sys.argv[2:]

    modules = get_modules_from_directory(
        directory=directory, excluded_patterns=excluded_files
    )

    print(modules)
