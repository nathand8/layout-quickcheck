from enum import Enum, unique


@unique
class BugType(Enum):
    LAYOUT = "Layout Under Invalidation" # Also known as "Under-Invalidation Bugs"
    PAGE_CRASH = "Page Crash"