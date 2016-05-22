import unittest
import os

import bpmn_python.bpmn_diagram_rep as diagram
import bpmn_python.bpmn_diagram_visualizer as visualizer

"""
    Put breakpoint on print instruction and use debugger to check objects structure.
"""


class MyTestCase(unittest.TestCase):
    def test_loadBPMNEditorDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/BPMNEditor-example.xml"))
        visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, "BPMNEditor-example")
        bpmn_graph.export_xml_file("./BPMNEditor-example-output.xml")
        bpmn_graph.export_xml_file_no_di("./BPMNEditor-example-output-no-di.xml")

    def test_loadSignavioDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/signavio-example.bpmn"))
        visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, "signavio-example")
        bpmn_graph.export_xml_file("./signavio-example-output.xml")
        bpmn_graph.export_xml_file_no_di("./signavio-example-output-no-di.xml")

    def test_loadSignavioComplexDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/signavio-complex-example.bpmn"))
        visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, "signavio-complex-example")
        bpmn_graph.export_xml_file("./signavio-complex-example-output.xml")
        bpmn_graph.export_xml_file_no_di("./signavio-complex-example-output-no-di.xml")

    def test_loadCamundaDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/camunda-example.bpmn"))
        visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, "camunda-example")
        bpmn_graph.export_xml_file("./camunda-example-output.xml")
        bpmn_graph.export_xml_file_no_di("./camunda-example-output-no-di.xml")

    def test_loadCamundaComplexDiagram(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/camunda-complex-example.bpmn"))
        visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, "camunda-complex-example")
        bpmn_graph.export_xml_file("./camunda-complex-example-output.xml")
        bpmn_graph.export_xml_file_no_di("./camunda-complex-example-output-no-di.xml")

    def test_get_all_nodes_edges(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.load_diagram_from_xml(os.path.abspath("../examples/BPMNEditor-example.xml"))
        all_nodes = bpmn_graph.get_nodes()
        task_nodes = bpmn_graph.get_nodes("task")
        all_edges = bpmn_graph.get_edges()
        edge = bpmn_graph.get_edge_by_id("sequenceFlow_7")
        assert len(all_nodes) == 8
        assert len(task_nodes) == 4
        assert len(all_edges) == 8

    def test_create_diagram_manually(self):
        bpmn_graph = diagram.BPMNDiagramGraph()
        bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
        [start_id, _] = bpmn_graph.add_start_event_to_diagram(start_event_name="start_event")
        [end_id, _] = bpmn_graph.add_end_event_to_diagram(end_event_name="end_event")
        [task1_id, _] = bpmn_graph.add_task_to_diagram(task_name="task1")
        [task2_id, _] = bpmn_graph.add_task_to_diagram(task_name="task2")

        [parallel_gate_fork_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(gateway_name="parallel_gate_fork")
        [task1_par_id, _] = bpmn_graph.add_task_to_diagram(task_name="task1_par")
        [task2_par_id, _] = bpmn_graph.add_task_to_diagram(task_name="task2_par")
        [parallel_gate_join_id, _] = bpmn_graph.add_parallel_gateway_to_diagram(gateway_name="parallel_gate_join")

        [exclusive_gate_fork_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(gateway_name="exclusive_gate_fork")
        [task1_ex_id, _] = bpmn_graph.add_task_to_diagram(task_name="task1_ex")
        [task2_ex_id, _] = bpmn_graph.add_task_to_diagram(task_name="task2_ex")
        [exclusive_gate_join_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(gateway_name="exclusive_gate_join")

        # [inclusive_gate_fork_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(gateway_name="inclusive_gate_fork")
        # [task1_in_id, _] = bpmn_graph.add_task_to_diagram(task_name="task1_in")
        # [task2_in_id, _] = bpmn_graph.add_task_to_diagram(task_name="task2_in")
        # [inclusive_gate_join_id, _] = bpmn_graph.add_inclusive_gateway_to_diagram(gateway_name="inclusive_gate_join")

        bpmn_graph.add_sequence_flow_to_diagram(start_id, task1_id, "start_to_one")

        bpmn_graph.add_sequence_flow_to_diagram(task1_id, parallel_gate_fork_id, "one_to_par_fork")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_fork_id, task1_par_id, "par_fork_to_par_one")
        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_fork_id, task2_par_id, "par_fork_to_par_two")
        bpmn_graph.add_sequence_flow_to_diagram(task1_par_id, parallel_gate_join_id, "par_one_to_par_join")
        bpmn_graph.add_sequence_flow_to_diagram(task2_par_id, parallel_gate_join_id, "par_two_to_par_join")

        bpmn_graph.add_sequence_flow_to_diagram(parallel_gate_join_id, exclusive_gate_fork_id, "par_join_to_ex_fork")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, task1_ex_id, "ex_fork_to_ex_one")
        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_fork_id, task2_ex_id, "ex_fork_to_ex_two")
        bpmn_graph.add_sequence_flow_to_diagram(task1_ex_id, exclusive_gate_join_id, "ex_one_to_ex_join")
        bpmn_graph.add_sequence_flow_to_diagram(task2_ex_id, exclusive_gate_join_id, "ex_two_to_ex_join")

        # BPMNEditor doesn't handle inclusiveGateway, so we can't test this fully. Method seems to be corret.
        # bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_join_id, inclusive_gate_fork_id, "ex_join_to_in_fork")
        # bpmn_graph.add_sequence_flow_to_diagram(inclusive_gate_fork_id, task1_in_id, "in_fork_to_in_one")
        # bpmn_graph.add_sequence_flow_to_diagram(inclusive_gate_fork_id, task2_in_id, "in_fork_to_in_two")
        # bpmn_graph.add_sequence_flow_to_diagram(task1_in_id, inclusive_gate_join_id, "in_one_to_in_join")
        # bpmn_graph.add_sequence_flow_to_diagram(task2_in_id, inclusive_gate_join_id, "in_two_to_in_join")

        bpmn_graph.add_sequence_flow_to_diagram(exclusive_gate_join_id, task2_id, "ex_join_to_two")
        bpmn_graph.add_sequence_flow_to_diagram(task2_id, end_id, "two_to_end")

        bpmn_graph.export_xml_file("./manually-created-output.bpmn")
        bpmn_graph.export_xml_file_no_di("./manually-created-output-no-di.bpmn")
        visualizer.visualize_diagram(bpmn_graph)
        visualizer.bpmn_diagram_to_dot_file(bpmn_graph, "manually-created")

if __name__ == '__main__':
    unittest.main()
