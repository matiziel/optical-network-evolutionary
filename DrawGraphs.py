import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


X = []
Y = []


for i in range(1):
    with open("./testFiles/testfile" + str(i + 1) + ".txt", "r") as file:
        for x in file:
            s = x.split(',')
            if(i == 0):
                X.append(int(s[0]))
            Y.append(int(s[2]))


plt.plot(X, Y)
# plt.plot(X, Y[1], label='K = 10')
# plt.plot(X, Y[2], label='K = 20')
# plt.plot(X, Y[3], label='K = 40')



plt.ylabel('Ilość lambd')
plt.xlabel('liczba iteracji')

plt.legend()

plt.show()
