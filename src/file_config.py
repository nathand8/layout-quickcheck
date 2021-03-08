import os
from datetime import datetime

timestamp_format = "%Y-%m-%d-%H-%M-%S-%f"


class FileConfig:
    bug_report_file_dir: str
    layout_file_dir: str


    def __init__(self):
        cwd = os.getcwd()
        cwd = cwd.replace("\\", "/")
        self.bug_report_file_dir = os.environ.get("BUG_REPORT_FILE_DIR", f"{cwd}/bugreportfiles")
        self.layout_file_dir = os.environ.get("LAYOUT_FILE_DIR", f"{cwd}/layoutfiles")
        self.relative_url = os.getenv("RELATIVE_LAYOUT_URL", "layoutfiles")

        if not os.path.exists(self.layout_file_dir):
            os.makedirs(self.layout_file_dir)
        if not os.path.exists(self.bug_report_file_dir):
            os.makedirs(self.bug_report_file_dir)
    

    def getTimestampFilePath(self):
        timestamp = datetime.now()
        formatted_timestamp = timestamp.strftime(timestamp_format)
        filename = f'test-file-{formatted_timestamp}.html'
        filepath = os.path.join(self.layout_file_dir, filename)
        return filepath, filename
    

    def getTimestampBugReport(self):
        timestamp = datetime.now()
        formatted_timestamp = timestamp.strftime(timestamp_format)
        bug_folder = os.path.join(self.bug_report_file_dir, f"bug-report-{formatted_timestamp}")
        return bug_folder