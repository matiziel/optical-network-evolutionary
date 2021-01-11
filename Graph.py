from DeserializeXml import Deserializer

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.data = Deserializer()

    def loadVertices(self):
        self.vertices = data.getVertices() 
