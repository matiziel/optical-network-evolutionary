class Flow:
    def __init__(self, edges):
        self.edges = edges
    
    def reset(self):
        self.edges = dict.fromkeys(self.edges, 0)
    
    def increment(self, link, value):
        self.edges[link] += value