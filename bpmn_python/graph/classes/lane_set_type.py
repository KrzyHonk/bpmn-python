# coding=utf-8
"""
Class used for representing tSetLane of BPMN 2.0 graph
"""
import graph.classes.base_element_type as base_element
import graph.classes.lane_type as lane


class LaneSet(base_element.BaseElement):
    """
    Class used for representing tSetLane of BPMN 2.0 graph.
    Fields (except inherited):
    - name: name of element. Must be either None (name is optional according to BPMN 2.0 XML Schema) or String.
    - lane_list: a list of Lane objects.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(LaneSet, self).__init__()
        self.__name = None
        self.__lane_list = []

    def get_name(self):
        """
        Getter for 'name' field.
        :return: value of 'name' field.
        """
        return self.__name

    def set_name(self, value):
        """
        Setter for 'name' field.
        :param value - a new value of 'name' field. Must be either None (name is optional according to BPMN 2.0 XML
        Schema) or String.
        """
        if value is None:
            self.__name = value
        elif not isinstance(value, str):
            raise TypeError("Name must be set to a String")
        else:
            self.__name = value

    def get_lane_list(self):
        """
        Getter for 'lane_list' field.
        :return: value of 'lane_list' field.
        """
        return self.__lane_list

    def set_lane_list(self, value):
        """
        Setter for 'lane_list' field.
        :param value - a new value of 'lane_list' field. Must be a list of Lane objects
        """
        if value is None or not isinstance(value, list):
            raise TypeError("LaneList new value must be a list")
        else:
            for element in value:
                if not isinstance(element, lane.Lane):
                    raise TypeError("LaneList elements in variable must be of Lane class")
            self.__lane_list = value
