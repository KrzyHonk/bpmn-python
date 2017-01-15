# coding=utf-8

import unittest

import bpmn_python.bpmn_diagram_rep as diagram
import bpmn_process_csv_export as csv_export


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

        bpmn_graph.add_sequence_flow_to_diagram(start_id, task1_id, sequence_flow_name="start_to_task_one")
        bpmn_graph.add_sequence_flow_to_diagram(task1_id, subprocess1_id, sequence_flow_name="task_one_to_subprocess_one")
        bpmn_graph.add_sequence_flow_to_diagram(subprocess1_id, subprocess2_id, sequence_flow_name="subprocess_one_to_subprocess_two")
        bpmn_graph.add_sequence_flow_to_diagram(subprocess2_id, task2_id, sequence_flow_name="subprocess_two_to_task_two")
        bpmn_graph.add_sequence_flow_to_diagram(task2_id, end_id, sequence_flow_name="task_two_to_end")

        bpmn_graph.export_csv_file(self.output_directory, "simple_diagram.csv")

    def test_create__diagram_manually(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(start_event_name="start_event")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(task_name="task1")
        bpmn_graph.add_sequence_flow_to_diagram(start_id, task1_id, "start_to_one")

        [exclusive_gate_fork_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(gateway_name="exclusive_gate_fork")
        [task1_ex_id, _] = bpmn_graph.add_task_to_diagram(task_name="task1_ex")
        [task2_ex_id, _] = bpmn_graph.add_task_to_diagram(task_name="task2_ex")
        [exclusive_gate_join_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(gateway_name="exclusive_gate_join")

        bpmn_graph.add_sequence_flow_to_diagram(task1_id, exclusive_gate_fork_id, "one_to_ex_fork")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, task1_ex_id, "ex_fork_to_ex_one")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, task2_ex_id, "ex_fork_to_ex_two")
        bpmn_graph.add_sequence_flow_to_diagram(task1_ex_id, exclusive_gate_join_id, "ex_one_to_ex_join")
        bpmn_graph.add_sequence_flow_to_diagram(task2_ex_id, exclusive_gate_join_id, "ex_two_to_ex_join")

        [task2_id, _] = bpmn_graph.add_task_to_diagram(task_name="task2")
        [end_id, _] = bpmn_graph.add_end_event_to_diagram(end_event_name="end_event")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_join_id, task2_id, "ex_join_to_two")
        bpmn_graph.add_sequence_flow_to_diagram(task2_id, end_id, "two_to_end")
        bpmn_graph.export_csv_file(self.output_directory, "simple_diagram.csv")

if __name__ == '__main__':
    unittest.main()
