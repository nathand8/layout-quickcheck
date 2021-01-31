import os

class FileConfig:
    bug_report_file_dir: str
    layout_file_dir: str

    def __init__(self):
        cwd = os.getcwd()
        cwd = cwd.replace("\\", "/")
        self.bug_report_file_dir = os.environ.get("BUG_REPORT_FILE_DIR", f"{cwd}/bugreportfiles")
        self.layout_file_dir = os.environ.get("LAYOUT_FILE_DIR", f"{cwd}/layoutfiles")

        if not os.path.exists(self.layout_file_dir):
            os.makedirs(self.layout_file_dir)
        if not os.path.exists(self.bug_report_file_dir):
            os.makedirs(self.bug_report_file_dir)
