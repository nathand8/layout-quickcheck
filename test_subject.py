from copy import deepcopy

class TestSubject:
    html_tree = {}
    # Format: html_tree = {
    #     tag: 'div',
    #     id: '12981283',
    #     children: [html_tree, ...]
    # }

    base_styles = {}
    # Format: base_styles = [{
    #     '1293918237': {'background-color': 'blue', ...}
    # }, ...]

    modified_styles = {}
    # Format: modified_styles = [{
    #     '1293918237': {'background-color': 'blue', ...}
    # }, ...]

    def __init__(self, html_tree, base_styles, modified_styles):
        self.html_tree = html_tree
        self.base_styles = base_styles
        self.modified_styles = modified_styles

    def deepcopy(self):
        return TestSubject(
            deepcopy(self.html_tree),
            deepcopy(self.base_styles),
            deepcopy(self.modified_styles)
        )

    def _removeElementInTreeById(self, id, node_list):
        for node in node_list:
            if "id" in node and node["id"] == id:
                node_list.remove(node)
                return
            else:
                self._removeElementInTreeById(id, node.get('children', []))
    
    def removeElementById(self, id):
        self._removeElementInTreeById(id, self.html_tree)
        if id in self.base_styles:
            del self.base_styles[id]
        if id in self.modified_styles:
            del self.modified_styles[id]
