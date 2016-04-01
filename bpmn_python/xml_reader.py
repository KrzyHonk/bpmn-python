from xml.dom import minidom

"""
Simple scrip that reads BPMN 2.0 XML file from given filepath and returns xml.dom.xminidom.Document object
"""

def readXmlFile (filepath):
    domTree = minidom.parse(filepath)
    return domTree