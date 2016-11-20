# coding=utf-8
"""
Test unit, using simple graph made in BPMNEditor editor for import/export operation
"""
import unittest
import os

import bpmn_python.bpmn_diagram_rep as diagram
import bpmn_python.bpmn_diagram_layouter as layouter


class BPMNEditorTests(unittest.TestCase):
    """
    This class contains test for bpmn-python package functionality using an example BPMN diagram created in BPMNEditor.
    """

    def test_layouter_manually_created_diagram(self):
        """
        Test for importing a simple BPMNEditor diagram example (as BPMN 2.0 XML) into inner representation
        and generating layout for it
        """
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

        layouter.BpmnDiagramLayouter.generate_layout(bpmn_graph)

    def test_load_bpmn_editor_diagram(self):
        """
        Test for importing a simple BPMNEditor diagram example (as BPMN 2.0 XML) into inner representation
        and generating layout for it
        """
        output_directory = "./output/test-bpmneditor/"
        example_directory = "../examples/BPMNEditor-simple-example.xml"
        output_file_with_di = "BPMNEditor-example-output.xml"
        output_file_no_di = "BPMNEditor-example-output-no-di.xml"

        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath(example_directory))
        bpmn_graph.export_xml_file(output_directory, output_file_with_di)
        bpmn_graph.export_xml_file_no_di(output_directory, output_file_no_di)

        layouter.BpmnDiagramLayouter.generate_layout(bpmn_graph)

    def test_load_camunda_simple_diagram(self):
        """
        Test for importing a simple Camunda diagram example (as BPMN 2.0 XML) into inner representation
        and later exporting it to XML file
        """

        output_directory = "./output/test-camunda/simple/"
        example_directory = "../examples/camunda-simple-example.bpmn"
        output_file_with_di = "camunda-example-output.xml"
        output_file_no_di = "camunda-example-output-no-di.xml"

        bpmn_graph = diagram.BpmnDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath(example_directory))
        bpmn_graph.export_xml_file(output_directory, output_file_with_di)
        bpmn_graph.export_xml_file_no_di(output_directory, output_file_no_di)

        layouter.BpmnDiagramLayouter.generate_layout(bpmn_graph)

if __name__ == '__main__':
    unittest.main()
