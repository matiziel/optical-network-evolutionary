class Flow:
    def __init__(self, edges):
        self.edges = edges
    
    def reset(self):
        self.edges = dict.fromkeys(self.edges, 0)
    
    def increment(self, link, value):
        self.edges[link] += value

    def getMaxValue(self):
        maxValue = 0
        for edge in self.edges:
            if self.edges[edge] > maxValue:
                maxValue = self.edges[edge]
        return maxValue