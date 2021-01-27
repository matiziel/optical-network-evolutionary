from Network import Network
from Chromosome import Chromosome

from random import randint, seed
from numpy import random as nprand
import random as rand
import numpy as np


class Solver:
    def __init__(self, populationSize=50, limit=96, K=20, paramPathNum=4, offspringPairs=30, deviation=1, geneProb=1/100):
        # program parameters-----------------------------------
        self.populationSize = populationSize
        self.limit = limit
        self.K = K
        self.paramPathNum = paramPathNum
        self.offspringPairs = offspringPairs
        self.deviation = deviation
        self.geneProb = geneProb
        self.cards = sorted([(10, 2), (40, 5), (100, 9)])
        # program parameters-----------------------------------

        filename = './Data/polska.xml'
        self.network = Network(filename)
        self.population = []
        self.populate(self.populationSize)
    
    def setSeed(self, seed):
        np.random.seed(seed)
        rand.seed(seed)

    def loop(self, count): # generate COUNT new generations and print the final value of the best individual
        for i in range(count):
            self.__newGeneration()
            print("gen#: ", i, " best lambda: ", self.__computeLambdaCount(
                self.population[0][0]), " best cost: ", self.__computeCardCost(self.population[0][0]))
        print("best value: ", self.population[0][1])

    def loopGetResults(self, count): # generate COUNT new generations and return a list of costs in each iteration
        results = []
        for _ in range(count):
            self.__newGeneration()
            results.append(self.__computeCardCost(self.population[0][0]))
        print("best value: ", self.population[0][1])
        return results

    def populate(self, count): # generate population at random
        maxCardCapacity = self.cards[-1][0]
        maxCardCount = int(self.network.getMaxDemand() / maxCardCapacity) + 1
        for _ in range(count):
            newChromosome = Chromosome(self.network.getDemandNum(
            ), self.paramPathNum, len(self.cards), maxCardCount)
            newCost = self.__evaluateIndividual(newChromosome)
            self.population.append((newChromosome, newCost))
        self.population = sorted(
            self.population, key=lambda individual: individual[1])
        self.__replacement()
        print("first cost: ", self.population[0][1])

    def __newGeneration(self): # randomly pick parents in a loop, crossover, mutate, append to new population, sort, kill the worst
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        for _ in range(self.offspringPairs):
            parent1 = self.population[randint(0, len(self.population) - 1)][0]
            parent2 = self.population[randint(0, len(self.population) - 1)][0]
            child1, child2 = Chromosome.kPointCrossover(
                parent1, parent2, self.K)
            child1.mutation(self.geneProb, self.deviation)
            child2.mutation(self.geneProb, self.deviation)
            # print("przed")
            # print("po")
            child1Cost = self.__evaluateIndividual(child1)
            child2Cost = self.__evaluateIndividual(child2)
            self.population.append((child1, child1Cost))
            self.population.append((child2, child2Cost))
        self.population = sorted(
            self.population, key=lambda individual: individual[1])
        self.__replacement()

    def __replacement(self):
        self.population = self.population[0:self.populationSize]

    def __computeCardCost(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, _ in enumerate(gene):
                path = paths[alleleInd]
                cards = sum(chromosome.genes[geneInd, alleleInd, :])
                for link in path:
                    self.network.incrementFlow(link, cards)

        cost = chromosome.getCost(self.cards)
        # check if path limit 8, 16, 32, 96 satisfied
        isOk = self.network.checkPathLimit(self.limit)
        if not(isOk):
            return cost + 60000000
            # return float('inf')
        isOk = self.__checkDemand(chromosome)  # check if demands satisfied
        if not(isOk):
            return cost + 20000000
            # return float('inf')
        return cost

    def __checkLimit(self, chromosome): # returns true if chromosome satisfies limit, returns false otherwise
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, _ in enumerate(gene):
                path = paths[alleleInd]
                cards = sum(chromosome.genes[geneInd, alleleInd, :])
                for link in path:
                    self.network.incrementFlow(link, cards)
        return self.network.checkPathLimit(self.limit)

    def __computeLambdaCount(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, _ in enumerate(gene):
                path = paths[alleleInd]
                cards = sum(chromosome.genes[geneInd, alleleInd, :])
                for link in path:
                    self.network.incrementFlow(link, cards)
        return self.network.flow.getMaxValue()

    def __evaluateIndividual(self, chromosome):
        return self.__EVALCostCheckLimit(chromosome) # Change evaluation method here

    def __EVALLambdaAndCost(self,chromosome):
        lSat = self.__checkLimit(chromosome)
        dSat = self.__checkDemand(chromosome)
        if not(lSat) or not(dSat):
            return float('inf')
        cardCost = self.__computeCardCost(chromosome)
        lambdaCount = self.__computeLambdaCount(chromosome)

        if lambdaCount > 96:
            coeff = 1.
        elif lambdaCount > 64:
            coeff = 0.8
        elif lambdaCount > 32:
            coeff = 0.6
        elif lambdaCount > 16:
            coeff = 0.4
        elif lambdaCount > 8:
            coeff = 0.2
        
        return  cardCost + lambdaCount * coeff

    def __EVALLambda(self,chromosome):
        if not(self.__checkDemand(chromosome)):
            return float('inf')
        return self.__computeLambdaCount(chromosome)

    def __EVALCostCheckLimit(self,chromosome):
        lSat = self.__checkLimit(chromosome)
        dSat = self.__checkDemand(chromosome)
        if not(lSat) or not(dSat):
            return float('inf')
        return self.__computeCardCost(chromosome)

    def __checkDemand(self, chromosome):
        for geneInd, gene in enumerate(chromosome.genes):
            flow = 0
            for allele in gene:
                for allelePartInd, allelePart in enumerate(allele):
                    flow += allelePart * self.cards[allelePartInd][0]
            if flow < self.network.demands[geneInd].value:
                return False
        return True
