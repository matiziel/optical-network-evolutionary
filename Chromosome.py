from random import randint
from numpy.random import normal
from Gene import Gene

class Chromosome:
    def __init__(self, geneNum, alleleNum, maxValue):
        self.genes = []
        for _ in range(geneNum):
            newGene = Gene(alleleNum, maxValue)
            self.genes.append(newGene)
        self.mutation(maxValue)
    
    def getMatrix(self):
        chromo = []
        for gene in self.genes:
            chromo.append(gene.alleles)
        return chromo

    def mutation(self, maxValue):
        for gene in self.genes:
            gene.mutation(maxValue)

    def crossover(self, partner):
        if len(self.genes) != len(partner.genes):
            print("ERROR")