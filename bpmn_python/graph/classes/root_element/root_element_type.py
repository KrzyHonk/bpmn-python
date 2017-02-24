# coding=utf-8
"""
Class used for representing tRootElement of BPMN 2.0 graph
"""
import graph.classes.base_element_type as base_element


class RootElement(base_element.BaseElement):
    """
    Class used for representing tRootElement of BPMN 2.0 graph.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(RootElement, self).__init__()
