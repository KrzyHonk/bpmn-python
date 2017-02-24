# coding=utf-8
"""
Class used for representing tIntermediateThrowEvent of BPMN 2.0 graph
"""
import graph.classes.events.throw_event_type as throw_event


class IntermediateThrowEvent(throw_event.ThrowEvent):
    """
    Class used for representing tIntermediateThrowEvent of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(IntermediateThrowEvent, self).__init__()
