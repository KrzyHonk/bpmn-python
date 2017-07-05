# coding=utf-8
"""
Test unit, using simple graph made in Signavio editor for import/export operation
"""
import os
import unittest

import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram


class SignavioSimpleTests(unittest.TestCase):
    """
    This class contains test for bpmn-python package functionality using a simple example of BPMN diagram
    created in Signavio Editor.
    """
    output_directory = "./output/test-signavio/simple/"
    example_path = "../examples/xml_import_export/signavio_simple_example.bpmn"
    output_file_with_di = "signavio-example-output.xml"
    output_file_no_di = "signavio-example-output-no-di.xml"
    output_dot_file = "signavio-example"
    output_png_file = "signavio-example"

    def test_loadSignavioSimpleDiagram(self):
        """
        Test for importing a simple Signavio diagram example (as BPMN 2.0 XML) into inner representation
        and later exporting it to XML file
        """
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_path))
        bpmn_graph.export_xml_file(self.output_directory, self.output_file_with_di)
        bpmn_graph.export_xml_file_no_di(self.output_directory, self.output_file_no_di)

    def test_loadSignavioSimpleDiagramAndVisualize(self):
        """
        Test for importing a simple Signavio diagram example (as BPMN 2.0 XML) into inner representation
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
