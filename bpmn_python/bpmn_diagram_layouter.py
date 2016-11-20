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
        Edge Sequence flow, message flow, data flow
        Element Every element of the process which is not an edge
        Start Event All types of start events
        End Event All types of end events

        Join An element with more than one incoming edge
        Split An element with more than one outgoing edge
        :param bpmn_diagram:
        :return:
        """
        elements_classification = []
        incoming_edges_param_name = "incoming"
        outgoing_edges_param_name = "outgoing"
        task_param_name = "task"
        node_param_name = "node"
        edge_param_name = "edge"
        classification_param_name = "classification"

        classification_element = "Element"
        classification_join = "Join"
        classification_split = "Split"
        classification_start_event = "Start Event"
        classification_end_event = "End Event"

        task_list = bpmn_diagram.get_nodes(task_param_name)
        for element in task_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        subprocess_list = bpmn_diagram.get_nodes("subProcess")
        for element in subprocess_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        complex_gateway_list = bpmn_diagram.get_nodes("complexGateway")
        for element in complex_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        event_based_gateway_list = bpmn_diagram.get_nodes("eventBasedGateway")
        for element in event_based_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        inclusive_gateway_list = bpmn_diagram.get_nodes("inclusiveGateway")
        for element in inclusive_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        exclusive_gateway_list = bpmn_diagram.get_nodes("exclusiveGateway")
        for element in exclusive_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        parallel_gateway_list = bpmn_diagram.get_nodes("parallelGateway")
        for element in parallel_gateway_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        start_event_list = bpmn_diagram.get_nodes("startEvent")
        for element in start_event_list:
            tmp = [classification_element, classification_start_event]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        intermediate_catch_event_list = bpmn_diagram.get_nodes("intermediateCatchEvent")
        for element in intermediate_catch_event_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        end_event_list = bpmn_diagram.get_nodes("endEvent")
        for element in end_event_list:
            tmp = [classification_element, classification_end_event]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        intermediate_throw_event_list = bpmn_diagram.get_nodes("intermediateThrowEvent")
        for element in intermediate_throw_event_list:
            tmp = [classification_element]
            if len(element[1][incoming_edges_param_name]) >= 2:
                tmp.append(classification_join)
            if len(element[1][outgoing_edges_param_name]) >= 2:
                tmp.append(classification_split)
            elements_classification += [{node_param_name: element, classification_param_name: tmp}]

        edges_classification = []
        eges_list = bpmn_diagram.get_edges()
        for edge in eges_list:
            edges_classification += [{edge_param_name: edge, classification_param_name: ["Edge"]}]

        return elements_classification, edges_classification

    @staticmethod
    def topological_sort(bpmn_diagram, elements_classification, edges_classification):
        """
        :return:
        """
        incoming_edges_param_name = "incoming"
        outgoing_edges_param_name = "outgoing"
        node_param_name = "node"
        classification_param_name = "classification"

        G = list(elements_classification)
        L = []
        S = []
        B = []

        while G:
            for classification in G:
                incoming_list = classification[node_param_name][1][incoming_edges_param_name]
                if len(incoming_list) == 0:
                    S.append(classification)
            while len(S) > 0:
                classification = S.pop()
                G.remove(classification)
                outgoing_list = list(classification[node_param_name][1][outgoing_edges_param_name])
                L.append(classification)
                '''
                foreach node m with an edge e from n to m do
                    remove e
                    decrement incoming link counter from m
                '''
                for target_edge in outgoing_list:
                    edge = bpmn_diagram.get_edge_by_id(target_edge)
                    source_id = edge[2]["source_id"]
                    target_id = edge[2]["target_id"]

                    try:
                        source = bpmn_diagram.get_node_by_id(source_id)
                        source[1][outgoing_edges_param_name].remove(target_edge)
                    except ValueError:
                        print(target_edge)

                    try:
                        target = bpmn_diagram.get_node_by_id(target_id)
                        target[1][incoming_edges_param_name].remove(target_edge)
                    except ValueError:
                        print(target_edge)
            else:
                for classification in G:
                    if "Join" in classification[classification_param_name]:
                        # TODO need some way to handle cycle (either add backward edges to representation)
                        # or implement different solution
                        pass
        return L, B
