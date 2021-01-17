from Network import Network
from Chromosome import Chromosome

from random import randint

class Solver:
    def __init__(self):
        self.populationSize = 10
        self.limit = 96
        self.K = 2
        self.paramPathNum = 2
        self.cards = sorted([(10,2), (40,5), (100, 9)])
        self.deviation = 1
        self.geneProb = 0.01

        #filename = './Data/sample.xml'
        filename = './Data/polska.xml'
        self.network = Network(filename)
        self.population = []
        self.populate(self.populationSize)
    
    def loop(self, count):
        for i in range(count):
            self.newGeneration()
            print("gen#: ", i, " best: ", self.population[0][1])
        best = self.population[0][0]
        print("best chromosome: ", best.getMatrix())
        print("best value: ", self.evaluateIndividual(best))
    
    def populate(self, count):
        maxCardCapacity = sorted(self.cards, reverse=True)[0][0]
        maxCardCount = int(self.network.getMaxDemand() / maxCardCapacity) + 1
        for _ in range(count):
            newChromosome = Chromosome(self.network.getDemandNum(), self.paramPathNum, len(self.cards), maxCardCount)
            newCost = self.evaluateIndividual(newChromosome)
            self.population.append((newChromosome, newCost))
        # print("first chromo: ", self.population[0][0].getMatrix())
        # print("first cost: ", self.evaluateIndividual(self.population[0][0]))
    
    def newGeneration(self):
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        for _ in range(10):
            parent1 = self.population[randint(0,len(self.population) - 1)][0]
            parent2 = self.population[randint(0,len(self.population) - 1)][0]
            child1, child2 = Chromosome.kPointCrossover(parent1, parent2, self.K) #75% czasu siedzi tutaj
            child1.mutation(self.geneProb, self.deviation)
            child2.mutation(self.geneProb, self.deviation)
            child1Cost = self.evaluateIndividual(child1) #20% czasu siedzi tutaj
            child2Cost = self.evaluateIndividual(child2)
            self.population.append((child1, child1Cost))
            self.population.append((child2, child2Cost))
        self.population = sorted(self.population, key = lambda individual: individual[1])
        self.__killTheWeak()

    def __killTheWeak(self):
        self.population = self.population[0:self.populationSize]
    
    def evaluateIndividual(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes): #50% czasu siedzi tutaj
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, allele in enumerate(gene.alleles):
                path = paths[alleleInd]
                cards = sum(allele.alleleParts)
                for link in path:
                    self.network.incrementFlow(link, cards)

        cost = chromosome.getCost(self.cards) #40% czasu siedzi tutaj
        isOk = self.network.checkPathLimit(self.limit) #check if path limit 8, 16, 32, 96 satisfied
        if not(isOk):
            return cost + 60000000
            return float('inf')
        isOk = self.__checkDemandSatisfied(chromosome) #check if demands satisfied
        if not(isOk):
            return cost + 20000000
            return float('inf')
        return cost
    
    def __checkDemandSatisfied(self, chromosome):
        for geneInd, gene in enumerate(chromosome.genes):
            flow = 0
            for allele in gene.alleles:
                for allelePartInd, allelePart in enumerate(allele.alleleParts):
                    flow += allelePart * self.cards[allelePartInd][0]
            if flow < self.network.demands[geneInd].value:
                return False
        return True

solver = Solver()
solver.loop(100)