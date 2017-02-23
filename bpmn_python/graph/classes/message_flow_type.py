# coding=utf-8
"""
Class used for representing tMessageFlow of BPMN 2.0 graph
"""

from bpmn_python.graph.classes.base_element_type import BaseElement


class MessageFlow(BaseElement):
    """
    Class used for representing tMessageFlow of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(MessageFlow, self).__init__()
        self.__name = None
        self.__source_ref = None
        self.__target_ref = None
        self.__message_ref = None

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

    def get_source_ref(self):
        """
        Getter for 'source_ref' field.
        :return: value of 'source_ref' field.
        """
        return self.__source_ref

    def set_source_ref(self, value):
        """
        Setter for 'source_ref' field.
        :param value - a new value of 'source_ref' field.
        """
        if not None and not isinstance(value, str):
            raise TypeError("SourceRef is required and must be set to a string")
        self.__source_ref = value

    def get_target_ref(self):
        """
        Getter for 'target_ref' field.
        :return: value of 'target_ref' field.
        """
        return self.__target_ref

    def set_target_ref(self, value):
        """
        Setter for 'target_ref' field.
        :param value - a new value of 'target_ref' field.
        """
        if not None and not isinstance(value, str):
            raise TypeError("TargetRef is required and must be set to a string")
        self.__target_ref = value

    def get_message_ref(self):
        """
        Getter for 'message_ref' field.
        :return: value of 'message_ref' field.
        """
        return self.__message_ref

    def set_message_ref(self, value):
        """
        Setter for 'message_ref' field.
        :param value - a new value of 'message_ref' field.
        """
        if not isinstance(value, str):
            raise TypeError("MessageRef must be set to a string")
        self.__message_ref = value
