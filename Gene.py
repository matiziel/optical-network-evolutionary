from Allele import Allele
from random import randint

class Gene:
    def __init__(self,  alleleNum, cardNum, maxValue):
        self.alleles = []
        for _ in range(alleleNum):
            newAllele = Allele(cardNum)
            self.alleles.append(newAllele)
        for _ in range(maxValue):
            self.alleles[randint(0,len(self.alleles)-1)].addOneBiggest()
    
    def mutation(self, deviation):
        for allele in self.alleles:
            allele.mutation(deviation)
    
    def getCost(self, costs):
        cost = 0
        for allele in self.alleles:
            cost += allele.getCost(costs)
        return cost
