import xml.etree.ElementTree as ET


class Deserializer:
    def __init__(self):
        self.tree = ET.parse('./Data/polska.xml')
        self.root = tree.getroot()

    def getVertices(self):
        root['']


tree = ET.parse('./Data/polska.xml')
root = tree.getroot()
# for child in root:
#     for c in child:
#         print(c.attrib)

print(root[0][1][0].attrib)
