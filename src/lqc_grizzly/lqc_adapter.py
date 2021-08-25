# Initial structure pulled from
# https://github.com/MozillaSecurity/grizzly/blob/feedback-example/grizzly/adapter/feedback_example/__init__.py

from enum import Enum, unique
from random import randint
from string import Template
from lqc.config.config import Config, parse_config
from lqc.generate.style_log_generator import generate_run_subject
from lqc.generate.web_page.create import html_string, JsVersion

from grizzly.adapter import Adapter
from lqc.minify.minify_test_file import MinifyStepFactory
from lqc.model.run_subject import RunSubject

__author__ = "Tyson Smith"
__credits__ = ["Tyson Smith", "Nathan Davis"]


@unique
class Mode(Enum):
    # normal fuzzing operation, generate test cases
    FUZZ = 0
    # reduce mode, apply reduction operations to a single test
    REDUCE = 1
    # no more reductions can be performed indicate we are complete
    REPORT = 2

def getSignature(run_subject: RunSubject):
    styles_used = list(run_subject.all_style_names())
    styles_used.sort()
    return ",".join(styles_used)

class LayoutQuickCheckAdapter(Adapter):
    """LayoutQuickCheckAdapter"""

    NAME = "LayoutQuickCheck-Adapter"

    def setup(self, _input, server_map):
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
        # TODO: Do we need to load different config files?
        config = parse_config("./config/preset-firefox.config.json")
        Config(config)

    def _found(self):
        # callback attached to '/found'
        self.fuzz["found"] = True
        return b""

    def enterFuzzMode(self):
        """Fuzz mode generates random tests"""
        self.fuzz["mode"] = Mode.FUZZ
        self.fuzz["found"] = False
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
            jslib = "function finish_test() { setTimeout(window.close, 10) }\n"
            # html_string will generate a complete web page with html and inline js
            self.fuzz["test"] = html_string(self.fuzz["run_subject"], js_version=JsVersion.GRIZZLY)

        elif self.fuzz["mode"] == Mode.REDUCE:

            # Run one minify step from MinifyStepFactory
            self.fuzz["proposed_run_subject"] = self.fuzz["minifyStepsFactory"].next_minimization_step(self.fuzz["run_subject"])
            # are we done reduction?
            if self.fuzz["proposed_run_subject"] == None:
                self.enterReportMode()
                # html_string will generate a complete web page with html and inline js
                self.fuzz["test"] = html_string(self.fuzz["run_subject"], js_version=JsVersion.GRIZZLY)
            else:
                # html_string will generate a complete web page with html and inline js
                self.fuzz["test"] = html_string(self.fuzz["proposed_run_subject"], js_version=JsVersion.GRIZZLY)
            jslib = "function finish_test() { setTimeout(window.close, 10) }\n"

        elif self.fuzz["mode"] == Mode.REPORT:
            # here we should force crash the browser so grizzly detects a result
            # see bug https://bugzilla.mozilla.org/show_bug.cgi?id=1725008
            sig = getSignature(self.fuzz["run_subject"])
            jslib = "function finish_test() { FuzzingFunctions.crash('" + sig + "') }\n"
            self.fuzz["test"] = self.fuzz["best"]
            self.fuzz["reported"] = True

        # Reset the "found" flag
        self.fuzz["found"] = False

        # add a non required file
        testcase.add_from_data(jslib, "helpers.js", required=False)

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
            if self.fuzz["reported"]:
                # return to fuzzing mode
                self.enterFuzzMode()

    def on_timeout(self, _test, _served):
        # browser likely hung, reset everything
        self.enterFuzzMode()
