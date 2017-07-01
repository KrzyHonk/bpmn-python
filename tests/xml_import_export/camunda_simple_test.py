# coding=utf-8
"""
Test unit, using simple graph made in bpmn.io editor for import/export operation
"""
import os
import unittest

import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram


class CamundaSimpleTests(unittest.TestCase):
    """
    This class contains test for bpmn-python package functionality using a simple example of BPMN diagram
    created in bpmn-io (Camunda library implementation).
    """
    output_directory = "./output/test-camunda/simple/"
    example_path = "../examples/xml_import_export/camunda_simple_example.bpmn"
    output_file_with_di = "camunda-example-output.xml"
    output_file_no_di = "camunda-example-output-no-di.xml"
    output_dot_file = "camunda-example"
    output_png_file = "camunda-example"

    def test_loadCamundaSimpleDiagram(self):
        """
        Test for importing a simple Camunda diagram example (as BPMN 2.0 XML) into inner representation
        and later exporting it to XML file
        """
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_path))
        bpmn_graph.export_xml_file(self.output_directory, self.output_file_with_di)
        bpmn_graph.export_xml_file_no_di(self.output_directory, self.output_file_no_di)

    def test_loadCamundaSimpleDiagramAndVisualize(self):
        """
        Test for importing a simple Camunda diagram example (as BPMN 2.0 XML) into inner representation
        and later exporting it to XML file. Includes test for visualization functionality.
        """
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_path))
        # Uncomment line below to get a simple view of created diagram
        # visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, self.output_directory + self.output_dot_file)
        visualizer.bpmn_diagram_to_png(bpmn_graph, self.output_directory + self.output_png_file)
        bpmn_graph.export_xml_file(self.output_directory, self.output_file_with_di)
        bpmn_graph.export_xml_file_no_di(self.output_directory, self.output_file_no_di)

if __name__ == '__main__':
    unittest.main()
