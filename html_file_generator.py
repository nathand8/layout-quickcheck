def save_file(path, formatted_timestamp, layout, postfix=''):
    new_file_name = f'test-file-{formatted_timestamp}{postfix}.html'

    with open(f'{path}/{new_file_name}', 'w') as html_file:
        html_file.write(layout)

    return new_file_name
