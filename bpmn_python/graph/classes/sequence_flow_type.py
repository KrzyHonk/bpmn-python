# coding=utf-8
"""
Class used for representing tSequenceFlow of BPMN 2.0 graph
"""
import graph.classes.condition_expression_type as condition_expression
import graph.classes.flow_element_type as flow_element


class SequenceFlow(flow_element.FlowElement):
    """
    Class used for representing tSequenceFlow of BPMN 2.0 graph.
    Fields (except inherited):
    - source_ref: an ID of source node. Required field. Must be a String type.
    - target_ref: an ID of target node. Required field. Must be a String type.
    - condition_expression: an expression used as condition of flow (conditional flow). Must be either None
    (condition_expression is optional according to BPMN 2.0 XML Schema) or String.
    - is_immediate: a boolean value.
    """

    def __init__(self, source_ref, target_ref):
        """
        Default constructor, initializes object fields with new instances.
        """
        if source_ref is None or not isinstance(source_ref, str):
            raise TypeError("SourceRef is required and must be set to a String")
        if target_ref is None or not isinstance(source_ref, str):
            raise TypeError("TargetRef is required and must be set to a String")

        super(SequenceFlow, self).__init__()
        self.__source_ref = source_ref
        self.__target_ref = target_ref
        self.__condition_expression = None
        self.__is_immediate = None

    def get_source_ref(self):
        """
        Getter for 'source_ref' field.
        :return: value of 'source_ref' field.
        """
        return self.__source_ref

    def set_source_ref(self, value):
        """
        Setter for 'source_ref' field.
        :param value - a new value of 'source_ref' field. Required field. Must be a String type.
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
        :param value - a new value of 'target_ref' field. Required field. Must be a String type.
        """
        if value is None or not isinstance(value, str):
            raise TypeError("TargetRef is required and must be set to a String")
        else:
            self.__target_ref = value

    def is_immediate(self):
        """
        Getter for 'is_immediate' field.
        :return: value of 'is_immediate' field.
        """
        return self.__is_immediate

    def set_is_immediate(self, value):
        """
        Setter for 'is_immediate' field.
        :param value - a new value of 'is_immediate' field. Must be a boolean type.
        """
        if value is None:
            self.__is_immediate = value
        elif not isinstance(value, bool):
            raise TypeError("IsImediate must be set to a bool")
        else:
            self.__is_immediate = value

    def get_condition_expression(self):
        """
        Getter for 'condition_expression' field.
        :return: value of 'condition_expression' field. Must be either None (condition_expression is optional according
        to BPMN 2.0 XML Schema) or String.
        """
        return self.__condition_expression

    def set_condition_expression(self, value):
        """
        Setter for 'condition_expression' field.
        :param value - a new value of 'condition_expression' field.
        """
        if value is None:
            self.__condition_expression = value
        if not isinstance(value, condition_expression.ConditionExpression):
            raise TypeError("ConditionExpression must be set to an instance of class ConditionExpression")
        else:
            self.__condition_expression = value
