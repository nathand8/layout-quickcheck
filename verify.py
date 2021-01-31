from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from layout_tester import run_test_on_page
import os
from test_subject import TestSubject
from test_config import TestConfig


if __name__ == "__main__":

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_webdriver = WebDriver(
        executable_path=os.environ.get("CHROME_DRIVER_PATH"), options=chrome_options
    )

    # chrome_webdriver.set_window_size(1000, 1000)

    browser_version = chrome_webdriver.capabilities['browserVersion']
    driver_version = chrome_webdriver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print("Chrome Version   :", browser_version)
    print("WebDriver Version:", driver_version)

    # url = "http://localhost:8000/odd-behavior-bugs/bug-report-2021-01-27-12-02-28-983697-minified-34/bug.html"
    # modified_styles = {"faab94b323c14fdbb3fdb364b2597c0e": {"padding-right": "1459mm", "white-space": "break-spaces"}}

    url = "http://localhost:8000/bugreportfiles/bug-report-2021-01-30-23-05-19-908613-minified-136/bug.html"
    modified_styles = {"e2349c93c3e74b21990e6865b688b794": {"animation-direction": "alternate", "font-feature-settings": "normal", "clip-path": "none", "line-height-step": "-1546vmin", "offset-path": "none", "overscroll-behavior-x": "none", "overscroll-behavior-y": "none", "padding-top": "1758em", "scroll-margin-right": "+103vmin", "scroll-padding-left": "auto", "text-justify": "auto", "text-underline-offset": "auto", "transform": "none", "y": "1537ch", "margin-inline-start": "510vi", "inset-block-end": "-961vh"}, "f9e5a944ea9c45da90087170f27235a4": {"animation-direction": "alternate-reverse", "animation-fill-mode": "backwards", "font-kerning": "normal", "font-weight": "bold", "font-feature-settings": "normal", "text-rendering": "optimizespeed", "backdrop-filter": "none", "backface-visibility": "visible", "border-image-width": "-25vw", "bottom": "auto", "box-sizing": "border-box", "caret-color": "auto", "counter-set": "none", "cx": "992cm", "d": "none", "flood-color": "currentcolor", "height": "-695vmin", "left": "1449mm", "lighting-color": "currentcolor", "offset-distance": "+1227rlh", "overflow-y": "scroll", "padding-right": "518vmin", "perspective": "+82vh", "right": "auto", "scroll-margin-inline-end": "-1782vh", "scroll-padding-right": "auto", "scroll-snap-type": "both", "shape-outside": "none", "shape-rendering": "auto", "text-decoration-color": "currentcolor", "text-decoration-style": "wavy", "top": "-480rem", "column-span": "none", "z-index": "auto", "margin-block-end": "1602rlh", "inset-inline-start": "1682in"}} 

    test_subject = TestSubject({}, {}, modified_styles)
    test_config = TestConfig(chrome_webdriver, "")

    differences = run_test_on_page(url, test_config, test_subject)

    print("differences:", differences)
