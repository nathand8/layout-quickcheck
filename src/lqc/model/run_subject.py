from copy import deepcopy

from lqc.model.element_tree import ElementTree
from lqc.model.style_map import StyleMap

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
    
    def all_style_names(self):
        return self.base_styles.all_style_names().union(self.modified_styles.all_style_names())

    def styles_signature(self):
        """ Return 'display' styles and modified styles """
        styles = set()
        display_styles = [x for x in self.base_styles.all_style_names() if ":" in x]
        styles = styles.union(display_styles)
        modified_styles = self.modified_styles.all_style_names()
        styles = styles.union(modified_styles)

        # Sort the styles
        styles = list(styles)
        styles.sort()
        styles = ",".join(styles)

        # Simplify the style names in the signature
        styles = styles.replace('block-start', 'block').replace('block-end', 'block')
        styles = styles.replace('inline-start', 'inline').replace('inline-end', 'inline')
        return styles
