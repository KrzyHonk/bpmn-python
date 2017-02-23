# coding=utf-8
"""
Class used for representing tParticipant of BPMN 2.0 graph
"""
from bpmn_python.graph.classes.base_element_type import BaseElement


class Participant(BaseElement):
    """
    Class used for representing tParticipant of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Participant, self).__init__()
        self.__name = None
        self.__process_ref = None

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

    def get_process_ref(self):
        """
        Getter for 'process_ref' field.
        :return:a value of 'process_ref' field.
        """
        return self.__process_ref

    def set_process_ref(self, value):
        """
        Setter for 'process_ref' field.
        :param value - a new value of 'process_ref' field.
        """
        if not isinstance(value, str):
            raise TypeError("ProcessRef must be set to a string")
        self.__process_ref = value
