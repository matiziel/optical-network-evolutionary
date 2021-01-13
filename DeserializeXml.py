import xml.etree.ElementTree as ET
from Demand import Demand

class Deserializer:
    def __init__(self):
        tree = ET.parse('./Data/polska.xml')
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
            index = (int(link[1]),int(link[2]))
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
        for demand in self.root[1]:
            cities = demand.attrib['id'].split('_')

            link = (cities[1], cities[2])
            value = int(float(demand[2].text))
            paths = self.getAdmissiblePaths(demand[3])

            newdemand = Demand(link,value,paths)
            demands.append(newdemand)
        return demands

    def getAdmissiblePaths(self, data):
        paths = []
        for path in data:
            partialPath = []
            for link in path:
                cities = link.text.split('_')
                partialPath.append((cities[1], cities[2]))
            paths.append(partialPath)
        return paths

