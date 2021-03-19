import re

# From https://stackoverflow.com/questions/57174866/preserving-indentation-in-a-triple-quoted-fstring
def indent(indent, inner_str):
    return inner_str.replace('\n', '\n' + indent)

def formatWithIndent(s, *args, **kwargs):
    """ Takes a multiline string and preserves the indent when calling format on it """
    pattern = r'(\s*){(.*)}'
    key_indents = {}
    for l in s.split("\n"):
        match = re.search(pattern, l)
        if match:
            key_indents[match.group(2)] = match.group(1)

    for kw, val in kwargs.items():
        if kw in key_indents:
            kwargs[kw] = indent(key_indents[kw], val)

    return s.format(**kwargs)
