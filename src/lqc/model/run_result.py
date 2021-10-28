from lqc.model.constants import BugType
from lqc.model.dimensions_conflict import DimensionsConflict


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

    def __init__(self, dimensions_conflict: DimensionsConflict):
        super().__init__(BugType.LAYOUT)
        self.dimensions_conflict = dimensions_conflict

    def isBug(self):
        return True
    

