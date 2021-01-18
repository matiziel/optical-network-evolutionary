from random import randint, sample, random
import numpy as np

class Chromosome:
    def __init__(self, geneNum, alleleNum, allelePartNum, maxValue):
        self.genes = np.zeros((geneNum, alleleNum, allelePartNum), dtype = int)
        for i in range(geneNum):
            for _ in range(maxValue):
                self.genes[i,randint(0,alleleNum-1),-1] += 1

    def __setGenes(self, genes):
        self.genes = genes
    
    def mutation(self, geneProb, deviation):
        shape = self.genes.shape
        for gene in self.genes:
            if random() < geneProb:
                for allele in gene:
                    for index in range(shape[2]):
                        allele[index] += int(np.random.normal(0,deviation))
        self.genes = np.maximum(self.genes, 0)

    @staticmethod
    def kPointCrossover(parent1, parent2, K):
        if parent1.genes.shape != parent2.genes.shape:
            raise Exception("Different chromosome shape in crossover")
        parentShape = parent1.genes.shape
        if K > parentShape[0]:
            raise Exception("kPointCrossover: k larger than number of genes")
        child1 = np.zeros(parentShape, dtype=int)
        child2 = np.zeros(parentShape, dtype=int)
        cutPoints = sample(range(0, parentShape[0]), K)
        swapState = True
        for i in range(0, parentShape[0]):
            if i in cutPoints:
                swapState = not(swapState)
            if swapState:
                child1[i,:,:] = parent1.genes[i,:,:]
                child2[i,:,:] = parent2.genes[i,:,:]
            else:
                child1[i,:,:] = parent2.genes[i,:,:]
                child2[i,:,:] = parent1.genes[i,:,:]
        result1 = Chromosome(0,0,0,0)
        result1.__setGenes(child1)
        result2 = Chromosome(0,0,0,0)
        result2.__setGenes(child2)
        return result1, result2
    
    def getCost(self, costs):
        cost = 0
        shape = self.genes.shape
        for gene in self.genes:
            for allele in gene:
                for index in range(shape[2]):
                    cost += allele[index] * costs[index][1]
        return cost