import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


X = []
Y = [[], [], [], []]


for i in range(len(Y)):
    with open("./testFiles/testfile" + str(i + 1) + ".txt", "r") as file:
        for x in file:
            s = x.split(',')
            if(i == 0):
                X.append(int(s[0]))
            Y[i].append(int(s[1]))


plt.plot(X, Y[0], label='geneProb = 1/150')
plt.plot(X, Y[1], label='geneProb = 1/100')
plt.plot(X, Y[2], label='geneProb = 1/75')
plt.plot(X, Y[3], label='geneProb = 1/50')


plt.ylabel('Koszt transponderów')
plt.xlabel('liczba iteracji')

plt.legend()

plt.show()
