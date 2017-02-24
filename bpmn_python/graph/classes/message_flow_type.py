# coding=utf-8
"""
Class used for representing tMessageFlow of BPMN 2.0 graph
"""
import graph.classes.base_element_type as base_element


class MessageFlow(base_element.BaseElement):
    """
    Class used for representing tMessageFlow of BPMN 2.0 graph
    """

    def __init__(self, source_ref, target_ref):
        """
        Default constructor, initializes object fields with new instances.
        Fields (except inherited):
        - name: name of element. Must be either None (name is optional according to BPMN 2.0 XML Schema) or String.
        - source_ref: an ID of source node. Required field. Must be a String type.
        - target_ref: an ID of target node. Required field. Must be a String type.
        - message_ref: an ID of referenced message element. Must be either None (message_ref is optional according to
        BPMN 2.0 XML Schema) or String.
        """
        if source_ref is None or not isinstance(source_ref, str):
            raise TypeError("SourceRef is required and must be set to a String")
        if target_ref is None or not isinstance(source_ref, str):
            raise TypeError("TargetRef is required and must be set to a String")

        super(MessageFlow, self).__init__()
        self.__name = None
        self.__source_ref = source_ref
        self.__target_ref = target_ref
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
        :param value - a new value of 'name' field. Must be either None (name is optional according to BPMN 2.0 XML
        Schema) or String.
        """
        if value is None:
            self.__name = value
        elif not isinstance(value, str):
            raise TypeError("Name must be set to a String")
        else:
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
        :param value - a new value of 'source_ref' field. Must be a String type.
        """
        if value is None or not isinstance(value, str):
            raise TypeError("SourceRef is required and must be set to a String")
        else:
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
        :param value - a new value of 'target_ref' field. Must be a String type.
        """
        if value is None or not isinstance(value, str):
            raise TypeError("TargetRef is required and must be set to a String")
        else:
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
        :param value - a new value of 'message_ref' field. Must be either None (message_ref is optional according to
        BPMN 2.0 XML Schema) or String.
        """
        if value is None:
            self.__message_ref = value
        if not isinstance(value, str):
            raise TypeError("MessageRef must be set to a String")
        else:
            self.__message_ref = value
