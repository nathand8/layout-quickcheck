from datetime import datetime

timestamp_format = '%Y-%m-%d-%H-%M-%S-%f'


def generate_html_file(path, layout):
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime(timestamp_format)
    file_name = f'test-file-{formatted_timestamp}.html'

    with open(f'{path}/{file_name}', 'w') as html_file:
        html_file.write(layout)

    return file_name, formatted_timestamp


def save_modified(path, formatted_timestamp, new_layout):
    new_file_name = f'test-file-{formatted_timestamp}-modified.html'

    with open(f'{path}/{new_file_name}', 'w') as html_file:
        html_file.write(new_layout)

    return new_file_name
