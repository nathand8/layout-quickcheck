class ElementTree():
    tree = {}

    def __init__(self, tree):
        self.tree = tree

    def _removeElementInTreeById(self, id, node_list):
        for node in node_list:
            if "id" in node and node["id"] == id:
                node_list.remove(node)
                return
            else:
                self._removeElementInTreeById(id, node.get('children', []))

    def removeElementById(self, id):
        self._removeElementInTreeById(id, self.tree)