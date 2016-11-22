# coding=utf-8
"""
Package with BPMNDiagramGraph - graph representation of BPMN diagram
"""


class BpmnDiagramLayouter:
    """
    Class BPMNDiagramGraphExport provides methods for exporting BPMNDiagramGraph into BPMN 2.0 XML file.
    As a utility class, it only contains static methods.
    This class is meant to be used from BPMNDiagramGraph class.
    """

    def __init__(self):
        pass

    @staticmethod
    def generate_layout(bpmn_diagram):
        """
        :param bpmn_diagram: an instance of BPMNDiagramGraph class.
        """
        classification = BpmnDiagramLayouter.generate_elements_clasification(bpmn_diagram)
        output = BpmnDiagramLayouter.topological_sort(bpmn_diagram, classification[0], classification[1])
        print("End")

    @staticmethod
    def generate_elements_clasification(bpmn_diagram):
        """
        :param bpmn_diagram:
        :return:
        """
        nodes_classification = []
        incoming_flows_list_param_name = "incoming"
        outgoing_flows_list_param_name = "outgoing"
        task_param_name = "task"
        node_param_name = "node"
        flow_param_name = "flow"
        classification_param_name = "classification"

        classification_element = "Element"
        classification_join = "Join"
        classification_split = "Split"
        classification_start_event = "Start Event"
        classification_end_event = "End Event"

        task_list = bpmn_diagram.get_nodes(task_param_name)
        for element in task_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        subprocess_list = bpmn_diagram.get_nodes("subProcess")
        for element in subprocess_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        complex_gateway_list = bpmn_diagram.get_nodes("complexGateway")
        for element in complex_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        event_based_gateway_list = bpmn_diagram.get_nodes("eventBasedGateway")
        for element in event_based_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        inclusive_gateway_list = bpmn_diagram.get_nodes("inclusiveGateway")
        for element in inclusive_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        exclusive_gateway_list = bpmn_diagram.get_nodes("exclusiveGateway")
        for element in exclusive_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        parallel_gateway_list = bpmn_diagram.get_nodes("parallelGateway")
        for element in parallel_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        start_event_list = bpmn_diagram.get_nodes("startEvent")
        for element in start_event_list:
            tmp = [classification_element, classification_start_event]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        intermediate_catch_event_list = bpmn_diagram.get_nodes("intermediateCatchEvent")
        for element in intermediate_catch_event_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        end_event_list = bpmn_diagram.get_nodes("endEvent")
        for element in end_event_list:
            tmp = [classification_element, classification_end_event]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        intermediate_throw_event_list = bpmn_diagram.get_nodes("intermediateThrowEvent")
        for element in intermediate_throw_event_list:
            tmp = [classification_element]
            if len(element[1][incoming_flows_list_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_flows_list_param_name]) >= 2:
                tmp.append(classification_split)
            nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

        flows_classification = []
        flows_list = bpmn_diagram.get_flows()
        for flow in flows_list:
            flows_classification += [{flow_param_name: flow, classification_param_name: ["Flow"]}]

        return nodes_classification, flows_classification

    @staticmethod
    def topological_sort(bpmn_diagram, nodes_with_classification, flows_classification):
        """
        :return:
        """
        incoming_flow_list_param_name = "incoming"
        outgoing_flow_list_param_name = "outgoing"
        node_param_name = "node"
        classification_param_name = "classification"

        tmp_nodes_with_classification = list(nodes_with_classification)
        sorted_nodes = []
        no_incoming_flow_nodes = []
        backward_flows = []

        while tmp_nodes_with_classification:
            for node_with_classification in tmp_nodes_with_classification:
                incoming_list = node_with_classification[node_param_name][1][incoming_flow_list_param_name]
                if len(incoming_list) == 0:
                    no_incoming_flow_nodes.append(node_with_classification)
            if len(no_incoming_flow_nodes) > 0:
                while len(no_incoming_flow_nodes) > 0:
                    node_with_classification = no_incoming_flow_nodes.pop()
                    tmp_nodes_with_classification.remove(node_with_classification)
                    sorted_nodes.append(node_with_classification)

                    outgoing_list = list(node_with_classification[node_param_name][1][outgoing_flow_list_param_name])
                    tmp_outgoing_list = list(outgoing_list)

                    for flow_id in tmp_outgoing_list:
                        '''
                        - Remove the outgoing flow for source flow node (the one without incoming flows)
                        - Get the target node
                        - Remove the incoming flow for target flow node
                        '''
                        outgoing_list.remove(flow_id)

                        flow = bpmn_diagram.get_flow_by_id(flow_id)
                        target_id = flow[2]["target_id"]
                        target = bpmn_diagram.get_node_by_id(target_id)
                        target[1][incoming_flow_list_param_name].remove(flow_id)
            else:
                for node_with_classification in tmp_nodes_with_classification:
                    if "Join" in node_with_classification[classification_param_name]:
                        incoming_list = list(node_with_classification[node_param_name][1][incoming_flow_list_param_name])
                        tmp_incoming_list = list(incoming_list)
                        for flow_id in tmp_incoming_list:
                            incoming_list.remove(flow_id)

                            flow = bpmn_diagram.get_flow_by_id(flow_id)
                            target_id = flow[2]["target_id"]
                            target = bpmn_diagram.get_node_by_id(target_id)
                            target[1][outgoing_flow_list_param_name].remove(flow_id)
        return sorted_nodes, backward_flows
