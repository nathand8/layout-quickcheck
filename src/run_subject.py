from copy import deepcopy
from style_map import StyleMap
from element_tree import ElementTree

class RunSubject:
    html_tree: ElementTree
    # Format: html_tree = {
    #     tag: 'div',
    #     id: '12981283',
    #     children: [html_tree, ...]
    # }

    base_styles: StyleMap
    # Format: base_styles = [{
    #     '1293918237': {'background-color': 'blue', ...}
    # }, ...]

    modified_styles: StyleMap
    # Format: modified_styles = [{
    #     '1293918237': {'background-color': 'blue', ...}
    # }, ...]

    def __init__(self, html_tree: ElementTree, base_styles: StyleMap, modified_styles: StyleMap):
        self.html_tree = html_tree
        self.base_styles = base_styles
        self.modified_styles = modified_styles

    def deepcopy(self):
        return RunSubject(
            deepcopy(self.html_tree),
            deepcopy(self.base_styles),
            deepcopy(self.modified_styles)
        )
    
    def removeElementById(self, id):
        self.html_tree.removeElementById(id)
        self.base_styles.removeById(id)
        self.modified_styles.removeById(id)
    
    def getElementIds(self):
        return self.html_tree.getElementIds() | self.base_styles.getElementIds() | self.modified_styles.getElementIds()
    
    def renameId(self, old_id, new_id):
        self.html_tree.renameId(old_id, new_id)
        self.base_styles.renameId(old_id, new_id)
        self.modified_styles.renameId(old_id, new_id)
