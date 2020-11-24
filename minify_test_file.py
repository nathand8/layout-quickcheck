from layout_tester import test_combination
from copy import deepcopy


def elements(tree):
    for element in tree:
        yield element
        yield from elements(element["children"])


def styles(s):
    for style_name, style_value in s.items():
        yield style_name, style_value


def remove_element(tree, element_id):
    for element in tree:
        element["children"] = remove_element(element["children"], element_id)
    return list(filter(lambda element: element["id"] != element_id, tree))


def minify(chrome_webdriver, test_timestamp, body, base_style_log, modified_style_log):
    minified_base_log = deepcopy(base_style_log)
    minified_modified_log = deepcopy(modified_style_log)
    iteration = 0

    # Minify modified log
    for element in elements(body):
        element_id = element["id"]

        proposed_modified = deepcopy(minified_modified_log)
        del proposed_modified[element_id]

        is_success, *_ = test_combination(
            chrome_webdriver,
            test_timestamp,
            f"-minified-{iteration}",
            body,
            minified_base_log,
            proposed_modified,
        )
        iteration += 1

        if not is_success:
            minified_modified_log = proposed_modified
        else:
            for style_name, style_value in styles(minified_modified_log[element_id]):
                proposed_modified = deepcopy(minified_modified_log)
                del proposed_modified[element_id][style_name]

                is_success, *_ = test_combination(
                    chrome_webdriver,
                    test_timestamp,
                    f"-minified-{iteration}",
                    body,
                    minified_base_log,
                    proposed_modified,
                )
                iteration += 1

                if not is_success:
                    minified_modified_log = proposed_modified

    # Minify base log
    for element in elements(body):
        element_id = element["id"]

        proposed_base = deepcopy(minified_base_log)
        del proposed_base[element_id]

        is_success, *_ = test_combination(
            chrome_webdriver,
            test_timestamp,
            f"-minified-{iteration}",
            body,
            proposed_base,
            minified_modified_log,
        )
        iteration += 1

        if not is_success:
            minified_base_log = proposed_base
        else:
            for style_name, style_value in styles(minified_base_log[element_id]):
                proposed_base = deepcopy(minified_base_log)
                del proposed_base[element_id][style_name]

                is_success, *_ = test_combination(
                    chrome_webdriver,
                    test_timestamp,
                    f"-minified-{iteration}",
                    body,
                    proposed_base,
                    minified_modified_log,
                )
                iteration += 1

                if not is_success:
                    minified_base_log = proposed_base

    # Remove unnecessary elements
    minified_body = deepcopy(body)
    for element in elements(body):
        element_id = element["id"]

        if (
            len(minified_base_log.get(element_id, {})) + len(minified_modified_log.get(element_id, {}))
            <= 0
        ):
            proposed_body = deepcopy(minified_body)
            proposed_body = remove_element(proposed_body, element_id)

            is_success, *_ = test_combination(
                chrome_webdriver,
                test_timestamp,
                f"-minified-{iteration}",
                proposed_body,
                minified_base_log,
                minified_modified_log,
            )
            iteration += 1

            if not is_success:
                minified_body = proposed_body

    # Create final representations of minified files
    is_success, minified_differences, _ = test_combination(
        chrome_webdriver,
        test_timestamp,
        f"-minified-{iteration}",
        minified_body,
        minified_base_log,
        minified_modified_log,
    )

    return (
        minified_body,
        minified_base_log,
        minified_modified_log,
        f"-minified-{iteration}",
        minified_differences,
    )
