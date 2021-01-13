from Network import Network
from Chromosome import Chromosome

class Solver:
    def __init__(self):
        filename = './Data/sample.xml'
        # filename = './Data/polska.xml'
        self.network = Network(filename)
        self.paramPathNum = 2
        self.cards = [(10,2), (40,5), (100, 9)]
        self.population = []
        self.log = []
    
    def populate(self, count):
        minCardValue = sorted(self.cards)[0][0]
        maxCardCount = int(self.network.getMaxDemand() / minCardValue)
        for _ in range(count): #TODO madrzejsza generacja
            self.population.append(Chromosome(self.network.getDemandNum(), self.paramPathNum, len(self.cards), maxCardCount))
    
    def newGeneration(self):
        if self.population == []:
            print("pusto")
        # pick parent pairs
        # produce children
        # assign value to every child
        # save children to log ( delete worst?? stala pamiec ale tracimy historie)
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

solver = Solver()
solver.populate(10)
print(solver.population[0].getMatrix())