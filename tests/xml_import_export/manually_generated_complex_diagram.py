# coding=utf-8
"""
Test unit, creates a more complex graph using functions provided by package and exports it to XML and graphic format
"""
import unittest

import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram


class ManualGenerationComplexTests(unittest.TestCase):
    """
    This class contains test for manual diagram generation functionality.
    """
    output_directory = "./output/test-manual/complex/"
    output_file_with_di = "manually-generated-complex-output.xml"
    output_file_no_di = "manually-generated-complex-output-no-di.xml"
    output_dot_file = "manually-generated-example"
    output_png_file = "manually-generated-example"

    def test_create_diagram_manually(self):
        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        process_id = bpmn_graph.add_process_to_diagram()

        [start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="start_event")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="First task")
        [subprocess1_id, _] = bpmn_graph.add_subprocess_to_diagram(process_id, subprocess_name="Subprocess")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, subprocess1_id)

        [parallel_gate_fork_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
                                                                                gateway_name="parallel_gate_fork")
        [task1_par_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1_par")
        [task2_par_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2_par")
        [parallel_gate_join_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(process_id,
                                                                                gateway_name="parallel_gate_join")

        bpmn_graph.add_sequence_flow_to_diagram(process_id, subprocess1_id, parallel_gate_fork_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_fork_id, task1_par_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_fork_id, task2_par_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_par_id, parallel_gate_join_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_par_id, parallel_gate_join_id)

        [exclusive_gate_fork_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="exclusive_gate_fork")
        [task1_ex_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1_ex")
        [task2_ex_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2_ex")
        [exclusive_gate_join_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="exclusive_gate_join")

        bpmn_graph.add_sequence_flow_to_diagram(process_id, parallel_gate_join_id, exclusive_gate_fork_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task1_ex_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task2_ex_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_ex_id, exclusive_gate_join_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_ex_id, exclusive_gate_join_id)

        [inclusive_gate_fork_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="inclusive_gate_fork")
        [task1_in_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1_in")
        [task2_in_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2_in")
        [inclusive_gate_join_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(process_id,
                                                                                  gateway_name="inclusive_gate_join")

        bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_join_id, inclusive_gate_fork_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, inclusive_gate_fork_id, task1_in_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, inclusive_gate_fork_id, task2_in_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_in_id, inclusive_gate_join_id)
        bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_in_id, inclusive_gate_join_id)

        [end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="end_event")
        bpmn_graph.add_sequence_flow_to_diagram(process_id, inclusive_gate_join_id, end_id)

        layouter.generate_layout(bpmn_graph)

        bpmn_graph.export_xml_file(self.output_directory, self.output_file_with_di)
        bpmn_graph.export_xml_file_no_di(self.output_directory, self.output_file_no_di)
        # Uncomment line below to get a simple view of created diagram
        # visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, self.output_directory + self.output_dot_file)
        visualizer.bpmn_diagram_to_png(bpmn_graph, self.output_directory + self.output_png_file)

if __name__ == '__main__':
    unittest.main()
