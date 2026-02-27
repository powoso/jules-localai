import os

def read_file_content(filepath):
    """
    Reads the content of a file.

    Args:
        filepath (str): The path to the file.

    Returns:
        tuple: (content (str), error (str))
               If successful, content is the string and error is None.
               If failed, content is None and error is the error message.
    """
    if not os.path.exists(filepath):
        return None, f"File not found: {filepath}"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read(), None
    except Exception as e:
        return None, f"Error reading file {filepath}: {e}"

def list_text_files(directory, ignore_dirs=None):
    """
    Lists all text files in a directory, ignoring specified directories.

    Args:
        directory (str): The directory to walk.
        ignore_dirs (list, optional): A list of directory names to ignore. Defaults to None.

    Returns:
        list: A list of file paths.
    """
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', 'node_modules', 'venv', '.env', '.idea', '.vscode']

    # Normalize ignore_dirs to lower case for case-insensitive matching
    ignore_dirs = set(d.lower() for d in ignore_dirs)

    text_files = []

    for root, dirs, files in os.walk(directory):
        # Filter directories to skip in-place
        dirs[:] = [d for d in dirs if d.lower() not in ignore_dirs]

        for file in files:
            # Simple check for text files based on extension (can be expanded)
            if file.lower().endswith(('.py', '.txt', '.md', '.js', '.ts', '.html', '.css', '.json', '.sh', '.yaml', '.yml', '.toml')):
                 text_files.append(os.path.join(root, file))

    return text_files
