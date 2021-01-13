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
        for _ in range(count):
            self.population.append(Chromosome(self.network.getDemandNum(), self.paramPathNum, len(self.cards), maxCardCount))
    
    def newGeneration(self):
        if self.population == []:
            raise Exception("Empty population, cannot generate new members")
        # pick parent pairs: turniejowo/progowo/ruletkowo
        # produce children
        # assign value to every child
        # create new population
    
    def checkOsobnik(self, chromosome):
        self.network.resetFlow()
        for geneInd, gene in enumerate(chromosome):
            paths = self.network.getDemandPaths(geneInd, self.paramPathNum)
            for alleleInd, allele in enumerate(gene):
                path = paths[alleleInd]
                cards = sum(allele)
                for link in path:
                    self.network.incrementFlow(link, cards)
                    #TODO: jezeli przepelniony, return 0
        return chromosome.getCost()

solver = Solver(5)
print(solver.population[0].getMatrix())