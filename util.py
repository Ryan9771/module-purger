import ast
import os
from typing import List


def get_imports_from_file(file_path):
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


# Example usage:
# file_path = "example.py"  # Path to the Python file
# imported_modules = get_imports_from_file(file_path)
# print(f"Modules imported in {file_path}: {imported_modules}")


def traverse_directories(directory: str, exclude_patterns: List[str]):
    pass


if __name__ == "__main__":
    import os

    for dirpath, dirname, filenames in os.walk("samples/"):
        for filename in filenames:
            if filename.endswith(".py"):
                print(filename)
