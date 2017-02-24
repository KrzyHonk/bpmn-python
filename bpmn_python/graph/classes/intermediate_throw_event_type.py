# coding=utf-8
"""
Class used for representing tIntermediateThrowEvent of BPMN 2.0 graph
"""
from bpmn_python.graph.classes.throw_event_type import ThrowEvent


class IntermediateThrowEvent(ThrowEvent):
    """
    Class used for representing tIntermediateThrowEvent of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(IntermediateThrowEvent, self).__init__()
