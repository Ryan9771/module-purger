from util import module_purger
import sys

if __name__ == "__main__":
    excluded_files = ["venv"]

    if len(sys.argv) < 2:
        directory = "."
    else:
        # Input arguments to the function
        directory = sys.argv[1]
        excluded_files = excluded_files + sys.argv[2:]

    module_purger(directory=directory, excluded_patterns=excluded_files)
