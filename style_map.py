class StyleMap():
    map = {}

    def __init__(self, map):
        self.map = map
        pass
    
    def removeById(self, id):
        del self.map[id]
    
    def toJS(self):
        """
        Create a string that will make style changes in javascript

        Example Output: 

            document.getElementById("912A37J38G").style["min-width"] = "200px";
            document.getElementById("912A37J38G").style["margin-left"] = "10em";
            document.getElementById("PTN873OUW").style["background-color"] = "blue";
            
        """
        ret_string = ""
        for (elementId, styles) in self.map.items():

            elementStyles = list(styles.items())
            elementStyles.sort() # Sort alphabetical order by style name (to enforce the same order every time)

            for (style_name, style_value) in elementStyles:
                ret_string += f'document.getElementById("{elementId}").style["{style_name}"] = "{style_value}";\n'

        return ret_string