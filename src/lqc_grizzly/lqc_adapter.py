# Initial structure pulled from
# https://github.com/MozillaSecurity/grizzly/blob/feedback-example/grizzly/adapter/feedback_example/__init__.py

import pathlib
import json
import os
from urllib.parse import unquote
from enum import Enum, unique
from lqc.config.config import Config, parse_config
from lqc.generate.style_log_generator import generate_run_subject
from lqc.generate.web_page.create import html_string

from grizzly.adapter import Adapter
from lqc.generate.web_page.javascript.create import EXTERNAL_JS_FILE_PATHS
from lqc.minify.minify_test_file import MinifyStepFactory
from lqc.model.run_result import RunResultLayoutBug
from lqc.model.run_subject import RunSubject

__author__ = "Tyson Smith"
__credits__ = ["Tyson Smith", "Nathan Davis"]

JS_BOOTSTRAP = """
window.addEventListener("load", test_bug_and_report);
"""

@unique
class Mode(Enum):
    # normal fuzzing operation, generate test cases
    FUZZ = 0
    # reduce mode, apply reduction operations to a single test
    REDUCE = 1
    # no more reductions can be performed indicate we are complete
    REPORT = 2

def getStyleLists(run_subject: RunSubject):
    """ Used for logging lists of styles used """

    base_styles = list(run_subject.base_styles.all_style_names())
    base_styles.sort()
    modified_styles = list(run_subject.modified_styles.all_style_names())
    modified_styles.sort()

    return {
        'base_styles': base_styles,
        'modified_styles': modified_styles
    }

def getSignature(run_subject: RunSubject):
    """Creates a list of all the styles used in a run_subject"""
    styles_used = list(run_subject.all_style_names())
    styles_used.sort()
    return ",".join(styles_used)

