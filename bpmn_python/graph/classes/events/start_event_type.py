# coding=utf-8
"""
Class used for representing tStartEvent of BPMN 2.0 graph
"""
import graph.classes.events.catch_event_type as catch_event


class StartEvent(catch_event.CatchEvent):
    """
    Class used for representing tStartEvent of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(StartEvent, self).__init__()
