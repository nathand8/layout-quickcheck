from web_page_creation.create import save_as_web_page
from file_config import FileConfig

def saveTestSubjectAsWebPage(test_subject):
    file_config = FileConfig()
    filepath, filename = file_config.getTimestampFilePath()
    save_as_web_page(test_subject, filepath)
    url = f"http://localhost:8000/{file_config.relative_url_path}/{filename}"

    return filepath, url
