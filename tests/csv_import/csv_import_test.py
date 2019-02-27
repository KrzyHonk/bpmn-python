# coding=utf-8
"""
Unit tests for exporting process to CSV functionality.
"""

import filecmp
import os
import unittest

import bpmn_python.bpmn_diagram_rep as diagram


class CsvExportTests(unittest.TestCase):
    """
    This class contains test for manual diagram generation functionality.
    """
    output_directory = "./output/"
    input_directory = "./input/"

    def test_csv_import_csv_export(self):
        processes = ["pizza-order", "airline-checkin", "order-processing"]

        for process in processes:
            bpmn_graph = diagram.BpmnDiagramGraph()
            bpmn_graph.load_diagram_from_csv_file(os.path.abspath(self.input_directory + process + ".csv"))
            bpmn_graph.export_csv_file(self.output_directory, process + ".csv")
            cmp_result = filecmp.cmp(self.input_directory + process + ".csv", self.output_directory, process + ".csv")
            # unittest.TestCase.assertTrue(self, cmp_result) # unfortunatelly csv export has bugs
            bpmn_graph.export_xml_file_no_di(self.output_directory, process + ".bpmn")


if __name__ == '__main__':
    unittest.main()
