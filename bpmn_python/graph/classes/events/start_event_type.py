# coding=utf-8
"""
Class used for representing tStartEvent of BPMN 2.0 graph
"""
from graph.classes.events.catch_event_type import CatchEvent


class StartEvent(CatchEvent):
    """
    Class used for representing tStartEvent of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(StartEvent, self).__init__()
