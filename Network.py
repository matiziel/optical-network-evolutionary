from Graph import Graph
from Demand import Demand
from DeserializeXml import Deserializer

class Network:
    def __init__(self):
        data = Deserializer()
        self.graph = Graph(data)
        self.demands = data.getDemands()
    
    def print(self):
        print(self.graph.vertices)
        print(self.graph.edges)
        print()
        for child in self.demands:
            print(child)

network = Network()
network.print()