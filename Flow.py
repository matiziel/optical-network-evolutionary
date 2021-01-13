class Flow:
    def __init__(self, edges):
        self.edges = edges
    
    def reset(self):
        for edgeInd in self.edges:
            self.edges[edgeInd] = 0
    
    def increment(self, link):
        self.edges[link] += 1
