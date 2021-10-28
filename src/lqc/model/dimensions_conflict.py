class DimensionsConflict:
    """
    The resulting dimensions from a test run that has a layout bug.

    dimension_results format is provided by JS:

    """

    def __init__(self, dimension_results):
        self.raw = dimension_results

    def outputAsJS(self):
        pass