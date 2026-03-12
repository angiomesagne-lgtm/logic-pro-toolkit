import os
import json
import csv
import mimetypes
from typing import List, Dict, Any

def scan_files(directory: str, extensions: List[str]) -> List[str]:
    """
    Scan a directory for files with specified extensions.

    Args:
        directory (str): The directory to scan.
        extensions (List[str]): A list of file extensions to look for.

    Returns:
        List[str]: A list of file paths that match the specified extensions.

    Raises:
        FileNotFoundError: If the directory does not exist.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    
    matched_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                matched_files.append(os.path.join(root, file))
    
    return matched_files

def format_size(bytes: int) -> str:
    """
    Format a size in bytes to a human-readable string.

    Args:
        bytes (int): The size in bytes.

    Returns:
        str: A human-readable representation of the size.
    """
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024**2:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1024**3:
        return f"{bytes / 1024**2:.2f} MB"
    else:
        return f"{bytes / 1024**3:.2f} GB"

def format_duration(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable string.

    Args:
        seconds (float): The duration in seconds.

    Returns:
        str: A human-readable representation of the duration.
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s" if hours else f"{minutes}m {seconds}s"

def export_json(data: Any, path: str) -> None:
    """
    Export data to a JSON file.

    Args:
        data (Any): The data to export.
        path (str): The path to the output JSON file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        raise IOError(f"Error writing to JSON file '{path}': {e}")

def export_csv(data: List[Dict[str, Any]], path: str) -> None:
    """
    Export data to a CSV file.

    Args:
        data (List[Dict[str, Any]]): A list of dictionaries representing rows of data.
        path (str): The path to the output CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    if not data:
        raise ValueError("Data for CSV export is empty.")
    
    try:
        with open(path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        raise IOError(f"Error writing to CSV file '{path}': {e}")

def get_file_info(path: str) -> Dict[str, Any]:
    """
    Get metadata information about a file.

    Args:
        path (str): The path to the file.

    Returns:
        Dict[str, Any]: A dictionary containing file metadata.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")
    
    file_info = {
        'path': path,
        'size': os.path.getsize(path),
        'mime_type': mimetypes.guess_type(path)[0],
        'last_modified': os.path.getmtime(path),
    }
    
    return file_info