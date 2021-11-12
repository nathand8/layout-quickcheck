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
    
    def _simplify_style_signature(self, style_name):
        """Replace pieces of the style name to consolidate similar style signatures"""
        style_name = style_name.replace('block-start', '[block]')
        style_name = style_name.replace('block-end', '[block]')
        style_name = style_name.replace('inline-start', '[inline]')
        style_name = style_name.replace('inline-end', '[inline]')
        style_name = style_name.replace('block-size', '[height]')
        style_name = style_name.replace('inline-size', '[width]')
        style_name = style_name.replace('left', '[inline]')
        style_name = style_name.replace('right', '[inline]')
        style_name = style_name.replace('top', '[block]')
        style_name = style_name.replace('bottom', '[block]')
        return style_name


    def styles_signature(self):
        """ Return 'display' style values and modified styles """
        styles = set()
        display_styles = [x for x in self.base_styles.all_style_names() if ":" in x]
        styles = styles.union(display_styles)
        modified_styles = self.modified_styles.all_style_names()
        styles = styles.union(modified_styles)

        # Simplify the style names in the signature
        styles = set([self._simplify_style_signature(x) for x in styles])

        # Sort the styles
        styles = list(styles)
        styles.sort()
        styles = ",".join(styles)

        return styles
