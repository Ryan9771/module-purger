import ast
import os
from pathlib import Path
from typing import List


def get_imports_from_file(file_path: str) -> List[str]:
    """
    Gets a list of module imports from a given file.

    Args:
    - file_path: The path of the file to extract imports from.

    Returns:
    - List[str]: A list of the imports extracted from the file
    """
    with open(file_path, "r") as file:
        file_content = file.read()

    # Parse the file into an AST
    tree = ast.parse(file_content)

    # Initialize an empty list to hold the import names
    imports = []

    # Walk through the AST nodes
    for node in ast.walk(tree):
        # Check for standard imports: `import module`
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        # Check for from-imports: `from module import ...`
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module if node.module else ""
            imports.append(module_name)

    return imports


def should_exclude(path: Path, exclusions: List[str]) -> bool:
    """
    Checks if the given path should be excluded based on the exclusion patterns.

    Args:
    - path (Path): Path to check.
    - exclusions (List[str]): List of exclusion patterns.

    Returns:
    - bool: True if the path matches an exclusion pattern, else False.
    """
    for pattern in exclusions:
        if path.match(pattern):
            return True

    return False


def traverse_directory(directory: str, excluded_patterns: List[str]) -> List[Path]:
    """
    Traverses all files in the specified directory and its recursive directories,
    printing all filenames that don't match the patterns in `exclusions`.

    Args:
    - directory (str): Directory to traverse.
    - exclusions (List[str]): List of patterns to exclude.
    """
    base_dir = Path(directory)
    included_files = []

    for curr_raw_path, dirs, files in os.walk(base_dir):
        curr_path = Path(curr_raw_path)

        # Exclude directories if they match the exclusion patterns
        dirs[:] = [
            d for d in dirs if not should_exclude(curr_path / d, excluded_patterns)
        ]

        for file in files:
            file_path = curr_path / file
            if not should_exclude(file_path, excluded_patterns):
                if file.endswith(".py"):
                    included_files.append(file_path)

    return [file.name for file in included_files]
