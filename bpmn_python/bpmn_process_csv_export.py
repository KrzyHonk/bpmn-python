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

import bmpn_python_consts as consts
import bpmn_diagram_exception as bpmn_exception
import bpmn_import_utils as utils


class BpmnDiagramGraphCsvExport(object):
    # TODO need to add support for lanes in import/export. After that, read user and add 'who' param
    # TODO multiple start events - use dictionary to handle it?
    # There will be problem with exporting. Maybe try with sorting by order (use regex grouping)
    # TODO loops
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
    def export_process_to_csv(bpmn_diagram, directory, filename):
        """
        Root method of CSV export functionality.
        :param bpmn_diagram: an instance of BpmnDiagramGraph class,
        :param directory: a string object, which is a path of output directory,
        :param filename: a string object, which is a name of output file.
        """
        nodes = copy.deepcopy(bpmn_diagram.get_nodes())
        start_nodes = []
        export_elements = []

        for node in nodes:
            incoming_list = node[1][consts.Consts.incoming_flows]
            if len(incoming_list) == 0:
                start_nodes.append(node)
        if len(start_nodes) != 1:
            raise bpmn_exception.BpmnPythonError("Exporting to CSV format accepts only one start event")

        nodes_classification = utils.BpmnImportUtils.generate_nodes_clasification(bpmn_diagram)
        start_node = start_nodes.pop()
        BpmnDiagramGraphCsvExport.export_node(bpmn_diagram, export_elements, start_node, nodes_classification)

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
    def export_node(bpmn_graph, export_elements, node, nodes_classification, order=0, prefix="", condition="", who=""):
        """
        General method for node exporting
        :param bpmn_graph: an instance of BpmnDiagramGraph class,
        :param export_elements: a dictionary object. The key is a node ID, value is a dictionary of parameters that
        will be used in exported CSV document,
        :param node: networkx.Node object,
        :param nodes_classification: dictionary of classification labels. Key - node id. Value - a list of labels,
        :param order: the order param of exported node,
        :param prefix: the prefix of exported node - if the task appears after some gateway, the prefix will identify
        the branch
        :param condition: the condition param of exported node,
        :param who: the condition param of exported node,
        :return: None or the next node object if the exported node was a gateway join.
        """
        node_type = node[1][consts.Consts.type]
        node_classification = nodes_classification[node[0]]

        if node_type == consts.Consts.task:
            return BpmnDiagramGraphCsvExport.export_task(bpmn_graph, export_elements, node, nodes_classification,
                                                         order=order, prefix=prefix, condition=condition, who=who)
        elif node_type == consts.Consts.subprocess:
            return BpmnDiagramGraphCsvExport.export_sub_process(bpmn_graph, export_elements, node, nodes_classification,
                                                                order=order, prefix=prefix, condition=condition,
                                                                who=who)
        elif node_type == consts.Consts.inclusive_gateway:
            return BpmnDiagramGraphCsvExport.export_inclusive_gateway(bpmn_graph, export_elements, node,
                                                                      nodes_classification, order=order, prefix=prefix,
                                                                      who=who)
        elif node_type == consts.Consts.exclusive_gateway:
            return BpmnDiagramGraphCsvExport.export_exclusive_gateway(bpmn_graph, export_elements, node,
                                                                      nodes_classification, order=order, prefix=prefix,
                                                                      condition=condition, who=who)
        elif node_type == consts.Consts.parallel_gateway:
            return BpmnDiagramGraphCsvExport.export_parallel_gateway(bpmn_graph, export_elements, node,
                                                                     nodes_classification, order=order, prefix=prefix,
                                                                     condition=condition, who=who)
        elif node_type == consts.Consts.start_event:
            return BpmnDiagramGraphCsvExport.export_start_event(bpmn_graph, export_elements, node, nodes_classification,
                                                                order=order, prefix=prefix, condition=condition,
                                                                who=who)
        elif node_type == consts.Consts.end_event:
            return BpmnDiagramGraphCsvExport.export_end_event(export_elements, node, nodes_classification, order=order,
                                                              prefix=prefix, condition=condition, who=who)

    @staticmethod
    def export_start_event(bpmn_graph, export_elements, node, nodes_classification, order=0, prefix="", condition="",
                           who=""):
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
        event_definitions = node[1][consts.Consts.event_definitions]
        if event_definitions is not None and len(event_definitions) > 0:
            event_definition = node[1][consts.Consts.event_definitions][0]
        else:
            event_definition = None

        if event_definition is None:
            activity = node[1][consts.Consts.node_name]
        elif event_definition[consts.Consts.definition_type] == "messageEventDefinition":
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
        return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node, nodes_classification,
                                                     order + 1, prefix, who)

    @staticmethod
    def export_end_event(export_elements, node, nodes_classification, order=0, prefix="", condition="", who=""):
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
        event_definitions = node[1][consts.Consts.event_definitions]
        if event_definitions is not None and len(event_definitions) > 0:
            event_definition = node[1][consts.Consts.event_definitions][0]
        else:
            event_definition = None

        if event_definition is None:
            activity = node[1][consts.Consts.node_name]
        elif event_definition[consts.Consts.definition_type] == "messageEventDefinition":
            activity = "message " + node[1][consts.Consts.node_name]
        else:
            activity = node[1][consts.Consts.node_name]

        export_elements.append({"Order": prefix + str(order), "Activity": activity, "Condition": condition, "Who": who,
                                "Subprocess": "", "Terminated": "yes"})
        # No outgoing elements for EndEvent
        return None

    @staticmethod
    def export_task(bpmn_graph, export_elements, node, nodes_classification, order=0, prefix="", condition="", who=""):
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
        outgoing_flows = node[1][consts.Consts.outgoing_flows]
        if len(outgoing_flows) == 1:
            outgoing_flow_id = outgoing_flows[0]
            outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

            return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                         nodes_classification, order + 1, prefix, "", who)
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
                tmp_next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                                      nodes_classification, 1, next_prefix, "", who)
                if tmp_next_node is not None:
                    next_node = tmp_next_node

            if next_node is not None:
                return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node,
                                                             nodes_classification, order + 1, prefix, "", who)
            else:
                return None
        else:
            return None

    @staticmethod
    def export_sub_process(bpmn_graph, export_elements, node, nodes_classification, order=0, prefix="", condition="",
                           who=""):
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
        outgoing_flows = node[1][consts.Consts.outgoing_flows]
        if len(outgoing_flows) == 1:
            outgoing_flow_id = outgoing_flows[0]
            outgoing_flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_graph.get_node_by_id(outgoing_flow[2][consts.Consts.target_ref])

            return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                         nodes_classification, order + 1, prefix, "", who)
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
                tmp_next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                                      nodes_classification, 1, next_prefix, "", who)
                if tmp_next_node is not None:
                    next_node = tmp_next_node

            if next_node is not None:
                return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node,
                                                             nodes_classification, order + 1, prefix, "", who)
            else:
                return None
        else:
            return None

    @staticmethod
    def export_exclusive_gateway(bpmn_graph, export_elements, node, nodes_classification, order=0, prefix="",
                                 condition="", who=""):
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
        if consts.Consts.default in node[1]:
            default_flow_id = node[1][consts.Consts.default]
        else:
            default_flow_id = None

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
                # TODO bramki - jeśli prowadzi flow prowadzi do joina, to daję goto

                if outgoing_flow_id == default_flow_id:
                    tmp_next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                                          nodes_classification, 1, next_prefix, "else",
                                                                          who)
                    if tmp_next_node is not None:
                        next_node = tmp_next_node
                else:
                    tmp_next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                                          nodes_classification, 1, next_prefix,
                                                                          condition,
                                                                          who)
                    if tmp_next_node is not None:
                        next_node = tmp_next_node

            if next_node is not None:
                return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node,
                                                             nodes_classification, order + 1, prefix, "", who)
            else:
                return None
        else:
            return None

    @staticmethod
    def export_parallel_gateway(bpmn_graph, export_elements, node, nodes_classification, order=0, prefix="",
                                condition="", who=""):
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
                next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                                  nodes_classification, 1, next_prefix, "", who)

            return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node, nodes_classification,
                                                         order + 1, prefix, "", who)
        else:
            return None

    @staticmethod
    def export_inclusive_gateway(bpmn_graph, export_elements, node, nodes_classification, order=0, prefix="", who=""):
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
                next_node = BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, outgoing_node,
                                                                  nodes_classification, 1, next_prefix, condition, who)

            return BpmnDiagramGraphCsvExport.export_node(bpmn_graph, export_elements, next_node, nodes_classification,
                                                         order + 1, prefix, "", who)
        else:
            return None

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
