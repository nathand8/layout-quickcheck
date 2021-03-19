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
    
    def _getElementIdsInTree(self, node_list):
        s = set()
        for node in node_list:
            if "id" in node:
                s.add(node["id"])
                if "children" in node:
                    s |= self._getElementIdsInTree(node["children"])
        return s
    
    def getElementIds(self):
        return self._getElementIdsInTree(self.tree)
    
    def _renameIdInTree(self, old_id, new_id, node_list):
        for node in node_list:
            if "id" in node and node["id"] == old_id:
                node["id"] = new_id
            if "children" in node:
                self._renameIdInTree(old_id, new_id, node["children"])
    
    def renameId(self, old_id, new_id):
        self._renameIdInTree(old_id, new_id, self.tree)
        
