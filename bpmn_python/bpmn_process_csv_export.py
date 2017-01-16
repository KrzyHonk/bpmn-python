# coding=utf-8
"""
"""
from __future__ import print_function

import copy
import errno
import os

import bpmn_diagram_exception as bpmn_exception


class BpmnDiagramGraphCsvExport:
    # TODO
    # TODO need to add support for lanes in import/export. After that, read user and pass it as 'who'
    """

    """
    gateways_list = ["exclusiveGateway", "inclusiveGateway", "parallelGateway"]
    tasks_list = ["task", "subProcess"]
    '''
    Supported start event types: normal, timer, message.
    Supported end event types: normal, message.
    '''
    events_list = ["startEvent", "endEvent"]
    lanes_list = ["process", "laneSet", "lane"]

    def __init__(self):
        pass

    @staticmethod
    def export_process_to_csv(bpmn_diagram, directory, filename):
        """
        Adds Task node attributes to exported XML element

        :param node_params: dictionary with given task parameters,
        :param output_element: object representing BPMN XML 'task' element.
        """
        incoming_flows_list_param_name = "incoming"
        nodes = copy.deepcopy(bpmn_diagram.get_nodes())
        start_nodes = []
        export_elements = []

        for node in nodes:
            incoming_list = node[1][incoming_flows_list_param_name]
            if len(incoming_list) == 0:
                start_nodes.append(node)
        if len(start_nodes) != 1:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format accepts only one start event")

        start_node = start_nodes.pop()
        nodes.remove(start_node)
        BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, start_node, order=0, prefix="",
                                              condition="",
                                              who="")

        try:
            os.makedirs(directory)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        file_object = open(directory + filename, "w")
        file_object.write("Order,Activity,Condition,Who,Subprocess,Terminated\n")
        BpmnDiagramGraphCsvExport.write_export_node_to_file(file_object, export_elements)
        file_object.close()

    @staticmethod
    def export_node(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        node_type = node[1]["type"]
        if node_type == "task":
            BpmnDiagramGraphCsvExport.export_task(bpmn_diagram, export_elements, node, order=order, prefix=prefix,
                                                  who=who)
        elif node_type == "subProcess":
            BpmnDiagramGraphCsvExport.export_sub_process(bpmn_diagram, export_elements, node, order=order,
                                                         prefix=prefix, who=who)
        elif node_type == "inclusiveGateway":
            BpmnDiagramGraphCsvExport.export_inclusive_gateway(bpmn_diagram, export_elements, node, order=order,
                                                               prefix=prefix, condition=condition, who=who)
        elif node_type == "exclusiveGateway":
            BpmnDiagramGraphCsvExport.export_exclusive_gateway(bpmn_diagram, export_elements, node, order=order,
                                                               prefix=prefix, condition=condition, who=who)
        elif node_type == "parallelGateway":
            BpmnDiagramGraphCsvExport.export_parallel_gateway(bpmn_diagram, export_elements, node, order=order,
                                                              prefix=prefix, condition=condition, who=who)
        elif node_type == "startEvent":
            BpmnDiagramGraphCsvExport.export_start_event(bpmn_diagram, export_elements, node, order=order,
                                                         prefix=prefix, who=who)
        elif node_type == "endEvent":
            BpmnDiagramGraphCsvExport.export_end_event(bpmn_diagram, export_elements, node, order=order, prefix=prefix,
                                                       who=who)

    @staticmethod
    def export_task(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        export_elements.append({"Order": prefix + str(order), "Activity": node[1]["node_name"],
                                "Condition": condition, "Who": who, "Subprocess": "", "Terminated": ""})
        outgoing_flow_id = node[1]["outgoing"][0]
        outgoing_flow = bpmn_diagram.get_flow_by_id(outgoing_flow_id)
        outgoing_node = bpmn_diagram.get_node_by_id(outgoing_flow[2]["target_id"])
        BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node, order + 1, prefix, who)

    @staticmethod
    def export_sub_process(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        export_elements.append({"Order": prefix + str(order), "Activity": node[1]["node_name"],
                                "Condition": condition, "Who": who, "Subprocess": "yes", "Terminated": ""})
        outgoing_flow_id = node[1]["outgoing"][0]
        outgoing_flow = bpmn_diagram.get_flow_by_id(outgoing_flow_id)
        outgoing_node = bpmn_diagram.get_node_by_id(outgoing_flow[2]["target_id"])
        BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node, order + 1, prefix, "", who)

    @staticmethod
    def export_inclusive_gateway(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        # TODO need to add support for conditions in import/export
        pass

    @staticmethod
    def export_exclusive_gateway(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        outgoing_flows = node[1]["outgoing"]
        if len(outgoing_flows) == 1:
            outgoing_flow_id = outgoing_flows[0]
            outgoing_flow = bpmn_diagram.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_diagram.get_node_by_id(outgoing_flow[2]["target_id"])
            prefix_a = prefix + str(order)
            BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node, order, prefix_a,
                                                  condition, who)
        elif len(outgoing_flows) == 2:
            outgoing_flow_id_a = outgoing_flows[0]
            outgoing_flow_a = bpmn_diagram.get_flow_by_id(outgoing_flow_id_a)
            outgoing_node_a = bpmn_diagram.get_node_by_id(outgoing_flow_a[2]["target_id"])
            prefix_a = prefix + str(order) + 'a'
            BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node_a, 1, prefix_a,
                                                  condition, who)

            outgoing_flow_id_b = outgoing_flows[1]
            outgoing_flow_b = bpmn_diagram.get_flow_by_id(outgoing_flow_id_b)
            outgoing_node_b = bpmn_diagram.get_node_by_id(outgoing_flow_b[2]["target_id"])
            prefix_b = prefix + str(order) + 'b'
            BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node_b, 1, prefix_b,
                                                  "else", who)
        else:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format: gateways must have 1 or 2 outgoing flows")

    @staticmethod
    def export_parallel_gateway(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        outgoing_flows = node[1]["outgoing"]
        if len(outgoing_flows) == 1:
            outgoing_flow_id = outgoing_flows[0]
            outgoing_flow = bpmn_diagram.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_diagram.get_node_by_id(outgoing_flow[2]["target_id"])
            prefix_a = prefix + str(order)
            BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node, order, prefix_a,
                                                  condition, who)
        elif len(outgoing_flows) == 2:
            outgoing_flow_id_a = outgoing_flows[0]
            outgoing_flow_a = bpmn_diagram.get_flow_by_id(outgoing_flow_id_a)
            outgoing_node_a = bpmn_diagram.get_node_by_id(outgoing_flow_a[2]["target_id"])
            prefix_a = prefix + str(order) + 'a'
            BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node_a, order, prefix_a,
                                                  condition, who)

            outgoing_flow_id_b = outgoing_flows[1]
            outgoing_flow_b = bpmn_diagram.get_flow_by_id(outgoing_flow_id_b)
            outgoing_node_b = bpmn_diagram.get_node_by_id(outgoing_flow_b[2]["target_id"])
            prefix_b = prefix + str(order) + 'b'
            BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node_b, order, prefix_b,
                                                  "", who)
        else:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format: gateways must have 1 or 2 outgoing flows")

    @staticmethod
    def export_start_event(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        export_elements.append({"Order": prefix + str(order), "Activity": node[1]["node_name"],
                                "Condition": condition, "Who": who, "Subprocess": "", "Terminated": ""})
        outgoing_flow_id = node[1]["outgoing"][0]
        outgoing_flow = bpmn_diagram.get_flow_by_id(outgoing_flow_id)
        outgoing_node = bpmn_diagram.get_node_by_id(outgoing_flow[2]["target_id"])
        BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, outgoing_node, order + 1, prefix, who)

    @staticmethod
    def export_end_event(bpmn_diagram, export_elements, node, order=0, prefix="", condition="", who=""):
        export_elements.append({"Order": prefix + str(order), "Activity": node[1]["node_name"],
                                "Condition": condition, "Who": who, "Subprocess": "", "Terminated": "yes"})

    @staticmethod
    def write_export_node_to_file(file_object, export_elements):
        for export_element in export_elements:
            # Order,Activity,Condition,Who,Subprocess,Terminated
            # export_element = export_elements[export_element_key]
            file_object.write(
                export_element["Order"] + "," + export_element["Activity"] + "," + export_element["Condition"] + "," +
                export_element["Who"] + "," + export_element["Subprocess"] + "," + export_element["Terminated"] + "\n")
