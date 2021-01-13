from Network import Network
from Chromosome import Chromosome

class Solver:
    def __init__(self, populationSize):
        filename = './Data/sample.xml'
        # filename = './Data/polska.xml'
        self.network = Network(filename)
        self.paramPathNum = 2
        self.cards = [(10,2), (40,5), (100, 9)]
        self.population = []
        self.populationSize = populationSize
        self.populate(populationSize)
    
    def populate(self, count):
        minCardValue = sorted(self.cards)[0][0]
        maxCardCount = int(self.network.getMaxDemand() / minCardValue)
        maxCardCount = 6
        for _ in range(count):
            self.population.append(Chromosome(self.network.getDemandNum(), self.paramPathNum, len(self.cards), maxCardCount))
    
    def newGeneration(self):
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        # pick parent pairs: turniejowo/progowo/ruletkowo
        # produce children
        # assign value to every child
        # create new population
    
    def evaluateIndividual(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome.genes):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, allele in enumerate(gene.alleles):
                path = paths[alleleInd]
                cards = sum(allele.alleleParts)
                for link in path:
                    self.network.incrementFlow(link, cards)

        isOk = self.network.checkPathLimit(1000) #check if path limit 8, 16, 32, 96 satisfied
        if not(isOk):
            return float('inf')
        isOk = self.__checkDemandSatisfied(chromosome) #check if demands satisfied
        if not(isOk):
            return float('inf')
        return chromosome.getCost(self.cards)
    
    def __checkDemandSatisfied(self, chromosome):
        for geneInd, gene in enumerate(chromosome.genes):
            flow = 0
            for allele in gene.alleles:
                for allelePartInd, allelePart in enumerate(allele.alleleParts):
                    flow += allelePart * self.cards[allelePartInd][0]
            print(flow)
            if flow < self.network.demands[geneInd].value:
                return False
        return True

solver = Solver(5)
print("chromosome: ", solver.population[0].getMatrix())
print("value: ", solver.evaluateIndividual(solver.population[0]))