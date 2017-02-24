# coding=utf-8
"""
Class used for representing tEventDefinition of BPMN 2.0 graph
"""
from graph.classes.root_element.root_element_type import RootElement


class EventDefinition(RootElement):
    """
    Class used for representing tEventDefinition of BPMN 2.0 graph.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(EventDefinition, self).__init__()
