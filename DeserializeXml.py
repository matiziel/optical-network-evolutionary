import xml.etree.ElementTree as ET
from Demand import Demand

class Deserializer:
    def __init__(self, filename):
        tree = ET.parse(filename)
        self.root = tree.getroot()

    def getCities(self):
        vertices = []
        for child in self.root[0][0]:
            vertices.append(child.attrib['id'])
        return vertices

    def getFlowEdges(self):
        edges = {}
        for child in self.root[0][1]:
            link = child.attrib['id'].split('_')
            index = (int(link[1]), int(link[2]))
            edges[index] = 0
        return edges

    def getLinks(self):
        edges = []
        for child in self.root[0][1]:
            link = child.attrib['id'].split('_')
            edges.append((int(link[1]),int(link[2])))
        return edges

    def getDemands(self):
        demands = []
        cunder100 = 0
        c100_110 = 0
        c110_120 = 0
        c120_140 = 0
        c140_150 = 0
        cover150 = 0
        for demand in self.root[1]:
            cities = demand.attrib['id'].split('_')

            link = (int(cities[1]), int(cities[2]))
            value = int(float(demand[2].text))
            if value <= 100:
                cunder100 += 1
            if value > 100 and value <= 110:
                c100_110 += 1
            if value > 110 and value <= 120:
                c110_120 += 1
            if value > 120 and value <= 140:
                c120_140 += 1
            if value > 140 and value <= 150:
                c140_150 += 1
            if value > 150:
                cover150 += 1
            paths = self.__getAdmissiblePaths(demand[3])

            newdemand = Demand(link,value,paths)
            demands.append(newdemand)
        sum = cunder100 * 9 + c100_110 * 11 + c110_120 * 13 + c120_140 * 14 + c140_150 * 16 + cover150 * 18
        print("suma", sum)
        return demands

    def __getAdmissiblePaths(self, data):
        paths = []
        for path in data:
            partialPath = []
            for link in path:
                cities = link.text.split('_')
                partialPath.append((int(cities[1]), int(cities[2])))
            paths.append(partialPath)
        return paths

