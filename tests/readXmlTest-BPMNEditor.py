import unittest
import os

import bpmn_python.bpmn_diagram_rep as diagram
import bpmn_python.bpmn_diagram_visualizer as visualizer

"""
    Put breakpoint on print instruction and use debugger to check objects structure.
"""

class MyTestCase(unittest.TestCase):
    def test_loadDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/BPMNEditor-example.xml"))
        visualizer.visualize_diagram(bpmn_graph)
        bpmn_graph.export_xml_file(bpmn_graph, "./output.xml")

    def test_loadSignavioDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/signavio-example.bpmn"))
        visualizer.visualize_diagram(bpmn_graph)
        bpmn_graph.export_xml_file(bpmn_graph, "./signavio-output.xml")

    def test_loadSignavioComplexDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/signavio-complex-example.bpmn"))
        visualizer.visualize_diagram(bpmn_graph)
        bpmn_graph.export_xml_file(bpmn_graph, "./signavio-complex-output.xml")

    def test_loadCamundaDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/camunda-complex-example.bpmn"))
        visualizer.visualize_diagram(bpmn_graph)
        bpmn_graph.export_xml_file(bpmn_graph, "./camunda-complex-output.xml")

if __name__ == '__main__':
    unittest.main()
