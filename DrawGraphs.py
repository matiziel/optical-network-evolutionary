import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def draw(labels):
    Y = []

    with open("./results/test_0", "r") as file:
        if file.closed:
            raise Exception("Generated files are missing")
        for i, _ in enumerate(file):
            pass
        X = list(range(i+1))

    for i in range(len(labels)):
        Y.append([])
        with open("./results/test_" + str(i), "r") as file:
            if file.closed:
                raise Exception("Generated files are missing")
            for line in file:
                number = line[:-1]
                Y[i].append(float(number))
        plt.plot(X, Y[i], label=labels[i])

    plt.ylabel('Card cost')
    plt.xlabel('Iteration number')

    plt.legend()
    plt.show()