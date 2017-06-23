# coding=utf-8
"""
Unit tests for exporting process to CSV functionality.
"""

import os
import unittest

import bpmn_python.bpmn_diagram_rep as diagram


class CsvExportTests(unittest.TestCase):
    """
    This class contains test for manual diagram generation functionality.
    """
    output_directory = "./output/test-csv-export/"
    example_directory = "../examples/csv_export/"

    def test_csv_export_bank_account_example(self):
        # TODO not working correctly, problem with nested splits
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_directory + "bank-account-process.bpmn"))
        bpmn_graph.export_csv_file(self.output_directory, "bank-account-process.csv")

    def test_csv_export_checkin_process_example(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_directory + "checkin-process.bpmn"))
        bpmn_graph.export_csv_file(self.output_directory, "checkin-process.csv")

    def test_csv_export_credit_process_example(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_directory + "credit-process.bpmn"))
        bpmn_graph.export_csv_file(self.output_directory, "credit-process.csv")

    def test_csv_export_order_processing_example(self):
        # TODO not working correctly, problem with nested splits
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_directory + "order-processing.bpmn"))
        bpmn_graph.export_csv_file(self.output_directory, "order-processing.csv")

    def test_csv_export_pizza_order_example(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_directory + "pizza-order.bpmn"))
        bpmn_graph.export_csv_file(self.output_directory, "pizza-order.csv")

    def test_csv_export_tram_process_example(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml_file(os.path.abspath(self.example_directory + "tram-process.bpmn"))
        # TODO Problem with the loops
        #bpmn_graph.export_csv_file(self.output_directory, "tram-process.csv")

    def test_csv_export_manual_simple_diagram(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        process_id = bpmn_graph.add_process_to_diagram()
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="Start event",
                                                              start_event_definition="timer")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 1")
        [subprocess1_id, _] = bpmn_graph.add_subprocess_to_diagram(process_id, subprocess_name="Subprocess 1")
        [subprocess2_id, _] = bpmn_graph.add_subprocess_to_diagram(process_id, subprocess_name="Subprocess 2")
        [task2_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 2")
        [end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="End event",
                                                          end_event_definition="message")

        bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id,
                                                sequence_flow_name="start_to_task_one")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, subprocess1_id,
                                                sequence_flow_name="task_one_to_subprocess_one")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, subprocess1_id, subprocess2_id,
                                                sequence_flow_name="subprocess_one_to_subprocess_two")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, subprocess2_id, task2_id,
                                                sequence_flow_name="subprocess_two_to_task_two")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_id, end_id,
                                                sequence_flow_name="task_two_to_end")

        bpmn_graph.export_csv_file(self.output_directory, "simple_diagram.csv")
        bpmn_graph.export_xml_file(self.output_directory, "simple_diagram.bpmn")

    def test_csv_export_diagram_with_exclusive_parallel_gateway(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        process_id = bpmn_graph.add_process_to_diagram()
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="Start event",
                                                              start_event_definition="timer")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 1")

        [exclusive_gate_fork_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="Exclusive gate fork")
        [task2_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 2")
        [task3_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 3")
        [task6_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 6")
        [exclusive_gate_join_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="Exclusive gate join")

        [parallel_gate_fork_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
                                                                                gateway_name="Parallel gateway fork")
        [task4_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 4")
        [task5_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 5")
        [parallel_gate_join_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
                                                                                gateway_name="Parallel gateway join")

        [end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="End event",
                                                          end_event_definition="message")

        bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id,
                                                sequence_flow_name="Start to one")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, exclusive_gate_fork_id,
                                                sequence_flow_name="Task one to exclusive fork")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task2_id,
                                                sequence_flow_name="Exclusive fork to task two")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_id, task3_id,
                                                sequence_flow_name="Task two to task three")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, parallel_gate_fork_id,
                                                sequence_flow_name="Exclusive fork to parallel fork")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_fork_id, task4_id,
                                                sequence_flow_name="Parallel fork to task four")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_fork_id, task5_id,
                                                sequence_flow_name="Parallel fork to task five")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task4_id, parallel_gate_join_id,
                                                sequence_flow_name="Task four to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task5_id, parallel_gate_join_id,
                                                sequence_flow_name="Task five to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_join_id, task6_id,
                                                sequence_flow_name="Parallel join to task six")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task3_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task three to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task6_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task six to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_join_id, end_id,
                                                sequence_flow_name="Exclusive join to end event")

        bpmn_graph.export_csv_file(self.output_directory, "exclusive_parallel_gateways_diagram.csv")
        bpmn_graph.export_xml_file(self.output_directory, "exclusive_parallel_gateways_diagram.bpmn")

    def test_csv_export_diagram_with_inclusive_parallel_gateway(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        process_id = bpmn_graph.add_process_to_diagram()
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="Start event",
                                                              start_event_definition="timer")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 1")

        [exclusive_gate_fork_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="Inclusive gate fork")
        [task2_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 2")
        [task3_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 3")
        [task6_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 6")
        [exclusive_gate_join_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="Inclusive gate join")

        [parallel_gate_fork_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
                                                                                gateway_name="Parallel gateway fork")
        [task4_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 4")
        [task5_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="Task 5")
        [parallel_gate_join_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
                                                                                gateway_name="Parallel gateway join")

        [end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="End event",
                                                          end_event_definition="message")

        bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id,
                                                sequence_flow_name="Start to one")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, exclusive_gate_fork_id,
                                                sequence_flow_name="Task one to exclusive fork")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task2_id,
                                                sequence_flow_name="Condition: approved")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_id, task3_id,
                                                sequence_flow_name="Task two to task three")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, parallel_gate_fork_id,
                                                sequence_flow_name="Condition: rejected")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_fork_id, task4_id,
                                                sequence_flow_name="Parallel fork to task four")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_fork_id, task5_id,
                                                sequence_flow_name="Parallel fork to task five")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task4_id, parallel_gate_join_id,
                                                sequence_flow_name="Task four to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task5_id, parallel_gate_join_id,
                                                sequence_flow_name="Task five to parallel join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_join_id, task6_id,
                                                sequence_flow_name="Parallel join to task six")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task3_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task three to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task6_id, exclusive_gate_join_id,
                                                sequence_flow_name="Task six to exclusive join")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_join_id, end_id,
                                                sequence_flow_name="Exclusive join to end event")

        bpmn_graph.export_csv_file(self.output_directory, "inclusive_parallel_gateways_diagram.csv")
        bpmn_graph.export_xml_file(self.output_directory, "inclusive_parallel_gateways_diagram.bpmn")


if __name__ == '__main__':
    unittest.main()
