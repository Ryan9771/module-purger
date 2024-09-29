import ast
import os
from pathlib import Path
from typing import List, Tuple


def replace_requirements(used_modules: List[str]) -> None:
    """
    Creates a new requirements.txt file with the used modules.

    Args:
    - used_modules (List[str]): List of modules to include in the requirements file.
    """

    # Archives the old requirements file
    os.rename("requirements.txt", "requirements-old.txt")

    # Writes the new requirements file
    with open("requirements.txt", "w") as file:
        for module in used_modules:
            file.write(f"{module}\n")


def get_used_modules(
    installed_modules: List[Tuple[str, str]], used_modules: List[str]
) -> List[str]:
    """
    Gets modules that are not in the required modules list.

    Args:
    - Installed modules (List[str]): List of modules to filter.
    - required_modules (List[str]): List of modules to keep.

    Returns:
    - List[str]: List of modules that are in `modules` and `required_modules`.
    """
    return [
        f"{module_name}=={version}"
        for (module_name, version) in installed_modules
        if module_name in used_modules
    ]


def get_modules_from_requirements() -> List[str]:
    """
    Gets a list of tuples of installed (module_name, module_verisons) from the requirements.txt file.
    """
    with open("requirements.txt", "r") as file:
        requirements = file.readlines()

    modules = []
    for requirement in requirements:
        if requirement.startswith("#"):
            continue

        module_and_version = requirement.split("==")
        modules.append((module_and_version[0], module_and_version[1].strip()))

    print(f"==== Modules: {modules} ====")

    return modules


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


def traverse_directory(directory: str, excluded_patterns: List[str]) -> List[str]:
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

    return [str(file) for file in included_files]


def get_modules_from_directory(
    directory: str, excluded_patterns: List[str]
) -> List[str]:
    """
    Gets all the modules that are imported in the .py files in the specified directory.

    Args:
    - directory (str): Directory to search for .py files.
    - excluded_patterns (List[str]): List of patterns to exclude.

    Returns:
    - List[str]: List of modules that are imported in the .py files in the directory.
    """

    # Gets the filepaths of all the .py files that are not excluded
    file_paths = traverse_directory(
        directory=directory, excluded_patterns=excluded_patterns
    )

    # Gets the modules that were imported from each file
    modules = []
    for file_path in file_paths:
        try:
            modules_from_file = get_imports_from_file(file_path=file_path)
        except Exception as e:
            print(f"==== Error processing file: {file_path} ====")
            modules_from_file = []

        modules += modules_from_file

    return modules


def module_purger(directory: str, excluded_patterns: List[str]) -> None:
    """
    Purges the unused modules from the requirements.txt file.

    Args:
    - directory (str): Directory to search for .py files.
    - excluded_patterns (List[str]): List of patterns to exclude.
    """
    # Get the modules from the requirements.txt file
    installed_modules = get_modules_from_requirements()

    # Get the modules from the directory
    used_modules = get_modules_from_directory(
        directory=directory, excluded_patterns=excluded_patterns
    )

    # Get the used modules
    filtered_modules = get_used_modules(
        installed_modules=installed_modules, used_modules=used_modules
    )

    # Replace the requirements.txt file
    replace_requirements(used_modules=filtered_modules)
