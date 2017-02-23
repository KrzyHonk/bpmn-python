# coding=utf-8
"""
Class used for representing tLane of BPMN 2.0 graph
"""
from bpmn_python.graph.classes.base_element_type import BaseElement
from bpmn_python.graph.classes.lane_set_type import LaneSet


class Lane(BaseElement):
    """
    Class used for representing tLane of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Lane, self).__init__()
        self.__name = None
        self.__flow_node_ref_list = None
        self.__child_lane_set = None

    def get_name(self):
        """
        Getter for 'name' field.
        :return:a value of 'name' field.
        """
        return self.__name

    def set_name(self, value):
        """
        Setter for 'name' field.
        :param value - a new value of 'name' field.
        """
        if not isinstance(value, str):
            raise TypeError("Name must be set to a string")
        self.__name = value

    def get_flow_node_ref_list(self):
        """
        Getter for 'flow_node_ref' field.
        :return:a value of 'flow_node_ref' field.
        """
        return self.__flow_node_ref_list

    def set_flow_node_ref_list(self, value):
        """
        Setter for 'flow_node_ref' field.
        :param value - a new value of 'flow_node_ref' field.
        """
        if type(value) is not list:
            raise TypeError("FlowNodeRefList new value must be a list")
        for element in value:
            if not isinstance(element, str):
                raise TypeError("FlowNodeRefList elements in variable must be of string class")
        self.__flow_node_ref_list = value

    def get_child_lane_set(self):
        """
        Getter for 'child_lane_set' field.
        :return:a value of 'child_lane_set' field.
        """
        return self.__child_lane_set

    def set_child_lane_set(self, value):
        """
        Setter for 'child_lane_set' field.
        :param value - a new value of 'child_lane_set' field.
        """
        if not isinstance(value, LaneSet):
            raise TypeError("ChildLaneSet must be a LaneSet")
        self.__child_lane_set = value
