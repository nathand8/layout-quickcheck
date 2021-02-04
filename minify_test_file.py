from layout_tester import test_combination
from css_generators.length import matches_length_pattern
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


def Minify_RemoveEachElement(test_subject):

    for element in elements(test_subject.html_tree):

        def removeElement(proposed_test_subject):
            proposed_test_subject.removeElementById(element['id'])
            return proposed_test_subject

        yield removeElement


def Minify_RemoveAllStylesForEachElement(test_subject):

    # Generate a function (for each id) to remove styles by id from base_styles.map
    for elementId, _ in test_subject.base_styles.map.items():

        def removeStyle(proposed_test_subject):
            if elementId in proposed_test_subject.base_styles.map:
                del proposed_test_subject.base_styles.map[elementId]
            return proposed_test_subject

        yield removeStyle

    # Generate a function (for each id) to remove styles by id from modified_styles.map
    for elementId, _ in test_subject.modified_styles.map.items():

        def removeStyle(proposed_test_subject):
            if elementId in proposed_test_subject.modified_styles.map:
                del proposed_test_subject.modified_styles.map[elementId]
            return proposed_test_subject

        yield removeStyle


def Minify_RemoveEachStyleForEachElement(test_subject):

    # Generate a function for each style - to remove that style from base_styles.map
    for elementId, styles in test_subject.base_styles.map.items():
        for style_name, _ in styles.items():

            def removeStyle(proposed_test_subject):
                if elementId in proposed_test_subject.base_styles.map and style_name in proposed_test_subject.base_styles.map[elementId]:
                    del proposed_test_subject.base_styles.map[elementId][style_name]
                return proposed_test_subject

            yield removeStyle

    # Generate a function for each style - to remove that style from modified_styles.map
    for elementId, styles in test_subject.modified_styles.map.items():
        for style_name, _ in styles.items():

            def removeStyle(proposed_test_subject):
                if elementId in proposed_test_subject.modified_styles.map and style_name in proposed_test_subject.modified_styles.map[elementId]:
                    del proposed_test_subject.modified_styles.map[elementId][style_name]
                return proposed_test_subject

            yield removeStyle


# Try simplifying css lengths (e.g "-1496vh" or "+1240vmin") to "-20px" or "20px"
def Minify_SimplifyLengthStyles(test_subject):

    # Generate a function for each style that is a length - change to a simple length
    for elementId, styles in test_subject.base_styles.map.items():
        for style_name, style_value in styles.items():
            if matches_length_pattern(style_value):

                def removeStyle(proposed_test_subject):
                    if style_value.startswith("-"):
                        proposed_test_subject.base_styles.map[elementId][style_name] = "-20px"
                    else:
                        proposed_test_subject.base_styles.map[elementId][style_name] = "20px"
                    return proposed_test_subject

                yield removeStyle

    # Generate a function for each style that is a length - change to a simple length
    for elementId, styles in test_subject.modified_styles.map.items():
        for style_name, style_value in styles.items():
            if matches_length_pattern(style_value):

                def removeStyle(proposed_test_subject):
                    if style_value.startswith("-"):
                        proposed_test_subject.modified_styles.map[elementId][style_name] = "-20px"
                    else:
                        proposed_test_subject.modified_styles.map[elementId][style_name] = "20px"
                    return proposed_test_subject

                yield removeStyle


def Enhance_MinHeightWidthPerElement(test_subject):

    # Generate a function for each element that gives it a min width
    # (and another function for min height)
    for element in elements(test_subject.html_tree):
        elementId = element['id']

        def giveMinSize(proposed_test_subject):
            if elementId in proposed_test_subject.base_styles.map:
                proposed_test_subject.base_styles.map[elementId]['min-width'] = "50px"
                proposed_test_subject.base_styles.map[elementId]['min-height'] = "50px"
            else:
                proposed_test_subject.base_styles.map[elementId] = {
                    'min-width': "50px",
                    'min-height': "50px"
                }
            return proposed_test_subject

        yield giveMinSize
        

def Enhance_BackgroundColorPerElement(test_subject):

    BACKGROUND_COLORS = ['black', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

    # Generate a function for each element that gives it a background-color
    for element in elements(test_subject.html_tree):
        elementId = element['id']
        background_color = random.choice(BACKGROUND_COLORS)

        def giveMinSize(proposed_test_subject):
            if elementId in proposed_test_subject.base_styles.map:
                proposed_test_subject.base_styles.map[elementId]['background-color'] = background_color
            else:
                proposed_test_subject.base_styles.map[elementId] = {'background-color': background_color}
            return proposed_test_subject

        yield giveMinSize


def minify(test_config, test_subject):

    def run_manipulations(iteration, test_subject, manipulations_generator):
        for manipulation in manipulations_generator:
            proposed_test_subject = manipulation(test_subject.deepcopy())
            
            bug_gone, *_ = test_combination(test_config, proposed_test_subject)
            iteration += 1
            if not bug_gone:
                test_subject = proposed_test_subject
        return (iteration, test_subject)

    iteration = 1
    (iteration, test_subject) = run_manipulations(iteration, test_subject, Minify_RemoveEachElement(test_subject))
    (iteration, test_subject) = run_manipulations(iteration, test_subject, Minify_RemoveAllStylesForEachElement(test_subject))
    (iteration, test_subject) = run_manipulations(iteration, test_subject, Minify_RemoveEachStyleForEachElement(test_subject))
    (iteration, test_subject) = run_manipulations(iteration, test_subject, Minify_SimplifyLengthStyles(test_subject))
    (iteration, test_subject) = run_manipulations(iteration, test_subject, Enhance_MinHeightWidthPerElement(test_subject))
    (iteration, test_subject) = run_manipulations(iteration, test_subject, Enhance_BackgroundColorPerElement(test_subject))
    
    # Create final representations of minified files
    _, minified_differences, _ = test_combination(test_config, test_subject)
    return (test_subject, minified_differences)
