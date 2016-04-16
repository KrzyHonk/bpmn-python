import unittest
import os

import bpmn_python.bpmn_diagram_rep as diagram
import bpmn_python.bpmn_diagram_visualizer as visualizer

"""
    Put breakpoint on print instruction and use debugger to check objects structure.
"""

class MyTestCase(unittest.TestCase):
    def test_loadBPMNEditorDiagram(self):
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

    def test_get_all_nodes_edges(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/BPMNEditor-example.xml"))
        all_nodes = bpmn_graph.get_nodes()
        task_nodes = bpmn_graph.get_nodes("task")
        all_edges = bpmn_graph.get_edges()
        edge = bpmn_graph.get_edge_by_id("sequenceFlow_7")
        assert len(all_nodes) == 8
        assert len(task_nodes) == 4
        assert len(all_edges) == 8
        assert edge[0] == "task_4"
        assert edge[1] == "xor_2"

if __name__ == '__main__':
    unittest.main()
