from Graph import Graph
from Flow import Flow
from Demand import Demand
from DeserializeXml import Deserializer

class Network:
    def __init__(self):
        data = Deserializer()
        self.graph = Graph(data.getCities(), data.getLinks())
        self.demands = data.getDemands()
        self.flow = Flow(data.getFlowEdges())
        self.cards = [(10,2),(40,5),(100,9)]
    
    def print(self):
        print(self.graph.vertices)
        print(self.graph.edges)
        print()
        for demand in self.demands:
            print(demand)
    
    def getCardNum(self):
        return len(self.cards)

    def getDemandNum(self):
        return len(self.demands)

network = Network()