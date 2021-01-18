from Network import Network
from Chromosome import Chromosome

from random import randint

class Solver:
    def __init__(self):
        self.populationSize = 20
        self.limit = 60
        self.K = 2
        self.paramPathNum = 6
        self.cards = sorted([(10,2), (40,5), (100, 9)])
        self.deviation = 1
        self.geneProb = 1/66.

        #filename = './Data/sample.xml'
        filename = './Data/polska.xml'
        self.network = Network(filename)
        self.population = []
        self.populate(10000)
    
    def loop(self, count):
        for i in range(count):
            self.newGeneration()
            if(self.population[0][1] < 1035):
                break
            print("gen#: ", i, " best: ", self.population[0][1])
        best = self.population[0]
        print("best chromosome: ", best[0].genes)
        print("best value: ", best[1])
    
    def populate(self, count):
        maxCardCapacity = self.cards[-1][0]
        maxCardCount = int(self.network.getMaxDemand() / maxCardCapacity) + 1
        for _ in range(count):
            newChromosome = Chromosome(self.network.getDemandNum(), self.paramPathNum, len(self.cards), maxCardCount)
            newCost = self.__evaluateIndividual(newChromosome)
            self.population.append((newChromosome, newCost))
        self.population = sorted(self.population, key = lambda individual: individual[1])
        self.__replacement()
        print("first cost: ", self.population[0][1])
    
    def newGeneration(self):
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        for _ in range(10):
            parent1 = self.population[randint(0,len(self.population) - 1)][0]
            parent2 = self.population[randint(0,len(self.population) - 1)][0]
            child1, child2 = Chromosome.kPointCrossover(parent1, parent2, self.K) 
            child1.mutation(self.geneProb, self.deviation)
            child2.mutation(self.geneProb, self.deviation)
            child1Cost = self.__evaluateIndividual(child1) 
            child2Cost = self.__evaluateIndividual(child2)
            self.population.append((child1, child1Cost))
            self.population.append((child2, child2Cost))
        self.population = sorted(self.population, key = lambda individual: individual[1])
        self.__replacement()

    def __replacement(self):
        self.population = self.population[0:self.populationSize]
    
    def __evaluateIndividual(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, _ in enumerate(gene):
                path = paths[alleleInd]
                cards = sum(chromosome.genes[geneInd,alleleInd,:])
                for link in path:
                    self.network.incrementFlow(link, cards)

        cost = chromosome.getCost(self.cards) 
        isOk = self.network.checkPathLimit(self.limit) #check if path limit 8, 16, 32, 96 satisfied
        if not(isOk):
            return cost + 60000000
            # return float('inf')
        isOk = self.__checkDemandSatisfied(chromosome) #check if demands satisfied
        if not(isOk):
            return cost + 20000000
            # return float('inf')
        return cost
    
    def __checkDemandSatisfied(self, chromosome):
        for geneInd, gene in enumerate(chromosome.genes):
            flow = 0
            for allele in gene:
                for allelePartInd, allelePart in enumerate(allele):
                    flow += allelePart * self.cards[allelePartInd][0]
            if flow < self.network.demands[geneInd].value:
                return False
        return True

solver = Solver()
solver.loop(100000)