class LayoutQuickCheckAdapter(Adapter):
    """LayoutQuickCheckAdapter"""

    NAME = "LayoutQuickCheck-Adapter"
    EXTRA_JS_FILE_NAMES = ["helpers.js", "bootstrap.js"]

    def setup(self, input_path, server_map):
        # indicates if a result was found
        self.fuzz["found"] = False
        # track most recent version of test (for reduction)
        self.fuzz["best"] = None
        # current operation mode
        self.enterFuzzMode()
        self.enable_harness()
        # adds '/found' to server so the test case/browser can send 'signals'
        # back to the framework
        server_map.set_dynamic_response("found", self._found)

        # Load the LayoutQuickCheck Config
        # Config file is specified on the command line with -i
        config = parse_config(input_path)
        Config(config)

    def _found(self, args):
        # callback attached to '/found'
        self.fuzz["found"] = True
        # "run_result" should always be the results from the last bug found
        self.fuzz["run_result"] = RunResultLayoutBug(json.loads(unquote(args)))
        return b""
    
    def _jsDriver(self, run_subject: RunSubject, reporting_bug=False):
        if reporting_bug:
            return """function finish_test(dimensionsDiffer) {
                // window.dump('\\nLQC Signature: ' + result_summary(dimensionsDiffer) + '\\n');
                window.dump('\\nLQC Signature: ' + """ + json.dumps(run_subject.styles_signature()) + """ + '\\n');
                log_bug_details(dimensionsDiffer); 
                window.dump('CSS Styles Used: """ + json.dumps(getStyleLists(run_subject), indent=4).replace("\n", "\\n") + """\\n\\n');
                // FuzzingFunctions.crash(result_summary(dimensionsDiffer));
                FuzzingFunctions.crash(""" + json.dumps(run_subject.styles_signature()) + """);
            }\n""" + JS_BOOTSTRAP
        else:
            return "function finish_test() { setTimeout(window.close, 10) }\n" + JS_BOOTSTRAP

    def enterFuzzMode(self):
        """Fuzz mode generates random tests"""
        self.fuzz["mode"] = Mode.FUZZ
        self.fuzz["found"] = False
        self.fuzz["run_result"] = None
        self.fuzz["best"] = None
        self.fuzz["reported"] = False
    
    def enterReduceMode(self):
        """Reduce mode minifies a single test where a bug is present"""
        self.fuzz["best"] = None
        self.fuzz["mode"] = Mode.REDUCE
        self.fuzz["minifyStepsFactory"] = MinifyStepFactory()

    def enterReportMode(self):
        """Report mode crashes the browser to report the bug"""
        self.fuzz["mode"] = Mode.REPORT

    def generate(self, testcase, _server_map):

        if self.fuzz["mode"] == Mode.FUZZ:
            # generate a test
            self.fuzz["run_subject"] = generate_run_subject()
            jslib = self._jsDriver(self.fuzz["run_subject"])
            # html_string will generate a complete web page with html and inline js
            self.fuzz["test"] = html_string(self.fuzz["run_subject"], extra_js_file_names=self.EXTRA_JS_FILE_NAMES)

        elif self.fuzz["mode"] == Mode.REDUCE:

            # Run one minify step from MinifyStepFactory
            self.fuzz["proposed_run_subject"] = self.fuzz["minifyStepsFactory"].next_minimization_step(self.fuzz["run_subject"])
            # are we done reduction?
            if self.fuzz["proposed_run_subject"] == None:
                self.enterReportMode()
                # html_string will generate a complete web page with html and inline js
                self.fuzz["test"] = html_string(self.fuzz["run_subject"], extra_js_file_names=self.EXTRA_JS_FILE_NAMES)
            else:
                # html_string will generate a complete web page with html and inline js
                self.fuzz["test"] = html_string(self.fuzz["proposed_run_subject"], extra_js_file_names=self.EXTRA_JS_FILE_NAMES)
            jslib = self._jsDriver(self.fuzz["run_subject"])

        elif self.fuzz["mode"] == Mode.REPORT:
            # here we should force crash the browser so grizzly detects a result
            # see bug https://bugzilla.mozilla.org/show_bug.cgi?id=1725008
            # sig = getSignature(self.fuzz["run_subject"])
            self.fuzz["test"] = html_string(self.fuzz["run_subject"], self.fuzz["run_result"], extra_js_file_names=self.EXTRA_JS_FILE_NAMES)
            jslib = self._jsDriver(self.fuzz["run_subject"], reporting_bug=True)
            self.fuzz["reported"] = True

        # Reset the "found" flag
        self.fuzz["found"] = False

        # add a non required file
        testcase.add_from_data(jslib, "bootstrap.js", required=False)

        # add the helper.js file
        helpersJSPath = pathlib.Path(__file__).parent.joinpath('grizzly_test_helpers.js').resolve()
        testcase.add_from_file(helpersJSPath, file_name="helpers.js")
        for filepath in EXTERNAL_JS_FILE_PATHS:
            filename = os.path.basename(filepath)
            testcase.add_from_file(filepath, file_name=filename)

        # add to testcase as entry point
        testcase.add_from_data(self.fuzz["test"], testcase.landing_page)

    def on_served(self, _test, _served):

        if self.fuzz["mode"] == Mode.FUZZ:
            if self.fuzz["found"]:
                # enable reduction mode
                self.enterReduceMode()
                # update "best" with latest test
                self.fuzz["best"] = self.fuzz["test"]
            
        # check if a result was detected and switch generation modes
        elif self.fuzz["mode"] == Mode.REDUCE:
            if self.fuzz["found"]:
                self.fuzz["run_subject"] = self.fuzz["proposed_run_subject"]
                self.fuzz["best"] = self.fuzz["test"]

        elif self.fuzz["mode"] == Mode.REPORT:
            assert self.fuzz["best"]
            if not self.fuzz["found"]:
                # bug mysteriously disappeared... return to fuzzing mode
                self.enterFuzzMode()
            if len(self.fuzz["run_subject"].modified_styles.map) == 0:
                # Minify step removed all modified styles, 
                print("Minify step removed all modified styles. False Positive, ignoring.")
                self.enterFuzzMode()
            if self.fuzz["reported"]:
                # return to fuzzing mode
                self.enterFuzzMode()

    def on_timeout(self, _test, _served):
        # browser likely hung, reset everything
        self.enterFuzzMode()
