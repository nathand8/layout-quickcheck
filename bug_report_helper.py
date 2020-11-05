import json


def all_style_names(*style_dicts):
    for d in style_dicts:
        for _element_id, styles in d.items():
            for style_name in styles:
                yield style_name


def save_bug_report(
    bug_report_path,
    test_file_path,
    formatted_timestamp,
    body,
    minified_base,
    minified_modified,
    postfix,
    differences,
):
    minified_base_file = f"test-file-{formatted_timestamp}{postfix}.html"
    minified_modified_file = f"test-file-{formatted_timestamp}{postfix}-modified.html"
    bug_report_file = f"bug-helper-{formatted_timestamp}.js"
    styles_used = list(set(all_style_names(minified_base, minified_modified)))
    styles_used.sort()
    styles_used_string = ",".join(styles_used)

    with open(f"{bug_report_path}/{bug_report_file}", "w") as f:
        f.write(f"// minified file {test_file_path}/{minified_base_file} \n")
        f.write(
            f"// minified modified file {test_file_path}/{minified_modified_file} \n"
        )
        f.write(
            """
Object.entries(styleLog).forEach(([id, styles]) => {
  const element = document.getElementById(id);
  Object.entries(styles).forEach(([styleName, styleValue]) => {
    element.style[styleName] = styleValue;
  });
});

Object.entries(styleLog).forEach(([id, styles]) => {
  const element = window.frames[0].document.getElementById(id);
  if (element) {
    Object.entries(styles).forEach(([styleName, styleValue]) => {
      element.style[styleName] = styleValue;
    });
  }
});
"""
        )
        f.write(f"const differences = {json.dumps(differences)}\n")
        f.write(f"const baseLog = {json.dumps(minified_base)}\n")
        f.write(f"const styleLog = {json.dumps(minified_modified)}\n")
        f.write(f"const stylesUsed = {json.dumps(styles_used)}\n")
        f.write(f'const stylesUsedString = "{styles_used_string}"\n')
