from Solver import Solver
from DrawGraphs import draw

seed = 0

iterNumber = 1000
repeatNumber = 10

testedValues = [1/50, 1/75, 1/100, 1/150]
labels = []
for i in testedValues:
    labels.append("geneProb = " + str(format(i, '.3g')))


for versionInd in range(len(testedValues)):

    results = []
    for k in range(repeatNumber):
        solver = Solver(geneProb=testedValues[versionInd], offspringPairs=3, populationSize=10)
        # solver.setSeed(seed)
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
