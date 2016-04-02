import unittest
import bpmn_python.xml_reader
import os
import bpmn_python.bpmn_diagram_rep as diagram

"""
    Put breakpoint on print instruction and use debugger to check objects structure.
"""

class MyTestCase(unittest.TestCase):
    def test_readXmlFile(self):
        domTree = bpmn_python.xml_reader.readXmlFile(os.path.abspath("../examples/BPMNEditor-example.xml"))
        processElement = domTree.getElementsByTagNameNS("*","process")[0]
        diagramElement = domTree.getElementsByTagNameNS("*","BPMNDiagram")[0]
        element = processElement.firstChild;
        print(os.path.abspath("../examples/BPMNEditor-example.xml"))

    def test_loadDiagram(self):
        bpmn_graph = diagram.xml_to_inner(os.path.abspath("../examples/BPMNEditor-example.xml"))
        print(os.path.abspath("../examples/BPMNEditor-example.xml"))

if __name__ == '__main__':
    unittest.main()
