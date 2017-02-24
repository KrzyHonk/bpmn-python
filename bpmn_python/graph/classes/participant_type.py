# coding=utf-8
"""
Class used for representing tParticipant of BPMN 2.0 graph
"""
import graph.classes.base_element_type as base_element


class Participant(base_element.BaseElement):
    """
    Class used for representing tParticipant of BPMN 2.0 graph
    Fields (except inherited):
    - name: name of element. Must be either None (name is optional according to BPMN 2.0 XML Schema) or String.
    - process_ref: an ID of referenced message element. Must be either None (process_ref is optional according to
    BPMN 2.0 XML Schema) or String.
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
        :param value - a new value of 'name' field. Must be either None (name is optional according to BPMN 2.0 XML
        Schema) or String.
        """
        if value is None:
            self.__name = value
        elif not isinstance(value, str):
            raise TypeError("Name must be set to a String")
        else:
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
        :param value - a new value of 'process_ref' field. Must be either None (process_ref is optional according to
        BPMN 2.0 XML Schema) or String.
        """
        if not isinstance(value, str):
            raise TypeError("ProcessRef must be set to a String")
        self.__process_ref = value
