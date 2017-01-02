# coding=utf-8
"""
Layout metrics computing tests
"""
import unittest
import os

import bpmn_python.diagram_layout_metrics as metrics
import bpmn_python.bpmn_diagram_rep as diagram


class MetricsTests(unittest.TestCase):
    """
    """
    output_directory = "./output/test-bpmneditor/"
    crossing_points_example_path = "../examples/crossing_point_test.bpmn"
    cycles_example_path = "../examples/cycles_test.bpmn"

    def load_example_diagram(self, filepath):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath(filepath))
        return bpmn_graph

    def test_count_crossing_points(self):
        bpmn_graph = MetricsTests.load_example_diagram(self, self.crossing_points_example_path)
        cross_points = metrics.count_crossing_points(bpmn_graph)
        self.assertEqual(cross_points, 6, "Crossing points count does not match")

    def test_count_segments(self):
        bpmn_graph = MetricsTests.load_example_diagram(self, self.crossing_points_example_path)
        segments_count = metrics.count_segments(bpmn_graph)
        self.assertEqual(segments_count, 25, "Segments count does not match")

    def test_compute_longest_path(self):
        bpmn_graph = MetricsTests.load_example_diagram(self, self.cycles_example_path)
        (longest_path, longest_path_len) = metrics.compute_longest_path(bpmn_graph)
        self.assertEqual(longest_path_len, 9, "Path length does not match")


if __name__ == '__main__':
    unittest.main()
