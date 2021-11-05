import os
from shutil import copy2
from lqc.config.file_config import FileConfig
from lqc.generate.web_page.create import save_as_web_page
from lqc.generate.web_page.javascript_minimal.create import EXTERNAL_JS_FILE_PATHS

def copyExternalJSFiles(folder):
    for filepath in EXTERNAL_JS_FILE_PATHS:
        copy2(filepath, folder)

def saveTestSubjectAsWebPage(run_subject):
    file_config = FileConfig()
    folder, filepath, filename = file_config.getTimestampFilePath()
    copyExternalJSFiles(folder)
    save_as_web_page(run_subject, filepath)
    url = "file://" + os.path.abspath(filepath)

    return filepath, url
