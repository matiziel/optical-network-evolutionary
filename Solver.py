from Network import Network
from Chromosome import Chromosome

from random import randint


class Solver:
    def __init__(self, populationSize=100, limit=96, K=5, paramPathNum=3, offspringPairs=30, geneProb=1/100):
        self.populationSize = populationSize
        self.limit = limit
        self.K = K
        self.paramPathNum = paramPathNum
        self.cards = sorted([(10, 2), (40, 5), (100, 9)])
        self.deviation = 1
        self.geneProb = geneProb
        self.offspringPairs = offspringPairs

        filename = './Data/polska.xml'
        self.network = Network(filename)
        self.population = []
        self.populate(self.populationSize)

    def loop(self, count):
        results = []
        for i in range(count):
            self.newGeneration()
            # print("gen#: ", i, " best lambda: ", self.__evaluateLambdaCount(
            #     self.population[0][0]), " best cost: ", self.__evaluateCardCost(self.population[0][0]))
            results.append(self.__evaluateCardCost(self.population[0][0]))
        best = self.population[0]
        # print("best chromosome: ", best[0].genes)
        print("best value: ", best[1])
        return results

    def populate(self, count):
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

    def newGeneration(self):
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        for _ in range(self.offspringPairs):
            parent1 = self.population[randint(0, len(self.population) - 1)][0]
            parent2 = self.population[randint(0, len(self.population) - 1)][0]
            child1, child2 = Chromosome.kPointCrossover(
                parent1, parent2, self.K)
            child1.mutation(self.geneProb, self.deviation)
            child2.mutation(self.geneProb, self.deviation)
            child1Cost = self.__evaluateIndividual(child1)
            child2Cost = self.__evaluateIndividual(child2)
            self.population.append((child1, child1Cost))
            self.population.append((child2, child2Cost))
        self.population = sorted(
            self.population, key=lambda individual: individual[1])
        self.__replacement()

    def __replacement(self):
        self.population = self.population[0:self.populationSize]

    def __evaluateCardCost(self, chromosome):
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
        isOk = self.__checkDemandSatisfied(
            chromosome)  # check if demands satisfied
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
                cards = sum(chromosome.genes[geneInd, alleleInd, :])
                for link in path:
                    self.network.incrementFlow(link, cards)

        cost = self.network.flow.getMaxValue()
        isOk = self.__checkDemandSatisfied(
            chromosome)  # check if demands satisfied
        if not(isOk):
            return cost + 20000000
            # return float('inf')
        return cost

    def __evaluateIndividual(self, chromosome):
        cardCost = self.__evaluateCardCost(chromosome)
        return cardCost

        # lambdaCount = self.__evaluateLambdaCount(chromosome)
        # coeff = 0

        # if lambdaCount > 96:
        #     coeff = 1.
        # elif lambdaCount > 64:
        #     coeff = 0.9
        # elif lambdaCount > 32:
        #     coeff = 0.7
        # elif lambdaCount > 16:
        #     coeff = 0.5
        # elif lambdaCount > 8:
        #     coeff = 0.3
        # else:
        #     coeff = 0.1

        # return lambdaCount*coeff + cardCost
        # return lambdaCount + cardCost/10.
        # return lambdaCount

    def __checkDemandSatisfied(self, chromosome):
        for geneInd, gene in enumerate(chromosome.genes):
            flow = 0
            for allele in gene:
                for allelePartInd, allelePart in enumerate(allele):
                    flow += allelePart * self.cards[allelePartInd][0]
            if flow < self.network.demands[geneInd].value:
                return False
        return True


files = ["./testFiles/testfile1.txt",
         "./testFiles/testfile2.txt",
         "./testFiles/testfile3.txt",
         "./testFiles/testfile4.txt"]


populationSizes = [20, 50, 100, 150]

Ks = [5, 10, 20, 40]

offspringPairs = [10, 20, 30, 40]

limits = [64, 96]

paths = [3, 4, 5, 6, 7]

geneProbs = [1/150, 1/100, 1/75, 1/50]

X = list(range(1000))


iterNumber = 10

for i in range(len(files)):
    Y = []
    for k in range(iterNumber):
        solver = Solver(populationSize=100, limit=96, K=20,
                        paramPathNum=4, offspringPairs=30, geneProb=geneProbs[i])
        Y.append(solver.loop(10))
    with open(files[i], "w") as file:
        for m in range(len(Y[0])):
            resultSum = 0
            for l in range(len(Y)):
                resultSum += Y[l][m]
            file.write(str(resultSum/iterNumber) + "\n")
