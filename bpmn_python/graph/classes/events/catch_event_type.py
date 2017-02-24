# coding=utf-8
"""
Class used for representing tCatchEvent of BPMN 2.0 graph
"""
import graph.classes.events.event_type as event
import graph.classes.root_element.event_definition_type as event_definition


class CatchEvent(event.Event):
    """
    Class used for representing tCatchEvent of BPMN 2.0 graph
    Fields (except inherited):
    - parallel_multiple: a boolean value. default value "false".
    - event_definition_list: a list of EventDefinition objects. Optional value.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(CatchEvent, self).__init__()
        self.__parallel_multiple = False
        self.__event_definition_list = []

    def parallel_multiple(self):
        """
        Getter for 'parallel_multiple' field.
        :return: value of 'parallel_multiple' field.
        """
        return self.__parallel_multiple

    def set_parallel_multiple(self, value):
        """
        Setter for 'parallel_multiple' field.
        :param value - a new value of 'parallel_multiple' field. Must be a boolean type. Does not accept None value.
        """
        if value is None or not isinstance(value, bool):
            raise TypeError("ParallelMultiple must be set to a bool")
        else:
            self.__parallel_multiple = value

    def get_event_definition_list(self):
        """
        Getter for 'event_definition_list' field.
        :return: value of 'event_definition_list' field.
        """
        return self.__event_definition_list

    def set_event_definition_list(self, value):
        """
        Setter for 'event_definition_list' field.
        :param value - a new value of 'event_definition_list' field. Must be a list of EventDefinition objects
        """
        if value is None or not isinstance(value, list):
            raise TypeError("EventDefinitionList new value must be a list")
        else:
            for element in value:
                if not isinstance(element, event_definition.EventDefinition):
                    raise TypeError("EventDefinitionList elements in variable must be of Lane class")
            self.__event_definition_list = value
