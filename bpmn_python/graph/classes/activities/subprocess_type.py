# coding=utf-8
"""
Class used for representing tSubProcess of BPMN 2.0 graph
"""
import graph.classes.activities.activity_type as activity
import graph.classes.flow_element_type as flow_element
import graph.classes.lane_set_type as lane_set


class SubProcess(activity.Activity):
    """
    Class used for representing tSubProcess of BPMN 2.0 graph
    Fields (except inherited):
    - lane_set_list: a list of LaneSet objects.
    - flow_element_list: a list of FlowElement objects.
    - triggered_by_event: a boolean value..
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(SubProcess, self).__init__()
        self.__triggered_by_event = False
        self.__lane_set_list = []
        self.__flow_element_list = []

    def triggered_by_event(self):
        """
        Getter for 'triggered_by_event' field.
        :return: value of 'triggered_by_event' field.
        """
        return self.__triggered_by_event

    def set_triggered_by_event(self, value):
        """
        Setter for 'triggered_by_event' field.
        :param value - a new value of 'triggered_by_event' field. Must be a boolean type. Does not accept None value.
        """
        if value is None or not isinstance(value, bool):
            raise TypeError("TriggeredByEvent must be set to a bool")
        else:
            self.__triggered_by_event = value

    def get_lane_set_list(self):
        """
        Getter for 'lane_set_list' field.
        :return:a value of 'lane_set_list' field.
        """
        return self.__lane_set_list

    def set_lane_set_list(self, value):
        """
        Setter for 'lane_set_list' field.
        :param value - a new value of 'lane_set_list' field. Must be a list
        """
        if value is None or not isinstance(value, list):
            raise TypeError("LaneSetList new value must be a list")
        else:
            for element in value:
                if not isinstance(element, lane_set.LaneSet):
                    raise TypeError("LaneSetList elements in variable must be of LaneSet class")
            self.__lane_set_list = value

    def get_flow_element_list(self):
        """
        Getter for 'flow_element_list' field.
        :return:a value of 'flow_element_list' field.
        """
        return self.__flow_element_list

    def set_flow_element_list(self, value):
        """
        Setter for 'flow_element_list' field.
        :param value - a new value of 'flow_element_list' field. Must be a list
        """
        if value is None or not isinstance(value, list):
            raise TypeError("FlowElementList new value must be a list")
        else:
            for element in value:
                if not isinstance(element, flow_element.FlowElement):
                    raise TypeError("FlowElementList elements in variable must be of FlowElement class")
            self.__flow_element_list = value
