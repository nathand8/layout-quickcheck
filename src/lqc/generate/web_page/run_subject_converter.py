import os
from lqc.config.file_config import FileConfig
from lqc.generate.web_page.create import save_as_web_page

def saveTestSubjectAsWebPage(run_subject):
    file_config = FileConfig()
    filepath, filename = file_config.getTimestampFilePath()
    save_as_web_page(run_subject, filepath)
    url = "file://" + os.path.abspath(filepath)

    return filepath, url
