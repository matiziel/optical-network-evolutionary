from random import random, randint

class Allele:
    def __init__(self, cardNum, maxValue):
        self.alleleParts = []
        for _ in range(cardNum):
            newPart = randint(0,maxValue)
            self.alleleParts.append(newPart)
  
    def mutation(self, mutationProb):
        for i in range(len(self.alleleParts)):
            if random() < mutationProb:
                if random() < 0.5:
                    self.alleleParts[i] += 1
                else:
                    self.alleleParts[i] = max(0,self.alleleParts[i]-1)
    
    def getCost(self, costs):
        if len(self.alleleParts) != len(costs):
            raise Exception("Different cost list count in evaluation")
        cost = 0
        for i in range(len(self.alleleParts)):
            cost += self.alleleParts[i]*costs[i][1]
        return cost