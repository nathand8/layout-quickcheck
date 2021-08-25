import traceback
import platform
from lqc.model.run_subject import RunSubject
from lqc_runner.selenium_harness.layout_tester import test_combination
from lqc_runner.variants.variants import getTargetVariant, getVariants


def format_variant_result(webdriver, description, is_original_variant, diff_method="Python", forced_slow=False):

    browser_name = webdriver.capabilities['browserName']
    browser_name = browser_name.capitalize()
    browser_version = "unknown"
    if "browserVersion" in webdriver.capabilities:
        browser_version = webdriver.capabilities['browserVersion']
    elif "version" in webdriver.capabilities:
        browser_version = webdriver.capabilities['version']
    window_size = webdriver.get_window_size()
    return {
        "description": description,
        "browser": browser_name,
        "browser_version": browser_version,
        "is_original_variant": is_original_variant,
        "window_size": window_size,
        "diff_method": diff_method,
        "forced_slow": forced_slow,
        "os_name": platform.system(),
        "os_details": platform.platform()
    }


def print_crash_output(variant_description):
    """
    Print helpful output after crashing
    """
    exception_lines = traceback.format_exc().splitlines()
    nonblank_lines = list(filter(lambda x: x, exception_lines))
    lastline = nonblank_lines[-1] if len(nonblank_lines) > 0 else ""
    print(f"Variant '{variant_description}' Failed: \n  {lastline}")


def test_variants(run_subject: RunSubject):

    variant_results = []
    for variant in getVariants():
        try:
            webdriver = variant["driver"]()
            is_original_variant = variant is getTargetVariant()
            result = format_variant_result(webdriver, variant["name"], is_original_variant, forced_slow=["force_slow"])
            bug_gone, *_ = test_combination(webdriver, run_subject, slow=variant["force_slow"])
            result["bug_detected"] = not bug_gone
            variant_results.append(result)
        except:
            print_crash_output(variant["name"])
        finally:
            try: webdriver.finish()
            except: pass

    # Summarize the variant_results
    summary = {}
    for v in variant_results:
        summary[v["description"]] = v["bug_detected"]

    return {
        "Test Variant Summary": summary,
        "Test Variant Details": variant_results
    }
