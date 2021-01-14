from Network import Network
from Chromosome import Chromosome

class Solver:
    def __init__(self):
        self.populationSize = 2
        self.limit = 96
        self.K = 2
        self.paramPathNum = 2
        self.cards = [(10,2), (40,5), (100, 9)]
        self.mutationProb = 0.8

        filename = './Data/sample.xml'
        # filename = './Data/polska.xml'
        self.network = Network(filename)
        self.population = []
        self.populate(self.populationSize)
    
    def loop(self, count):
        for i in range(count):
            print("loop ", i)
            self.newGeneration()
            #for individual in self.population:
                #print("individual: ", individual[0].getMatrix(), ", cost: ", self.evaluateIndividual(individual[0]))
        #best = self.population[0][0]
        #print(best.getMatrix())
        #print(self.evaluateIndividual(best))
    
    def populate(self, count):
        minCardValue = sorted(self.cards)[0][0]
        maxCardCount = int(self.network.getMaxDemand() / minCardValue)
        maxCardCount = 6
        for _ in range(count):
            newChromosome = Chromosome(self.network.getDemandNum(), self.paramPathNum, len(self.cards), maxCardCount)
            newCost = self.evaluateIndividual(newChromosome)
            self.population.append((newChromosome, newCost))
    
    def newGeneration(self):
        # for individual in self.population:
        #     print("BEFORE: individual: ", individual[0].getMatrix(), ", cost: ", self.evaluateIndividual(individual[0]))
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        newPopulation = self.population.copy()
        for index in range(int(self.populationSize/2)):
            parent1 = self.population[2*index][0]
            parent2 = self.population[2*index + 1][0]
            child1, child2 = Chromosome.kPointCrossover(parent1, parent2, self.K)
            print("parent1 before child mutation: ", parent1.getMatrix())
            print("parent2 before child mutation: ", parent2.getMatrix())
            print("child1 before child mutation:  ", child1.getMatrix())
            print("child2 before child mutation:  ", child2.getMatrix())
            child1.mutation(self.mutationProb)
            child2.mutation(self.mutationProb)
            #MUTACJA DZIECI ZMIENIA RODZICOW??????????????????????
            print("parent1 after child mutation:  ", parent1.getMatrix())
            print("parent2 after child mutation:  ", parent2.getMatrix())
            print("child1 after child mutation:   ", child1.getMatrix())
            print("child2 after child mutation:   ", child2.getMatrix())
            child1Cost = self.evaluateIndividual(child1)
            child2Cost = self.evaluateIndividual(child2)
            newPopulation.append((child1, child1Cost))
            newPopulation.append((child2, child2Cost))
        # for individual in newPopulation:
        #     print("all: individual: ", individual[0].getMatrix(), ", cost: ", self.evaluateIndividual(individual[0]))
        newPopulation = sorted(newPopulation, key = lambda individual: individual[1])
        # for individual in newPopulation:
        #     print("allsorted: individual: ", individual[0].getMatrix(), ", cost: ", self.evaluateIndividual(individual[0]))
        for i in range(len(self.population)):
            self.population[i] = newPopulation[i]
        # for individual in self.population:
        #     print("AFTER: individual: ", individual[0].getMatrix(), ", cost: ", self.evaluateIndividual(individual[0]))
    
    def evaluateIndividual(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, allele in enumerate(gene.alleles):
                path = paths[alleleInd]
                cards = sum(allele.alleleParts)
                for link in path:
                    self.network.incrementFlow(link, cards)

        isOk = self.network.checkPathLimit(self.limit) #check if path limit 8, 16, 32, 96 satisfied
        if not(isOk):
            return float('inf')
        isOk = self.__checkDemandSatisfied(chromosome) #check if demands satisfied
        if not(isOk):
            return float('inf')
        cost = chromosome.getCost(self.cards)
        #print("evaluating chromosome: ", chromosome.getMatrix())
        #print("cost: ", cost)
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
solver.loop(1)