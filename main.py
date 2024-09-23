from util import traverse_directory

if __name__ == "__main__":

    # Arguments to the function
    directory = "."
    excluded_files = ["venv", ".git*"]

    included_files = traverse_directory(
        directory=directory, excluded_patterns=excluded_files
    )

    print(included_files)
