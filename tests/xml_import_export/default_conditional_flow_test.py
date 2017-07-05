# coding=utf-8
"""
Test unit, using simple graph made in BPMNEditor editor for import/export operation
"""
import os
import unittest

import bpmn_python.bpmn_diagram_rep as diagram


class DefaultConditionalFlowTests(unittest.TestCase):
    """
    This class contains test for bpmn-python package functionality using an example BPMN diagram created in BPMNEditor.
    """
    output_directory = "./output/test-flows/"
    example_path = "../examples/xml_import_export/default-conditional-flow-example.bpmn"
    output_file = "default-conditional-flow-example.bpmn"

    def test_loadBPMNEditorDiagramAndVisualize(self):
        """
        Test for importing a simple BPMNEditor diagram example (as BPMN 2.0 XML) into inner representation
        and later exporting it to XML file. Includes test for visualization functionality.
        """
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_path))
        bpmn_graph.export_xml_file(self.output_directory, self.output_file)

if __name__ == '__main__':
    unittest.main()
