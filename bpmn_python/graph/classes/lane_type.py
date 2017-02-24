# coding=utf-8
"""
Class used for representing tLane of BPMN 2.0 graph
"""
import graph.classes.base_element_type as base_element
import graph.classes.lane_set_type as lane_set


class Lane(base_element.BaseElement):
    """
    Class used for representing tLane of BPMN 2.0 graph.
    Fields (except inherited):
    - name: name of element. Must be either None (name is optional according to BPMN 2.0 XML Schema) or String.
    - flow_node_ref_list: a list of String objects (ID of referenced nodes).
    - child_lane_set: an object of LaneSet type.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Lane, self).__init__()
        self.__name = None
        self.__flow_node_ref_list = []
        self.__child_lane_set = None

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

    def get_flow_node_ref_list(self):
        """
        Getter for 'flow_node_ref' field.
        :return:a value of 'flow_node_ref' field.
        """
        return self.__flow_node_ref_list

    def set_flow_node_ref_list(self, value):
        """
        Setter for 'flow_node_ref' field.
        :param value - a new value of 'flow_node_ref' field. Must be a list of String objects (ID of referenced nodes).
        """
        if value is None or not isinstance(value, list):
            raise TypeError("FlowNodeRefList new value must be a list")
        else:
            for element in value:
                if not isinstance(element, str):
                    raise TypeError("FlowNodeRefList elements in variable must be of String class")
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
        :param value - a new value of 'child_lane_set' field. Must be an object of LaneSet type.
        """
        if value is None:
            self.__child_lane_set = value
        elif not isinstance(value, lane_set.LaneSet):
            raise TypeError("ChildLaneSet must be a LaneSet")
        else:
            self.__child_lane_set = value
