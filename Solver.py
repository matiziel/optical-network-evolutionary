from Network import Network
from Chromosome import Chromosome

class Solver:
    def __init__(self):
        self.populationSize = 2
        self.limit = 150
        self.K = 2
        self.paramPathNum = 2
        self.cards = [(10,2), (40,5), (100, 9)]

        filename = './Data/sample.xml'
        # filename = './Data/polska.xml'
        self.network = Network(filename)
        self.population = []
        self.populate(self.populationSize)
    
    def populate(self, count):
        minCardValue = sorted(self.cards)[0][0]
        maxCardCount = int(self.network.getMaxDemand() / minCardValue)
        maxCardCount = 6
        for _ in range(count):
            newChromosome = Chromosome(self.network.getDemandNum(), self.paramPathNum, len(self.cards), maxCardCount)
            newCost = self.evaluateIndividual(newChromosome)
            self.population.append((newChromosome, newCost))
    
    def newGeneration(self):
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        children = []
        for index in range(int(self.populationSize/2)):
            parent1 = self.population[2*index][0]
            parent2 = self.population[2*index + 1][0]
            child1, child2 = Chromosome.kPointCrossover(parent1, parent2, self.K)
            child1Cost = self.evaluateIndividual(child1)
            child2Cost = self.evaluateIndividual(child2)
            children.append((child1, child1Cost))
            children.append((child2, child2Cost))
        # TODO create new population from parents +children, ruletkowo
        for parent in self.population:
            print("parent: ", parent[0].getMatrix())
        for child in children:
            print("child: ", child[0].getMatrix(), " ", child[1])
    
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
solver.newGeneration()