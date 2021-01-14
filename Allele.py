from random import random, randint
from numpy.random import normal

class Allele:
    def __init__(self, cardNum):
        self.alleleParts = []
        for _ in range(cardNum):
            self.alleleParts.append(0)
    
    def addOneBiggest(self):
        self.alleleParts[-1] += 1
  
    def mutation(self, deviation):
        for i in range(len(self.alleleParts)):
            self.alleleParts[i] += int(normal(0,deviation))
            self.alleleParts[i] = max(0,self.alleleParts[i])
    
    def getCost(self, costs):
        if len(self.alleleParts) != len(costs):
            raise Exception("Different cost list count in evaluation")
        cost = 0
        for i in range(len(self.alleleParts)):
            cost += self.alleleParts[i]*costs[i][1]
        return cost
