from layout_tester import test_combination


def elements(tree):
    for element in tree:
        yield element
        yield from elements(element["children"])


def styles(s):
    for style_name, style_value in s.items():
        yield style_name, style_value


def minify(chrome_webdriver, test_timestamp, body, base_style_log, modified_style_log):
    minified_base_log = base_style_log.copy()
    minified_modified_log = modified_style_log.copy()
    iteration = 0

    # Minify modified log
    for element in elements(body):
        element_id = element["id"]

        control_success, *_ = test_combination(
            chrome_webdriver,
            test_timestamp,
            f"-minified-{iteration}",
            body,
            minified_base_log,
            minified_modified_log,
        )
        iteration += 1

        proposed_modified = minified_modified_log.copy()
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

        if control_success == is_success:
            minified_modified_log = proposed_modified
        else:
            styles_that_matter = {}
            for style_name, style_value in styles(minified_modified_log[element_id]):
                proposed_modified = minified_modified_log.copy()
                element_style_list = {style_name: style_value}
                proposed_modified[element_id] = element_style_list

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
                    styles_that_matter[style_name] = style_value
            if len(styles_that_matter) > 0:
                minified_modified_log[element_id] = styles_that_matter

    print("base after step 1")
    print(minified_base_log)

    print("modified after step 1")
    print(minified_modified_log)

    # Minify base log
    for element in elements(body):
        element_id = element["id"]

        control_success, *_ = test_combination(
            chrome_webdriver,
            test_timestamp,
            f"-minified-{iteration}",
            body,
            minified_base_log,
            minified_modified_log,
        )
        iteration += 1

        proposed_base = minified_base_log.copy()
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

        if control_success == is_success:
            minified_base_log = proposed_base
        else:
            styles_that_matter = {}
            for style_name, style_value in styles(minified_base_log[element_id]):
                proposed_base = minified_base_log.copy()
                element_style_list = {style_name: style_value}
                proposed_base[element_id] = element_style_list

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
                    styles_that_matter[style_name] = style_value
            if len(styles_that_matter) > 0:
                minified_base_log[element_id] = styles_that_matter

    print("base after step 2")
    print(minified_base_log)

    print("modified after step 2")
    print(minified_modified_log)

    # Create final representations of minified files
    is_success, *_ = test_combination(
        chrome_webdriver,
        test_timestamp,
        f"-minified-{iteration}",
        body,
        minified_base_log,
        minified_modified_log,
    )

    return body, minified_base_log, minified_modified_log, f"-minified-{iteration}"
