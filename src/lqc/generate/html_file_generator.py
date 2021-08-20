import os

def save_file(filepath, layout):
    with open(filepath, 'w') as html_file:
        html_file.write(layout)


def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print(f"Removing File Error: File not found {filepath}")


