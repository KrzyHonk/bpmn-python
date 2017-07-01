# coding=utf-8
"""
Test unit, using simple graph made in Signavio editor for import/export operation
"""
import os
import unittest

import bpmn_python.bpmn_diagram_rep as diagram


class BPMNEditorTests(unittest.TestCase):
    """
    This class contains test for bpmn-python package functionality using an example BPMN diagram, which contains
    multiple pool and lane elements.
    """
    output_directory = "./output/test-lane/"
    example_path = "../examples/xml_import_export/lanes.bpmn"
    output_file_with_di = "lanes-example-output.xml"
    output_file_no_di = "lanes-example-output-no-di.xml"

    def test_load_lanes_example(self):
        """
        Test for importing a simple BPMNEditor diagram example (as BPMN 2.0 XML) into inner representation
        and later exporting it to XML file
        """
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_path))
        bpmn_graph.export_xml_file(self.output_directory, self.output_file_with_di)
        bpmn_graph.export_xml_file_no_di(self.output_directory, self.output_file_no_di)

if __name__ == '__main__':
    unittest.main()
