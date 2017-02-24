# coding=utf-8
"""
Class used for representing tActivity of BPMN 2.0 graph
"""
import graph.classes.flow_node_type as flow_node


class Activity(flow_node.FlowNode):
    """
    Class used for representing tActivity of BPMN 2.0 graph
    Fields (except inherited):
    - default: ID of default flow of gateway. Must be either None (default is optional according to BPMN 2.0 XML Schema)
    or String.
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Activity, self).__init__()
        self.__default = None

    def get_default(self):
        """
        Getter for 'default' field.
        :return:a value of 'default' field.
        """
        return self.__default

    def set_default(self, value):
        """
        Setter for 'default' field.
        :param value - a new value of 'default' field. Must be either None (default is optional according to
        BPMN 2.0 XML Schema) or String.
        """
        if value is None:
            self.__default = value
        elif not isinstance(value, str):
            raise TypeError("Default must be set to a String")
        else:
            self.__default = value
