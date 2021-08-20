class StyleMap():
    map = {}

    def __init__(self, map):
        self.map = map
        pass
    
    def removeById(self, id):
        del self.map[id]
    
    def getElementIds(self):
        return set(self.map.keys())
    
    def renameId(self, old_id, new_id):
        if old_id in self.map:
            self.map[new_id] = self.map[old_id]
            del self.map[old_id]
    
    def toJS(self):
        """
        Create a string that will make style changes in javascript

        Example Output: 

            var abeofmwlekrifj = document.getElementById("abeofmwlekrifj");
            if (abeofmwlekrifj) {
                abeofmwlekrifj.style["min-width"] = "200px";
                abeofmwlekrifj.style["margin-left"] = "10em";
            }

            var zomelfjeiwle = document.getElementById("zomelfjeiwle");
            if (zomelfjeiwle) {
                zomelfjeiwle.style["background-color"] = "blue";
            }
            
        """
        ret_string = ""
        for (elementId, styles) in self.map.items():

            elementStyles = list(styles.items())
            elementStyles.sort() # Sort alphabetical order by style name (to enforce the same order every time)

            if elementStyles:
                ret_string += f'var {elementId} = document.getElementById("{elementId}");\n'
                ret_string += 'if (' + elementId + ') {\n'

                for (style_name, style_value) in elementStyles:
                    ret_string += f'  {elementId}.style["{style_name}"] = "{style_value}";\n'
                
                ret_string += '}\n'

        return ret_string