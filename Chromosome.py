from random import randint
from numpy.random import normal
from Gene import Gene

class Chromosome:
    def __init__(self, geneNum, alleleNum, maxValue):
        self.genes = []
        for _ in range(geneNum):
            newGene = Gene(alleleNum, maxValue)
            self.genes.append(newGene)
        print(self.getMatrix())
        self.mutation(maxValue)
        print(self.getMatrix())
    
    def getMatrix(self):
        chromo = []
        for gene in self.genes:
            chromo.append(gene.alleles)
        return chromo

    def mutation(self, maxValue):
        for gene in self.genes:
            gene.mutation(maxValue)

    def crossover(self, partner):
        if len(self.genes) != len(partner.genes):
            print("ERROR")

chromo = Chromosome(10, 3, 100)

#1 nie moga byc z gory ustalone wartosci na danym polaczeniu 0,10,40,100, bo mozemy miec na jednej linii nnp 80 (jezeli chcemy koszty kart jako parametry)
#2 jak robic ten crossover, na poziomie genu czy allelu? chyba obu, zeby sie wszystko ladnie zmienialo. oba tak samo? inaczej? odwrotnie?
