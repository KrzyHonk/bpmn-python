# coding=utf-8
"""
Class used for representing tCallableElement of BPMN 2.0 graph
"""
import graph.classes.root_element.root_element_type as root_element


class CallableElement(root_element.RootElement):
    """
    Class used for representing tCallableElement of BPMN 2.0 graph.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(CallableElement, self).__init__()
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
        :param value - a new value of 'name' field. Must be either None (name is optional according to BPMN 2.0 XML
        Schema) or String.
        """
        if value is None:
            self.__name = value
        elif not isinstance(value, str):
            raise TypeError("Name must be set to a String")
        else:
            self.__name = value
