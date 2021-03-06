from web_page_creation.create import save_as_web_page
from file_config import FileConfig
import os

def saveTestSubjectAsWebPage(run_subject):
    file_config = FileConfig()
    filepath, filename = file_config.getTimestampFilePath()
    save_as_web_page(run_subject, filepath)
    url = "file://" + os.path.abspath(filepath)

    return filepath, url
