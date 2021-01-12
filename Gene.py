from random import randint
from numpy.random import normal

class Gene:
    def __init__(self,  alleleNum, maxValue):
        self.alleles = []
        for _ in range(alleleNum):
            newAllele = randint(0,maxValue)
            self.alleles.append(newAllele)
        self.mutation(maxValue)

    def mutation(self, maxValue):
        deviation = 5 
        for alleleInd, _ in enumerate(self.alleles):
            oldAllele = self.alleles[alleleInd]
            change = int(normal(0, deviation))
            newAllele = oldAllele + change
            newAllele = max(min(newAllele, maxValue), 0)
            self.alleles[alleleInd] = newAllele
    
    def crossover(self, partner):
        if len(self.alleles) != len(partner.alleles):
            print("ERROR")