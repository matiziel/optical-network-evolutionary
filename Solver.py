from Network import Network
from Chromosome import Chromosome

from random import randint

class Solver:
    def __init__(self):
        self.populationSize = 100
        self.limit = 64
        self.K = 20 #
        self.paramPathNum = 3 #
        self.cards = sorted([(10,2), (40,5), (100, 9)])
        self.deviation = 1
        self.geneProb = 1/100. #
        self.offspringPairs = 30

        filename = './Data/polska.xml'
        self.network = Network(filename)
        self.population = []
        self.populate(self.populationSize)
    
    def loop(self, count):
        for i in range(count):
            self.newGeneration()
            print("gen#: ", i, " best lambda: ", self.__evaluateLambdaCount(self.population[0][0]), " best cost: ", self.__evaluateCardCost(self.population[0][0]))
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
        for _ in range(self.offspringPairs):
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
    
    def __evaluateCardCost(self, chromosome):
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

    def __evaluateLambdaCount(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, _ in enumerate(gene):
                path = paths[alleleInd]
                cards = sum(chromosome.genes[geneInd,alleleInd,:])
                for link in path:
                    self.network.incrementFlow(link, cards)

        cost = self.network.flow.getMaxValue()
        isOk = self.__checkDemandSatisfied(chromosome) #check if demands satisfied
        if not(isOk):
            return cost + 20000000
            # return float('inf')
        return cost

    def __evaluateIndividual(self, chromosome):
        lambdaCount = self.__evaluateLambdaCount(chromosome)
        coeff = 0

        if lambdaCount > 96:
            coeff = 1.
        elif lambdaCount > 64:
            coeff = 0.9
        elif lambdaCount > 32:
            coeff = 0.7
        elif lambdaCount > 16:
            coeff = 0.5
        elif lambdaCount > 8:
            coeff = 0.3
        else:
            coeff = 0.1

        cardCost = self.__evaluateCardCost(chromosome)
        return lambdaCount*coeff + cardCost
        # return lambdaCount + cardCost/10.
        # return lambdaCount
        # return cardCost

    
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