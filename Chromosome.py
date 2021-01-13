from random import randint, sample
from numpy.random import normal
from Gene import Gene

class Chromosome:
    def __init__(self, geneNum, alleleNum, allelePartNum):
        self.genes = []
        for _ in range(geneNum):
            newGene = Gene(alleleNum, allelePartNum)
            self.genes.append(newGene)

    def __setGenes(self, genes):
        self.genes = genes
    
    def getMatrix(self):
        chromo = []
        for gene in self.genes:
            chromo.append(gene.alleles)
        return chromo

    def mutation(self, maxValue):
        for gene in self.genes:
            gene.mutation(maxValue)

    @staticmethod
    def kPointCrossover(chromo1, chromo2, K):
        child1 = chromo1.genes
        child2 = chromo2.genes
        if len(child1) != len(child2):
            raise Exception("Different gene count in crossover")
        cutPoints = sample(range(1,len(child1)), 2)
        swapState = True
        for i in range(0, len(child1)):
            if i in cutPoints:
                swapState = not(swapState)
            if swapState:
                child2[i], child1[i] = child1[i], child2[i]
        result1 = Chromosome(0,0,0)
        result1.__setGenes(child1)
        result2 = Chromosome(0,0,0)
        result2.__setGenes(child2)
        return result1, result2