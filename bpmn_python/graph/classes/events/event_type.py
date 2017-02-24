# coding=utf-8
"""
Class used for representing tEvent of BPMN 2.0 graph
"""
import graph.classes.flow_node_type as flow_node


class Event(flow_node.FlowNode):
    """
    Class used for representing tEvent of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Event, self).__init__()
