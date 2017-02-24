# coding=utf-8
"""
Class used for representing tProcess of BPMN 2.0 graph
"""
import graph.classes.flow_element_type as flow_element
import graph.classes.lane_set_type as lane_set
import graph.classes.root_element.callable_element_type as callable_element


class Process(callable_element.CallableElement):
    """
    Class used for representing tProcess of BPMN 2.0 graph.
    """
    __process_type_list = ["None", "Public", "Private"]

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Process, self).__init__()
        self.__process_type = "None"
        self.__is_closed = False
        self.__is_executable = False
        self.__lane_set_list = []
        self.__flow_element_list = []

    def get_process_type(self):
        """
        Getter for 'process_type' field.
        :return:a value of 'process_type' field.
        """
        return self.__process_type

    def set_process_type(self, value):
        """
        Setter for 'process_type' field.
        :param value - a new value of 'process_type' field.
        """
        if value is None or not isinstance(value, str):
            raise TypeError("ProcessType must be set to a String")
        elif value not in Process.__process_type_list:
            raise ValueError("ProcessType must be one of specified values: 'None', 'Public', 'Private'")
        else:
            self.__process_type = value

    def is_closed(self):
        """
        Getter for 'is_closed' field.
        :return: value of 'is_closed' field.
        """
        return self.__is_closed

    def set_is_closed(self, value):
        """
        Setter for 'is_closed' field.
        :param value - a new value of 'is_closed' field. Must be a boolean type. Does not accept None value.
        """
        if value is None or not isinstance(value, bool):
            raise TypeError("IsClosed must be set to a bool")
        else:
            self.__is_closed = value

    def is_executable(self):
        """
        Getter for 'is_executable' field.
        :return: value of 'is_executable' field.
        """
        return self.__is_executable

    def set_is_executable(self, value):
        """
        Setter for 'is_executable' field.
        :param value - a new value of 'is_executable' field. Must be a boolean type. Does not accept None value.
        """
        if value is None or not isinstance(value, bool):
            raise TypeError("IsExecutable must be set to a bool")
        else:
            self.__is_executable = value

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
