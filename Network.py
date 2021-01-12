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
        for demand in self.demands:
            print(demand)
    
    def getDemandNum(self):
        return len(self.demands)

    def getMaxDemand(self):
        max = 0
        for demand in self.demands:
            if demand.value > max:
                max = demand.value
        return max + 1