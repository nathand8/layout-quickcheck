import os
from datetime import datetime

timestamp_format = "%Y-%m-%d-%H-%M-%S-%f"

def get_file_path(parent_path):
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime(timestamp_format)
    filename = f'test-file-{formatted_timestamp}.html'
    filepath = os.path.join(parent_path, filename)
    return filepath, filename


def save_file(filepath, layout):
    with open(filepath, 'w') as html_file:
        html_file.write(layout)


def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print(f"Removing File Error: File not found {filepath}")


