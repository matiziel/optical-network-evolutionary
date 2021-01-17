from random import randint, sample, random
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

    def mutation(self, geneProb, deviation):
        for gene in self.genes:
            if random() < geneProb:
                gene.mutation(deviation)

    @staticmethod
    def kPointCrossover(chromo1, chromo2, K):
        if len(chromo1.genes) != len(chromo2.genes):
            raise Exception("Different gene count in crossover")
        child1 = []
        child2 = []
        cutPoints = sample(range(1,len(chromo1.genes)), K)
        swapState = True
        for i in range(0, len(chromo1.genes)):
            if i in cutPoints:
                swapState = not(swapState)
            if swapState:
                child1.append(deepcopy(chromo2.genes[i])) #dlugo kopiuje - nie wiem jak uniknac
                child2.append(deepcopy(chromo1.genes[i]))
            else:
                child1.append(deepcopy(chromo1.genes[i]))
                child2.append(deepcopy(chromo2.genes[i]))
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