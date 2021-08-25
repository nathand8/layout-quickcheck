import random

from lqc.generate.css.util.length import matches_length_pattern
from lqc.model.run_subject import RunSubject
from lqc.selenium_harness.layout_tester import test_combination


def elements(tree):
    for element in tree:
        if element["tag"] != "<text>":
            yield element
            yield from elements(element["children"])


def Minify_RemoveEachElement(run_subject):

    for element in elements(run_subject.html_tree.tree):

        def removeElement(proposed_run_subject):
            proposed_run_subject.removeElementById(element['id'])
            return proposed_run_subject

        yield removeElement


def Minify_RemoveAllStylesForEachElement(run_subject):

    # Generate a function (for each id) to remove styles by id from base_styles.map
    for elementId, _ in run_subject.base_styles.map.items():

        def removeStyle(proposed_run_subject):
            if elementId in proposed_run_subject.base_styles.map:
                del proposed_run_subject.base_styles.map[elementId]
            return proposed_run_subject

        yield removeStyle

    # Generate a function (for each id) to remove styles by id from modified_styles.map
    for elementId, _ in run_subject.modified_styles.map.items():

        def removeStyle(proposed_run_subject):
            if elementId in proposed_run_subject.modified_styles.map:
                del proposed_run_subject.modified_styles.map[elementId]
            return proposed_run_subject

        yield removeStyle


def Minify_RemoveEachStyleForEachElement(run_subject):

    # Generate a function for each style - to remove that style from base_styles.map
    for elementId, styles in run_subject.base_styles.map.items():
        for style_name, _ in styles.items():

            def removeStyle(proposed_run_subject):
                if elementId in proposed_run_subject.base_styles.map and style_name in proposed_run_subject.base_styles.map[elementId]:
                    del proposed_run_subject.base_styles.map[elementId][style_name]
                return proposed_run_subject

            yield removeStyle

    # Generate a function for each style - to remove that style from modified_styles.map
    for elementId, styles in run_subject.modified_styles.map.items():
        for style_name, _ in styles.items():

            def removeStyle(proposed_run_subject):
                if elementId in proposed_run_subject.modified_styles.map and style_name in proposed_run_subject.modified_styles.map[elementId]:
                    del proposed_run_subject.modified_styles.map[elementId][style_name]
                return proposed_run_subject

            yield removeStyle


def Minify_MoveStyleChangesToFirstLoad(run_subject):
    """ For each of the modified styles, try moving that style to the base styles.
        This should leave only the absolutely essential styles being modified.
    """

    # Generate a function for each item in modified_styles
    for elementId, styles in run_subject.modified_styles.map.items():
        for style_name, style_value in styles.items():
            
            def moveStyleUpstream(proposed_run_subject):

                # Add style to base styles
                if elementId not in proposed_run_subject.base_styles.map.keys():
                    proposed_run_subject.base_styles.map[elementId] = {}
                proposed_run_subject.base_styles.map[elementId][style_name] = style_value

                # Remove style from modified styles
                del proposed_run_subject.modified_styles.map[elementId][style_name]
                if len(proposed_run_subject.modified_styles.map[elementId]) == 0:
                    del proposed_run_subject.modified_styles.map[elementId] 

                return proposed_run_subject
            
            yield moveStyleUpstream



# Try simplifying css lengths (e.g "-1496vh" or "+1240vmin") to "-20px" or "20px"
def Minify_SimplifyLengthStyles(run_subject):

    # Generate a function for each style that is a length - change to a simple length
    for elementId, styles in run_subject.base_styles.map.items():
        for style_name, style_value in styles.items():
            if matches_length_pattern(style_value):

                def removeStyle(proposed_run_subject):
                    if style_value.startswith("-"):
                        proposed_run_subject.base_styles.map[elementId][style_name] = "-20px"
                    else:
                        proposed_run_subject.base_styles.map[elementId][style_name] = "20px"
                    return proposed_run_subject

                yield removeStyle

    # Generate a function for each style that is a length - change to a simple length
    for elementId, styles in run_subject.modified_styles.map.items():
        for style_name, style_value in styles.items():
            if matches_length_pattern(style_value):

                def removeStyle(proposed_run_subject):
                    if style_value.startswith("-"):
                        proposed_run_subject.modified_styles.map[elementId][style_name] = "-20px"
                    else:
                        proposed_run_subject.modified_styles.map[elementId][style_name] = "20px"
                    return proposed_run_subject

                yield removeStyle


