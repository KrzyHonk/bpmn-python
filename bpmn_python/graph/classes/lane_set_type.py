# coding=utf-8
"""
Class used for representing tSetLane of BPMN 2.0 graph
"""
from bpmn_python.graph.classes.base_element_type import BaseElement
from bpmn_python.graph.classes.lane_type import Lane


class LaneSet(BaseElement):
    """
    Class used for representing tSetLane of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(LaneSet, self).__init__()
        self.__name = None
        self.__lane_list = None

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

    def get_lane_list(self):
        """
        Getter for 'lane_list' field.
        :return:a value of 'lane_list' field.
        """
        return self.__lane_list

    def set_lane_list(self, value):
        """
        Setter for 'lane_list' field.
        :param value - a new value of 'lane_list' field.
        """
        if type(value) is not list:
            raise TypeError("LaneList new value must be a list")
        for element in value:
            if not isinstance(element, Lane):
                raise TypeError("LaneList elements in variable must be of Lane class")
        self.__lane_list = value
