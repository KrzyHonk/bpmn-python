import unittest
import os
import bpmn_python.bpmn_diagram_rep as diagram

"""
    Put breakpoint on print instruction and use debugger to check objects structure.
"""

class MyTestCase(unittest.TestCase):
    def test_readXmlFile(self):
        domTree = diagram.read_xml_file(os.path.abspath("../examples/BPMNEditor-example.xml"))
        processElement = domTree.getElementsByTagNameNS("*","process")[0]
        diagramElement = domTree.getElementsByTagNameNS("*","BPMNDiagram")[0]
        element = processElement.firstChild;
        print(os.path.abspath("../examples/BPMNEditor-example.xml"))

    def test_loadDiagram(self):
        bpmn_graph = diagram.xml_to_inner(os.path.abspath("../examples/BPMNEditor-example.xml"))
        diagram.export_xml_file(bpmn_graph, "./output.xml")

    def test_loadSignavioDiagram(self):
        bpmn_graph = diagram.xml_to_inner(os.path.abspath("../examples/signavio-example.bpmn"))
        diagram.export_xml_file(bpmn_graph, "./signavio-output.xml")

    def test_loadCamundaDiagram(self):
        bpmn_graph = diagram.xml_to_inner(os.path.abspath("../examples/camunda-example.bpmn"))
        diagram.export_xml_file(bpmn_graph, "./camunda-output.xml")

if __name__ == '__main__':
    unittest.main()
