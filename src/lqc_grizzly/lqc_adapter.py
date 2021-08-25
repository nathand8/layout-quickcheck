# Initial structure pulled from
# https://github.com/MozillaSecurity/grizzly/blob/feedback-example/grizzly/adapter/feedback_example/__init__.py

from enum import Enum, unique
from random import randint
from string import Template
from lqc.config.config import Config, parse_config
from lqc.generate.style_log_generator import generate_run_subject
from lqc.generate.web_page.create import html_string, JsVersion

from grizzly.adapter import Adapter

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


class LayoutQuickCheckAdapter(Adapter):
    """LayoutQuickCheckAdapter"""

    NAME = "LayoutQuickCheck-Adapter"

    def setup(self, _input, server_map):
        # indicates if a result was found
        self.fuzz["found"] = False
        # track most recent version of test (for reduction)
        self.fuzz["best"] = None
        # current operation mode
        self.fuzz["mode"] = Mode.FUZZ
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

    def generate(self, testcase, _server_map):
        self.fuzz["found"] = False
        if self.fuzz["mode"] == Mode.REDUCE:
            # are we done reduction?
            if randint(0, 10) == 5:
                # let's say we are done
                self.fuzz["mode"] = Mode.REPORT
            else:
                # generate next reduced version to test
                pass

        if self.fuzz["mode"] == Mode.REPORT:
            # here we should force crash the browser so grizzly detects a result
            # see bug https://bugzilla.mozilla.org/show_bug.cgi?id=1725008
            # jslib = "function finish_test() { FuzzingFunctions.moz_crash(sig) }\n"
            # but for now...
            jslib = "function finish_test() { setTimeout(window.close, 10) }\n"
        else:
            jslib = "function finish_test() { setTimeout(window.close, 10) }\n"
        # add a non required file
        testcase.add_from_data(jslib, "helpers.js", required=False)

        # generate a test
        if self.fuzz["mode"] == Mode.REDUCE:
            self.fuzz["test"] = external_reduce(self.fuzz["test"])


        # stepsFactory = MinifyStepFactory()
        # while True:
        #     proposed_run_subject = stepsFactory.next_minimization_step(run_subject)
        #     if proposed_run_subject == None:
        #         break
            
        #     bug_gone, *_ = test_combination(target_browser.getDriver(), proposed_run_subject)
        #     if not bug_gone:
        #         run_subject = proposed_run_subject

        elif self.fuzz["mode"] == Mode.REPORT:
            # report "best"
            self.fuzz["test"] = self.fuzz["best"]
        else:
            run_subject = generate_run_subject()
            self.fuzz["run_subject"] = run_subject
            # html_string will generate a complete web page with html and inline js
            self.fuzz["test"] = html_string(run_subject, js_version=JsVersion.GRIZZLY)

        # add to testcase as entry point
        testcase.add_from_data(self.fuzz["test"], testcase.landing_page)

    def on_served(self, _test, _served):
        # check if a result was detected and switch generation modes
        if self.fuzz["mode"] == Mode.REPORT:
            assert self.fuzz["best"]
            # return to fuzzing mode
            self.fuzz["mode"] = Mode.FUZZ
            self.fuzz["best"] = None
        elif self.fuzz["found"]:
            # enable reduction mode
            if self.fuzz["mode"] == Mode.FUZZ:
                self.fuzz["mode"] = Mode.REDUCE
            # update "best" with latest test
            self.fuzz["best"] = self.fuzz["test"]

    def on_timeout(self, _test, _served):
        # browser likely hung, reset everything
        self.fuzz["best"] = None
        self.fuzz["mode"] = Mode.FUZZ


TEST_TEMPLATE = Template(
    """<!DOCTYPE html>
<html>
<head>
<script src="helpers.js"></script>
<script>
document.addEventListener("DOMContentLoaded", async () => {
  if ($randint === 0) {
    // pretend we found a result
    await fetch("/found")
  }
  finish_test()
})
</script>
</head>
<body><h1>RUNNING</h1></body>
</html>
"""
)


def external_generate():
    test_data = TEST_TEMPLATE.safe_substitute(randint=randint(0, 20))
    return test_data


def external_reduce(testcase):
    return testcase.replace("RUNNING", "REDUCING")