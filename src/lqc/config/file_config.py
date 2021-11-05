import os
from datetime import datetime

from lqc.config.config import Config

timestamp_format = "%Y-%m-%d-%H-%M-%S-%f"


class FileConfig:
    bug_report_file_dir: str
    layout_file_dir: str


    def __init__(self):
        config = Config()
        cwd = os.getcwd()
        cwd = cwd.replace("\\", "/")
        self.bug_report_file_dir = config.getBugReportDirectory()
        self.layout_file_dir = config.getTmpFilesDirectory()

        if not os.path.exists(self.layout_file_dir):
            os.makedirs(self.layout_file_dir)
        if not os.path.exists(self.bug_report_file_dir):
            os.makedirs(self.bug_report_file_dir)
    

    def getTimestampFilePath(self):
        timestamp = datetime.now()
        formatted_timestamp = timestamp.strftime(timestamp_format)
        filename = f'test-file-{formatted_timestamp}.html'
        filepath = os.path.join(self.layout_file_dir, filename)
        return self.layout_file_dir, filepath, filename
    

    def getTimestampBugReport(self):
        timestamp = datetime.now()
        formatted_timestamp = timestamp.strftime(timestamp_format)
        bug_folder = os.path.join(self.bug_report_file_dir, f"bug-report-{formatted_timestamp}")
        return bug_folder
