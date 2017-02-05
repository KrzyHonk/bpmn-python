# coding=utf-8
"""
Implementation of exporting process to CSV functionality, as proposed in article "Spreadsheet-Based Business
Process Modeling" by Kluza k. and Wisniewski P.
"""
from __future__ import print_function

import copy
import errno
import os
import string

import bpmn_diagram_exception as bpmn_exception
import bpmn_python.bmpn_python_consts as consts


class BpmnDiagramGraphCsvExport:
    # TODO need to add support for lanes in import/export. After that, read user and add 'who' param
    # TODO Drop the assumption that gateway has only two outgoing flows
    # increase it to the size of alphabet - should be enough for normal users
    """
    Class that provides implementation of exporting process to CSV functionality
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
    def export_process_to_csv(bpmn_graph, directory, filename):
        """
        Root method of CSV export functionality.
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param directory: a string object, which is a path of output directory,
        :param filename: a string object, which is a name of output file.
        """
        nodes = copy.deepcopy(bpmn_graph.get_nodes())
        start_nodes = []
        export_elements = []

        for node in nodes:
            incoming_list = node[1][consts.Consts.incoming_flows]
            if len(incoming_list) == 0:
                start_nodes.append(node)
        if len(start_nodes) != 1:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format accepts only one start event")

        start_node = start_nodes.pop()
        nodes.remove(start_node)
        BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, start_node, order=0, prefix="",
                                              condition="", who="")

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
    def export_node(bpmn_graph, export_elements, node, order=0, prefix="", condition="", who=""):
        """
        General method for node exporting
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """
        node_type = node[1][consts.Consts.type]
        if node_type == consts.Consts.task:
            return BpmnDiagramGraphCsvExport.export_task(bpmn_graph, export_elements, node, order=order,
                                                         prefix=prefix, condition=condition, who=who)
        elif node_type == consts.Consts.subprocess:
            return BpmnDiagramGraphCsvExport.export_sub_process(bpmn_graph, export_elements, node, order=order,
                                                                prefix=prefix, condition=condition, who=who)
        elif node_type == consts.Consts.inclusive_gateway:
            return BpmnDiagramGraphCsvExport.export_inclusive_gateway(bpmn_graph, export_elements, node, order=order,
                                                                      prefix=prefix, who=who)
        elif node_type == consts.Consts.exclusive_gateway:
            return BpmnDiagramGraphCsvExport.export_exclusive_gateway(bpmn_graph, export_elements, node, order=order,
                                                                      prefix=prefix, condition=condition, who=who)
        elif node_type == consts.Consts.parallel_gateway:
            return BpmnDiagramGraphCsvExport.export_parallel_gateway(bpmn_graph, export_elements, node, order=order,
                                                                     prefix=prefix, condition=condition, who=who)
        elif node_type == consts.Consts.start_event:
            return BpmnDiagramGraphCsvExport.export_start_event(bpmn_graph, export_elements, node, order=order,
                                                                prefix=prefix, condition=condition, who=who)
        elif node_type == consts.Consts.end_event:
            return BpmnDiagramGraphCsvExport.export_end_event(export_elements, node, order=order,
                                                              prefix=prefix, condition=condition, who=who)

    @staticmethod
    def export_start_event(bpmn_graph, export_elements, node, order=0, prefix="", condition="", who=""):
        """
        Start event export
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """

        # Assuming that there is only one event definition
        event_definition = node[1][consts.Consts.event_definitions][0]
        if event_definition[consts.Consts.definition_type] == "messageEventDefinition":
            activity = "message " + node[1][consts.Consts.node_name]
        elif event_definition[consts.Consts.definition_type] == "timerEventDefinition":
            activity = "timer " + node[1][consts.Consts.node_name]
        else:
            activity = node[1][consts.Consts.node_name]

        export_elements.append({"Order": prefix + str(order), "Activity": activity, "Condition": condition,
                                "Who": who, "Subprocess": "", "Terminated": ""})

        outgoing_flow_id = node[1][consts.Consts.outgoing_flows][0]
        outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
        outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])
        return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node, order + 1, prefix, who)

    @staticmethod
    def export_end_event(export_elements, node, order=0, prefix="", condition="", who=""):
        """
        End event export
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """

        # Assuming that there is only one event definition
        event_definition = node[1][consts.Consts.event_definitions][0]
        if event_definition[consts.Consts.definition_type] == "messageEventDefinition":
            activity = "message " + node[1][consts.Consts.node_name]
        else:
            activity = node[1][consts.Consts.node_name]

        export_elements.append({"Order": prefix + str(order), "Activity": activity, "Condition": condition, "Who": who,
                                "Subprocess": "", "Terminated": "yes"})

    @staticmethod
    def export_task(bpmn_graph, export_elements, node, order=0, prefix="", condition="", who=""):
        """
        Task export
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """
        export_elements.append({"Order": prefix + str(order), "Activity": node[1][consts.Consts.node_name],
                                "Condition": condition, "Who": who, "Subprocess": "", "Terminated": ""})
        outgoing_flow_id = node[1][consts.Consts.outgoing_flows][0]
        outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
        outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])
        return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node, order + 1, prefix, who)

    @staticmethod
    def export_sub_process(bpmn_graph, export_elements, node, order=0, prefix="", condition="", who=""):
        """
        Subprocess export
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """
        export_elements.append({"Order": prefix + str(order), "Activity": node[1][consts.Consts.node_name],
                                "Condition": condition, "Who": who, "Subprocess": "yes", "Terminated": ""})
        outgoing_flow_id = node[1][consts.Consts.outgoing_flows][0]
        outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
        outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])
        return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node, order + 1, prefix, "",
                                                     who)

    @staticmethod
    def export_exclusive_gateway(bpmn_graph, export_elements, node, order=0, prefix="", condition="", who=""):
        """
        Exclusive gateway export
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """
        outgoing_flows = node[1][consts.Consts.outgoing_flows]
        if len(outgoing_flows) == 1:
            outgoing_flow_id = outgoing_flows[0]
            outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

            return outgoing_node
        elif len(outgoing_flows) > 1:
            next_node = None
            alphabet_suffix_index = 0
            for outgoing_flow_id in outgoing_flows:
                outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
                outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

                # This will work only up to 26 outgoing flows
                suffix = string.ascii_lowercase[alphabet_suffix_index]
                next_prefix = prefix + str(order) + suffix
                alphabet_suffix_index += 1
                # TODO add support for default path and add "else" condition
                next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node, 1,
                                                                  next_prefix, "", who)

            return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node, order + 1, prefix, "",
                                                         who)
        else:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format: gateway must have at least 1 outgoing flow")

    @staticmethod
    def export_parallel_gateway(bpmn_graph, export_elements, node, order=0, prefix="", condition="", who=""):
        """
        Parallel gateway export
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """
        outgoing_flows = node[1][consts.Consts.outgoing_flows]
        if len(outgoing_flows) == 1:
            outgoing_flow_id = outgoing_flows[0]
            outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

            return outgoing_node
        elif len(outgoing_flows) > 1:
            next_node = None
            alphabet_suffix_index = 0
            for outgoing_flow_id in outgoing_flows:
                outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
                outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

                # This will work only up to 26 outgoing flows
                suffix = string.ascii_lowercase[alphabet_suffix_index]
                next_prefix = prefix + str(order) + suffix
                alphabet_suffix_index += 1
                next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node, 1,
                                                                  next_prefix, "", who)

            return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node, order + 1, prefix, "",
                                                         who)
        else:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format: gateways must have 1 or 2 outgoing flows")

    @staticmethod
    def export_inclusive_gateway(bpmn_graph, export_elements, node, order=0, prefix="", who=""):
        """
        Inclusive gateway export
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """
        outgoing_flows = node[1][consts.Consts.outgoing_flows]
        if len(outgoing_flows) == 1:
            outgoing_flow_id = outgoing_flows[0]
            outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

            return outgoing_node
        elif len(outgoing_flows) > 1:
            next_node = None
            alphabet_suffix_index = 0
            for outgoing_flow_id in outgoing_flows:
                outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
                outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

                # This will work only up to 26 outgoing flows
                suffix = string.ascii_lowercase[alphabet_suffix_index]
                next_prefix = prefix + str(order) + suffix
                alphabet_suffix_index += 1
                condition = outgoing_flow[2][consts.Consts.name]
                next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node, 1,
                                                                  next_prefix, condition, who)

            return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node, order + 1, prefix, "",
                                                         who)
        else:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format: gateways must have 1 or 2 outgoing flows")

    @staticmethod
    def write_export_node_to_file(file_object, export_elements):
        """
        Exporting process to CSV file
        :param file_object: object of File class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document.
        """
        for export_element in export_elements:
            # Order,Activity,Condition,Who,Subprocess,Terminated
            file_object.write(
                export_element["Order"] + "," + export_element["Activity"] + "," + export_element["Condition"] + "," +
                export_element["Who"] + "," + export_element["Subprocess"] + "," + export_element["Terminated"] + "\n")
