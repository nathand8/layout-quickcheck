def parse_servo_json(servo_json):
    root = servo_json

    def recurse(element, parent_x, parent_x_margin, parent_y):
        data = element['data']['block_flow'] \
            if element['class'] == 'Flex' \
            else element['data']
        position = data['base']['position']
        border_box = data['fragment']['border_box']
        x = (position['start']['i'] / 60) + (border_box['start']['i'] /
                                             60) + parent_x - parent_x_margin
        y = (position['start']['b'] / 60) + (border_box['start']['b'] /
                                             60) + parent_y
        margin_x = (data['fragment']['margin']['inline_start'] / 60)
        values = {
            'x': x,
            'y': y,
            'width': border_box['size']['inline'] / 60,
            'height': border_box['size']['block'] / 60
        }

        values['children'] = list(
            map(lambda child: recurse(child, x, margin_x, y), data['base']['children']))

        return values

    return recurse(root['children'][0], 0, 0, 0)
