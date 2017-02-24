# coding=utf-8
"""
Class used for representing tFlowNode of BPMN 2.0 graph
"""
import bpmn_python.graph.classes.flow_element_type as flow_element_type


class FlowNode(flow_element_type.FlowElement):
    """
    Class used for representing tFlowNode of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        Fields (except inherited):
        - incoming_list: a list of IDs (String type) of incoming flows.
        - outgoing_list: a list of IDs (String type) of outgoing flows.
        """
        super(FlowNode, self).__init__()
        self.__incoming_list = []
        self.__outgoing_list = []

    def get_incoming(self):
        """
        Getter for 'incoming' field.
        :return:a value of 'incoming' field.
        """
        return self.__incoming_list

    def set_incoming(self, value):
        """
        Setter for 'incoming' field.
        :param value - a new value of 'incoming' field. List of IDs (String type) of incoming flows.
        """
        if not isinstance(value, list):
            raise TypeError("IncomingList new value must be a list")
        for element in value:
            if not isinstance(element, str):
                raise TypeError("IncomingList elements in variable must be of String class")
        self.__incoming_list = value

    def get_outgoing(self):
        """
        Getter for 'outgoing' field.
        :return:a value of 'outgoing' field.
        """
        return self.__outgoing_list

    def set_outgoing(self, value):
        """
        Setter for 'outgoing' field.
        :param value - a new value of 'outgoing' field. Must be a list of IDs (String type) of outgoing flows.
        """
        if not isinstance(value, list):
            raise TypeError("OutgoingList new value must be a list")
        for element in value:
            if not isinstance(element, str):
                raise TypeError("OutgoingList elements in variable must be of String class")
        self.__outgoing_list = value
