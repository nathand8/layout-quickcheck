from webdrivers.target_browser import TargetBrowser
from layout_tester import test_combination
from css_generators.util.length import matches_length_pattern
from copy import deepcopy
import random


def elements(tree):
    for element in tree:
        if element["tag"] != "<text>":
            yield element
            yield from elements(element["children"])


def styles(s):
    for style_name, style_value in s.items():
        yield style_name, style_value


def remove_element(tree, element_id):
    for element in tree:
        element["children"] = remove_element(element["children"], element_id)
    return list(
        filter(
            lambda element: element["tag"] == "<text>" or element["id"] != element_id,
            tree,
        )
    )


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


def minify(target_browser: TargetBrowser, run_subject):

    def run_manipulations(iteration, run_subject, manipulations_generator):
        for manipulation in manipulations_generator:
            proposed_run_subject = manipulation(run_subject.deepcopy())
            
            bug_gone, *_ = test_combination(target_browser.getDriver(), proposed_run_subject)
            iteration += 1
            if not bug_gone:
                run_subject = proposed_run_subject
        return (iteration, run_subject)

    iteration = 1
    (iteration, run_subject) = run_manipulations(iteration, run_subject, Minify_RemoveEachElement(run_subject))
    (iteration, run_subject) = run_manipulations(iteration, run_subject, Minify_RemoveAllStylesForEachElement(run_subject))
    (iteration, run_subject) = run_manipulations(iteration, run_subject, Minify_RemoveEachStyleForEachElement(run_subject))
    (iteration, run_subject) = run_manipulations(iteration, run_subject, Minify_SimplifyLengthStyles(run_subject))
    (iteration, run_subject) = run_manipulations(iteration, run_subject, Enhance_MinHeightWidthPerElement(run_subject))
    (iteration, run_subject) = run_manipulations(iteration, run_subject, Enhance_BackgroundColorPerElement(run_subject))
    
    # Create final representations of minified files
    _, minified_differences, _ = test_combination(target_browser.getDriver(), run_subject)
    return (run_subject, minified_differences)
