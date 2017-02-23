# coding=utf-8
"""
Class used for representing tBaseElement of BPMN 2.0 graph
"""


class BaseElement(object):
    """
    Class used for representing tBaseElement of BPMN 2.0 graph.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        self.__id = None

    def get_id(self):
        """
        Getter for 'id' field.
        :return:a value of 'id' field.
        """
        return self.__id

    def set_id(self, value):
        """
        Setter for 'id' field.
        :param value - a new value of 'id' field.
        """
        if not isinstance(value, str):
            raise TypeError("ID must be set to a string")
        self.__id = value
