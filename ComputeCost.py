from Network import Network
from Chromosome import Chromosome

PathNumParam = 2

network = Network()
chromosome1 = Chromosome(network.getDemandNum(), PathNumParam, network.getMaxDemand())
chromosome2 = Chromosome(network.getDemandNum(), PathNumParam, network.getMaxDemand())
print(chromosome1.getMatrix())
print(chromosome2.getMatrix())








#1 nie moga byc z gory ustalone wartosci na danym polaczeniu 0,10,40,100, bo mozemy miec na jednej linii nnp 80 (jezeli chcemy koszty kart jako parametry
#2 jak robic ten crossover, na poziomie genu czy allelu? chyba obu, zeby sie wszystko ladnie zmienialo. oba tak samo? inaczej? odwrotnie?
#3 najwiekszy demand = 198
#4 trzeba jakos graph tymczasowy robic, zeby krawedzie uzupelniac. inna klasa? ta sama? dziedziczenie?
#5 compute cost moglby byc jedna funkcja, klasa potrzebna? moze dac go jako metode do klasy wyzej