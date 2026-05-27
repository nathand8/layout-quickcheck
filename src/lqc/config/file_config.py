import os
from datetime import datetime

from lqc.config.config import Config

timestamp_format = "%Y-%m-%d-%H-%M-%S-%f"


class FileConfig:
    bug_report_file_dir: str
    layout_file_dir: str


    def __init__(self):
        config = Config()
        self.bug_report_file_dir = config.getBugReportDirectory()
        self.layout_file_dir = config.getTmpFilesDirectory()

        if not os.path.exists(self.layout_file_dir):
            os.makedirs(self.layout_file_dir)
        if not os.path.exists(self.bug_report_file_dir):
            os.makedirs(self.bug_report_file_dir)
            
    def getCustomTimestampPath(self, custom_folder: str):
        timestamp = datetime.now()
        formatted_timestamp = timestamp.strftime(timestamp_format)
        custom_dir = os.path.join(self.bug_report_file_dir, custom_folder)
        if not os.path.exists(custom_dir):
            os.makedirs(custom_dir)        
        dirpath = os.path.join(custom_dir, f"{custom_folder}-{formatted_timestamp}")
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        return dirpath
