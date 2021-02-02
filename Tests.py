from Solver import Solver
from DrawGraphs import draw

seed = 0

iterNumber = 5000
repeatNumber = 1

testedValues = [[(5, 2), (10, 3), (50, 4), (150,14), (100, 10), (200, 26)]]
labels = []
for i in testedValues:
    # labels.append("parentCount = " + str(format(i, '.3g')))
    label = ""
    for j in i:
        label += str(j[0]) + ", " + str(j[1]) + "      "
    labels.append("Card costs = " + label)

for versionInd in range(len(testedValues)):
    print("Version " + str(versionInd))
    results = []
    for k in range(repeatNumber):
        print("Iteration " + str(k))
        solver = Solver(cards=testedValues[versionInd])
        solver.setSeed(0)
        results.append(solver.loopGetResults(iterNumber))

    resultAverage = []
    for iteration in range(iterNumber):
        resultSum = 0
        for runInd in range(repeatNumber):
            resultSum += results[runInd][iteration]
        resultAverage.append(resultSum/repeatNumber)
        
    fileName = "./results/test_" + str(versionInd)
    with open(fileName, "w") as file:
        if file.closed:
            raise Exception("Cannot open file")
        for result in resultAverage:
            file.write(str(result) + "\n")

draw(labels)
