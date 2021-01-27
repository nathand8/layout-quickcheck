- Created on the CADE machine
- Can't reproduce problem

Here's what's been tried:
- Web server on CADE machine, port 8000 forwarded to local machine, load page, run "recreateTheProblem();" in console -> No bug
- Web server on local machine, load page, run "recreateTheProblem()" in console -> No bug
- Verify.py on CADE machine -> Bug
- Verify.py on local machine -> Bug
    - Chrome Version: 88.0.4324.96,  WebDriver Version: 87.0.4280.20
- Verify.py on local machine -> Bug
    - Config: remove Chrome flags ('--headless', '--no-sandbox', '--disable-dev-shm-usage')
- Verify.py on local machine -> NO BUG
    - Config: remove Chrome flags ('--headless', '--no-sandbox', '--disable-dev-shm-usage')
    - Put a debugger in the function and walk step by step
- Verify.py on local machine -> NO BUG
    - Config: INCLUDE Chrome flags ('--headless', '--no-sandbox', '--disable-dev-shm-usage')
    - Put a debugger in the function and walk step by step

Conclusion:
- This should NOT be a BUG
- This must have been a RACE CONDITION. The elements were measured the first time before the page had finished loading.

Finding the right wait condition:
- Verify.py on local machine -> NO BUG
    - Put a manual sleep for 1 second after page has loaded, before styles are modified
- Verify.py on local machine -> BUG
    - Wait for elements listed in modified_style_log to be loaded on the page
- Verify.py on local machine -> BUG
    - Wait for manual 0.1 seconds (using time.sleep)
- Verify.py on local machine -> NO BUG
    - Wait for manual 0.5 seconds (using time.sleep)
- Verify.py on local machine -> BUG
    - Wait for manual 0.2 seconds (using time.sleep)
- Verify.py on local machine -> BUG
    - Wait for manual 0.3 seconds (using time.sleep)
- Verify.py on local machine -> NO BUG
    - Wait for manual 0.4 seconds (using time.sleep)
- Verify.py on local machine -> NO BUG
    - Wait for manual 0.4 seconds (using time.sleep)
- Using javascript to determine when page is loaded -> BUG
    - Triggering on document.readyState
- Using javascript to determine when page is loaded -> NO BUG
    - Waiting for one complete timeout cycle
    - This WORKS!... But it's painfully slow. (4x)
- Using javascript to determine when page is loaded -> BUG
    - Waiting for page load event
    - Note: Event had already fired. Had to use https://stackoverflow.com/a/53525488/1457295
    