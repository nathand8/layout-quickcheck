class StyleMap():
    map = {}

    def __init__(self, map):
        self.map = map
        pass
    
    def removeById(self, id):
        del self.map[id]