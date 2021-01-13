class Demand:
    def __init__(self,link, value, paths):
        self.link = link
        self.value = value
        self.paths = paths
    
    def getPaths(self):
        return self.paths