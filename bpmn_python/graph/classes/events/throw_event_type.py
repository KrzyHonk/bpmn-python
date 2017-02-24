# coding=utf-8
"""
Class used for representing tThrowEvent of BPMN 2.0 graph
"""
import graph.classes.events.event_type as event
import graph.classes.root_element.event_definition_type as event_definition


class ThrowEvent(event.Event):
    """
    Class used for representing tThrowEvent of BPMN 2.0 graph
    Fields (except inherited):
    - event_definition_list: a list of EventDefinition objects. Optional value.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(ThrowEvent, self).__init__()
        self.__event_definition_list = []

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
