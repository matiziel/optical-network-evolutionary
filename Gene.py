from Allele import Allele

class Gene:
    def __init__(self,  alleleNum, cardNum, maxValue):
        self.alleles = []
        for _ in range(alleleNum):
            newAllele = Allele(cardNum, maxValue)
            self.alleles.append(newAllele)
    
    def mutation(self, mutationProb):
        for allele in self.alleles:
            allele.mutation(mutationProb)
    
    def getCost(self, costs):
        cost = 0
        for allele in self.alleles:
            cost += allele.getCost(costs)
        return cost