def Enhance_MinHeightWidthPerElement(run_subject):

    # Generate a function for each element that gives it a min width
    # (and another function for min height)
    for element in elements(run_subject.html_tree.tree):
        elementId = element['id']

        def giveMinSize(proposed_run_subject):
            if elementId in proposed_run_subject.base_styles.map:
                proposed_run_subject.base_styles.map[elementId]['min-width'] = "50px"
                proposed_run_subject.base_styles.map[elementId]['min-height'] = "50px"
            else:
                proposed_run_subject.base_styles.map[elementId] = {
                    'min-width': "50px",
                    'min-height': "50px"
                }
            return proposed_run_subject

        yield giveMinSize
        

def Enhance_BackgroundColorPerElement(run_subject):

    BACKGROUND_COLORS = ['black', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

    # Generate a function for each element that gives it a background-color
    for element in elements(run_subject.html_tree.tree):
        elementId = element['id']
        background_color = random.choice(BACKGROUND_COLORS)

        def giveMinSize(proposed_run_subject):
            if elementId in proposed_run_subject.base_styles.map:
                proposed_run_subject.base_styles.map[elementId]['background-color'] = background_color
            else:
                proposed_run_subject.base_styles.map[elementId] = {'background-color': background_color}
            return proposed_run_subject

        yield giveMinSize


def Enhance_ShortenIds(run_subject: RunSubject):

    shortened_ids = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty']

    # Get a set of all the ids in html and css
    original_ids = run_subject.getElementIds()

    def renameIds(proposed_run_subject):
        for original_id, short_id in zip(original_ids, shortened_ids):
            proposed_run_subject.renameId(original_id, short_id)
        return proposed_run_subject
    
    yield renameIds



def minify(target_browser, run_subject):

    stepsFactory = MinifyStepFactory()
    while True:
        proposed_run_subject = stepsFactory.next_minimization_step(run_subject)
        if proposed_run_subject == None:
            break
        
        bug_gone, *_ = test_combination(target_browser.getDriver(), proposed_run_subject)
        if not bug_gone:
            run_subject = proposed_run_subject

    # Create final representations of minified files
    _, minified_differences, _ = test_combination(target_browser.getDriver(), run_subject)
    return (run_subject, minified_differences)


class MinifyStepFactory():

    GENERATORS = [
        Minify_RemoveEachElement,
        Minify_RemoveAllStylesForEachElement,
        Minify_RemoveEachStyleForEachElement,
        Minify_MoveStyleChangesToFirstLoad,
        Minify_SimplifyLengthStyles,
        Enhance_MinHeightWidthPerElement,
        Enhance_BackgroundColorPerElement,
        Enhance_ShortenIds,
    ]

    def __init__(self):
        self.queue = []
        self.current_generator_index = 0
        self.current_generator = None

    def next_minimization_step(self, run_subject):
        manipulation = None
        if self.current_generator == None:
            self.current_generator = self.GENERATORS[self.current_generator_index](run_subject)

        while manipulation == None:
            try:
                manipulation = next(self.current_generator)
            except StopIteration:
                self.current_generator_index += 1
                if self.current_generator_index >= len(self.GENERATORS):
                    return None
                self.current_generator = self.GENERATORS[self.current_generator_index](run_subject)
        
        return manipulation(run_subject.deepcopy())


