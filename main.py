from util import traverse_directory
import sys

if __name__ == "__main__":
    excluded_files = ["venv"]

    if len(sys.argv) < 2:
        directory = "."
    else:
        # Input arguments to the function
        directory = sys.argv[1]
        excluded_files = excluded_files + sys.argv[2:]

    included_files = traverse_directory(
        directory=directory, excluded_patterns=excluded_files
    )

    print(included_files)
