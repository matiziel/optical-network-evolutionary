from Network import Network
from Chromosome import Chromosome
from random import sample

PathNumParam = 2

network = Network()
chromosome1 = Chromosome(network.getDemandNum(), PathNumParam, network.getCardNum())
chromosome2 = Chromosome(network.getDemandNum(), PathNumParam, network.getCardNum())


children = Chromosome.kPointCrossover(chromosome1, chromosome2, 2)
children[0].print()


#1 nie moga byc z gory ustalone wartosci na danym polaczeniu 0,10,40,100, bo mozemy miec na jednej linii nnp 80 (jezeli chcemy koszty kart jako parametry
#2 jak robic ten crossover, na poziomie genu czy allelu? chyba obu, zeby sie wszystko ladnie zmienialo. oba tak samo? inaczej? odwrotnie?
#3 najwiekszy demand = 198
#4 trzeba jakos graph tymczasowy robic, zeby krawedzie uzupelniac. inna klasa? ta sama? dziedziczenie?
#5 compute cost moglby byc jedna funkcja, klasa potrzebna? moze dac go jako metode do klasy wyzej
