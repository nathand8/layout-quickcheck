import json


def save_bug_report(
    bug_report_path,
    test_file_path,
    formatted_timestamp,
    body,
    minified_base,
    minified_modified,
    postfix,
):
    minified_base_file = f"test-file-{formatted_timestamp}{postfix}.html"
    minified_modified_file = f"test-file-{formatted_timestamp}{postfix}-modified.html"
    bug_report_file = f"bug-helper-{formatted_timestamp}.js"

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
        f.write(f"const styleLog = {json.dumps(minified_modified)}")
