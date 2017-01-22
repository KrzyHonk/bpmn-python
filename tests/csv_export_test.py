# coding=utf-8
"""
Unit tests for exporting process to CSV functionality.
"""

import unittest

import bpmn_python.bpmn_diagram_rep as diagram


class CsvExportTests(unittest.TestCase):
    """
    This class contains test for manual diagram generation functionality.
    """
    output_directory = "./output/test-csv-export/"

    def test_create_simple_diagram_manually(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(start_event_name="Start event")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 1")
        [subprocess1_id, _] = bpmn_graph.add_subprocess_to_diagram(subprocess_name="Subprocess 1")
        [subprocess2_id, _] = bpmn_graph.add_subprocess_to_diagram(subprocess_name="Subprocess 2")
        [task2_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 2")
        [end_id, _] = bpmn_graph.add_end_event_to_diagram(end_event_name="End event")

        bpmn_graph.add_sequence_flow_to_diagram(start_id, task1_id,
                                                sequence_flow_name="start_to_task_one")
        bpmn_graph.add_sequence_flow_to_diagram(task1_id, subprocess1_id,
                                                sequence_flow_name="task_one_to_subprocess_one")
        bpmn_graph.add_sequence_flow_to_diagram(subprocess1_id, subprocess2_id,
                                                sequence_flow_name="subprocess_one_to_subprocess_two")
        bpmn_graph.add_sequence_flow_to_diagram(subprocess2_id, task2_id,
                                                sequence_flow_name="subprocess_two_to_task_two")
        bpmn_graph.add_sequence_flow_to_diagram(task2_id, end_id,
                                                sequence_flow_name="task_two_to_end")

        bpmn_graph.export_csv_file(self.output_directory, "simple_diagram.csv")
        bpmn_graph.export_xml_file(self.output_directory, "simple_diagram.bpmn")

    def test_create_diagram_with_exclusive_parallel_gateway_manually(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(start_event_name="Start event")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 1")

        [exclusive_gate_fork_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(gateway_name="Exclusive gate fork")
        [task2_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 2")
        [task3_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 3")
        [task6_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 6")
        [exclusive_gate_join_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(gateway_name="Exclusive gate join")

        [parallel_gate_fork_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(gateway_name="Parallel gateway fork")
        [task4_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 4")
        [task5_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 5")
        [parallel_gate_join_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(gateway_name="Parallel gateway join")

        [end_id, _] = bpmn_graph.add_end_event_to_diagram(end_event_name="End event")

        bpmn_graph.add_sequence_flow_to_diagram(start_id, task1_id,
                                                sequence_flow_name="Start to one")
        bpmn_graph.add_sequence_flow_to_diagram(task1_id, exclusive_gate_fork_id,
                                                sequence_flow_name="Task one to exclusive fork")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, task2_id,
                                                sequence_flow_name="Exclusive fork to task two")
        bpmn_graph.add_sequence_flow_to_diagram(task2_id, task3_id,
                                                sequence_flow_name="Task two to task three")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, parallel_gate_fork_id,
                                                sequence_flow_name="Exclusive fork to parallel fork")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_fork_id, task4_id,
                                                sequence_flow_name="Parallel fork to task four")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_fork_id, task5_id,
                                                sequence_flow_name="Parallel fork to task five")
        bpmn_graph.add_sequence_flow_to_diagram(task4_id, parallel_gate_join_id,
                                                sequence_flow_name="Task four to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(task5_id, parallel_gate_join_id,
                                                sequence_flow_name="Task five to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_join_id, task6_id,
                                                sequence_flow_name="Parallel join to task six")
        bpmn_graph.add_sequence_flow_to_diagram(task3_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task three to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(task6_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task six to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_join_id, end_id,
                                                sequence_flow_name="Exclusive join to end event")

        bpmn_graph.export_csv_file(self.output_directory, "exclusive_parallel_gateways_diagram.csv")
        bpmn_graph.export_xml_file(self.output_directory, "exclusive_parallel_gateways_diagram.bpmn")

    def test_create_diagram_with_inclusive_parallel_gateway_manually(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(start_event_name="Start event")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 1")

        [exclusive_gate_fork_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(gateway_name="Inclusive gate fork")
        [task2_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 2")
        [task3_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 3")
        [task6_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 6")
        [exclusive_gate_join_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(gateway_name="Inclusive gate join")

        [parallel_gate_fork_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(gateway_name="Parallel gateway fork")
        [task4_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 4")
        [task5_id, _] = bpmn_graph.add_task_to_diagram(task_name="Task 5")
        [parallel_gate_join_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(gateway_name="Parallel gateway join")

        [end_id, _] = bpmn_graph.add_end_event_to_diagram(end_event_name="End event")

        bpmn_graph.add_sequence_flow_to_diagram(start_id, task1_id,
                                                sequence_flow_name="Start to one")
        bpmn_graph.add_sequence_flow_to_diagram(task1_id, exclusive_gate_fork_id,
                                                sequence_flow_name="Task one to exclusive fork")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, task2_id,
                                                sequence_flow_name="Condition: approved")
        bpmn_graph.add_sequence_flow_to_diagram(task2_id, task3_id,
                                                sequence_flow_name="Task two to task three")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, parallel_gate_fork_id,
                                                sequence_flow_name="Condition: rejected")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_fork_id, task4_id,
                                                sequence_flow_name="Parallel fork to task four")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_fork_id, task5_id,
                                                sequence_flow_name="Parallel fork to task five")
        bpmn_graph.add_sequence_flow_to_diagram(task4_id, parallel_gate_join_id,
                                                sequence_flow_name="Task four to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(task5_id, parallel_gate_join_id,
                                                sequence_flow_name="Task five to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_join_id, task6_id,
                                                sequence_flow_name="Parallel join to task six")
        bpmn_graph.add_sequence_flow_to_diagram(task3_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task three to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(task6_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task six to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_join_id, end_id,
                                                sequence_flow_name="Exclusive join to end event")

        bpmn_graph.export_csv_file(self.output_directory, "inclusive_parallel_gateways_diagram.csv")
        bpmn_graph.export_xml_file(self.output_directory, "inclusive_parallel_gateways_diagram.bpmn")


if __name__ == '__main__':
    unittest.main()
