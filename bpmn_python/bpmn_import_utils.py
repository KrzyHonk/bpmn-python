# coding=utf-8
"""
Class including utility method used in diagram importing
"""

import bpmn_python.bpmn_python_consts as consts


class BpmnImportUtils(object):
    """
    Class including utility method used in diagram importing
    """

    def __init__(self):
        pass

    @staticmethod
    def remove_namespace_from_tag_name(tag_name):
        """
        Helper function, removes namespace annotation from tag name.

        :param tag_name: string with tag name.
        """
        return tag_name.split(':')[-1]

    @staticmethod
    def iterate_elements(parent):
        """
        Helper function that iterates over child Nodes/Elements of parent Node/Element.

        :param parent: object of Element class, representing parent element.
        """
        element = parent.firstChild
        while element is not None:
            yield element
            element = element.nextSibling

    @staticmethod
    def generate_nodes_clasification(bpmn_diagram):
        """
        Diagram elements classification. Implementation based on article "A Simple Algorithm for Automatic Layout of
        BPMN Processes".
        Assigns a classification to the diagram element according to specific element parameters.
        - Element - every element of the process which is not an edge,
        - Start Event - all types of start events,
        - End Event - all types of end events,
        - Join - an element with more than one incoming edge,
        - Split - an element with more than one outgoing edge.

        :param bpmn_diagram: BPMNDiagramGraph class instance representing a BPMN process diagram.
        :return: a dictionary of classification labels. Key - node id. Values - a list of labels.
        """
        nodes_classification = {}

        classification_element = "Element"
        classification_start_event = "Start Event"
        classification_end_event = "End Event"

        task_list = bpmn_diagram.get_nodes(consts.Consts.task)
        for element in task_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        subprocess_list = bpmn_diagram.get_nodes(consts.Consts.subprocess)
        for element in subprocess_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        complex_gateway_list = bpmn_diagram.get_nodes(consts.Consts.complex_gateway)
        for element in complex_gateway_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        event_based_gateway_list = bpmn_diagram.get_nodes(consts.Consts.event_based_gateway)
        for element in event_based_gateway_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        inclusive_gateway_list = bpmn_diagram.get_nodes(consts.Consts.inclusive_gateway)
        for element in inclusive_gateway_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        exclusive_gateway_list = bpmn_diagram.get_nodes(consts.Consts.exclusive_gateway)
        for element in exclusive_gateway_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        parallel_gateway_list = bpmn_diagram.get_nodes(consts.Consts.parallel_gateway)
        for element in parallel_gateway_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        start_event_list = bpmn_diagram.get_nodes(consts.Consts.start_event)
        for element in start_event_list:
            classification_labels = [classification_element, classification_start_event]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        intermediate_catch_event_list = bpmn_diagram.get_nodes(consts.Consts.intermediate_catch_event)
        for element in intermediate_catch_event_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        end_event_list = bpmn_diagram.get_nodes(consts.Consts.end_event)
        for element in end_event_list:
            classification_labels = [classification_element, classification_end_event]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        intermediate_throw_event_list = bpmn_diagram.get_nodes(consts.Consts.intermediate_throw_event)
        for element in intermediate_throw_event_list:
            classification_labels = [classification_element]
            BpmnImportUtils.split_join_classification(element, classification_labels, nodes_classification)

        return nodes_classification

    @staticmethod
    def split_join_classification(element, classification_labels, nodes_classification):
        """
        Add the "Split", "Join" classification, if the element qualifies for.

        :param element: an element from BPMN diagram,
        :param classification_labels: list of labels attached to the element,
        :param nodes_classification: dictionary of classification labels. Key - node id. Value - a list of labels.
        """
        classification_join = "Join"
        classification_split = "Split"
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            classification_labels.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            classification_labels.append(classification_split)
        nodes_classification[element[0]] = classification_labels
