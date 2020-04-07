def compare_layout(layout_a, layout_b):
    differences = {}

    for key in layout_a:
        if isinstance(layout_a[key], list):
            if len(layout_a[key]) != len(layout_b[key]):
                differences[key] = f'children list length different: {len(layout_a[key])} vs {len(layout_b[key])}'
            else:
                diff_list = []
                for a, b, i in zip(layout_a[key], layout_b[key], range(len(layout_a[key]))):
                    key_diff = compare_layout(a, b)
                    if key_diff is not None:
                        diff_list.append({
                            'index': i,
                            'diff': key_diff
                        })
                if len(diff_list) > 0:
                    differences[key] = diff_list
        else:
            if layout_a[key] != layout_b[key]:
                differences[key] = {
                    'value_a': layout_a[key],
                    'value_b': layout_b[key]
                }
    return differences if differences != {} else None
