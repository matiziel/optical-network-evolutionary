from random import randint, sample
from numpy.random import normal
from Gene import Gene
from copy import deepcopy

class Chromosome:
    def __init__(self, geneNum, alleleNum, allelePartNum, maxValue):
        self.genes = []
        for _ in range(geneNum):
            newGene = Gene(alleleNum, allelePartNum, maxValue)
            self.genes.append(newGene)

    def __setGenes(self, genes):
        self.genes = genes
    
    def getMatrix(self):
        chromoList = []
        for gene in self.genes:
            genList = []
            for allele in gene.alleles:
                genList.append(allele.alleleParts)
            chromoList.append(genList)
        return chromoList

    def mutation(self, deviation):
        for gene in self.genes:
            gene.mutation(deviation)

    @staticmethod
    def kPointCrossover(chromo1, chromo2, K):
        child1 = deepcopy(chromo1.genes)
        child2 = deepcopy(chromo2.genes)
        if len(child1) != len(child2):
            raise Exception("Different gene count in crossover")
        cutPoints = sample(range(1,len(child1)), 2)
        swapState = True
        for i in range(0, len(child1)):
            if i in cutPoints:
                swapState = not(swapState)
            if swapState:
                child2[i], child1[i] = child1[i], child2[i]
        result1 = Chromosome(0,0,0,0)
        result1.__setGenes(child1)
        result2 = Chromosome(0,0,0,0)
        result2.__setGenes(child2)
        return result1, result2
    
    def getCost(self, costs):
        cost = 0
        for gene in self.genes:
            cost += gene.getCost(costs)
        return cost

# parent1 = Chromosome(10,1,1,1)
# parent2 = Chromosome(10,1,1,1)
# print(parent1.getMatrix())
# print(parent2.getMatrix())
# child1, child2 = Chromosome.kPointCrossover(parent1, parent2, 2)
# print(parent1.getMatrix())
# print(parent2.getMatrix())