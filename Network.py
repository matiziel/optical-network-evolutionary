from Graph import Graph
from Flow import Flow
from Demand import Demand
from DeserializeXml import Deserializer

class Network:
    def __init__(self, filename):
        data = Deserializer(filename)
        self.graph = Graph(data.getCities(), data.getLinks())
        self.demands = data.getDemands()
        self.flow = Flow(data.getFlowEdges())
    
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
        return max
    
    def resetFlow(self):
        self.flow.reset()

    def incrementFlow(self, link, value):
        self.flow.increment(link, value)

    def getDemandPaths(self, demandInd, count):
        return self.demands[demandInd].getPaths[0:count-1]