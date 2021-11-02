from lqc.model.constants import BugType


class RunResult:
    type: BugType

    def __init__(self, type: BugType):
        self.type = type

    def isBug(self) -> bool:
        raise NotImplemented("RunResult().isBug() should be overridden")

class RunResultPass(RunResult):

    def __init__(self):
        super().__init__(None)

    def isBug(self):
        return False


class RunResultCrash(RunResult):

    def __init__(self):
        super().__init__(BugType.PAGE_CRASH)

    def isBug(self):
        return True


class RunResultLayoutBug(RunResult):
    """
    The resulting dimensions from a test run that has a layout bug.

    element_dimensions format is provided by JS:
    [{
        'id': 'one',
        'tag': 'div',
        'id_tag': 'one<div>',
        'differing_dims': ['bottom', 'height'],
        'post_modify_dims': {'bottom': 10, 'height': 5},
        'post_reload_dims': {'bottom': 20, 'height': 15},
    }, ...]

    """

    def __init__(self, element_dimensions):
        super().__init__(BugType.LAYOUT)
        self.element_dimensions = element_dimensions

    def isBug(self):
        return True

    def getDimensionsAsJSString(self):
        """
        Returns a JS String that will measure all the elements and dimensions
        that were conflicting.

        Example Output:
        'console.log();'
        """
        pass
    

