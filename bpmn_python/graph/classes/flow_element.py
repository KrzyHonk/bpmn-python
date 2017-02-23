# coding=utf-8
"""
Class used for representing tFlowElement of BPMN 2.0 graph
"""
from bpmn_python.graph.classes.base_element_type import BaseElement


class FlowElement(BaseElement):
    """
    Class used for representing tSetLane of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(FlowElement, self).__init__()
        self.__name = None

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
