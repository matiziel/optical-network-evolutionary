class Demand:
    def __init__(self,link, value, paths):
        self.link = link
        self.value = value
        self.paths = paths
    def __str__(self):
        return str(self.link) + "\n" + str(self.value) + "\n" + str(self.paths)
