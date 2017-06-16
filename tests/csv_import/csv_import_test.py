# coding=utf-8
"""
Unit tests for exporting process to CSV functionality.
"""

import os
import unittest

import bpmn_python.graph.bpmn_diagram_rep as diagram


class CsvExportTests(unittest.TestCase):
    """
    This class contains test for manual diagram generation functionality.
    """
    output_directory = "./output/test-csv-import/"
    example_directory = "../examples/csv_import/"

    def test_csv_export_bank_account_example(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_csv_file(os.path.abspath(self.example_directory + "pizza-order.csv"))
        # bpmn_graph.export_csv_file(self.output_directory, "pizza-order-export.csv")


if __name__ == '__main__':
    unittest.main()
