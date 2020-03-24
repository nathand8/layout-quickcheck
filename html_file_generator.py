from layout_generator import generate_layout
from datetime import datetime

timestamp_format = '%Y-%m-%d-%H-%M-%S-%f'

def generate_html_file(path):
  layout = generate_layout()

  timestamp = datetime.now()
  formatted_timestamp = timestamp.strftime(timestamp_format)
  file_name = f'test-file-{formatted_timestamp}.html'

  with open(f'{path}/{file_name}', 'w') as html_file:
    html_file.write(layout)
  
  return file_name
