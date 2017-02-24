# coding=utf-8
"""
Class used for representing tGateway of BPMN 2.0 graph
"""
import graph.classes.flow_node_type as flow_node


class Gateway(flow_node.FlowNode):
    """
    Class used for representing tGateway of BPMN 2.0 graph
    """
    __gateway_directions_list = ["Unspecified", "Converging", "Diverging", "Mixed"]

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(Gateway, self).__init__()
        self.__gateway_direction = "Unspecified"

    def get_gateway_direction(self):
        """
        Getter for 'gateway_direction' field.
        :return:a value of 'gateway_direction' field.
        """
        return self.__gateway_direction

    def set_gateway_direction(self, value):
        """
        Setter for 'gateway_direction' field.
        :param value - a new value of 'gateway_direction' field.
        """
        if value is None or not isinstance(value, str):
            raise TypeError("GatewayDirection must be set to a String")
        elif value not in Gateway.__gateway_directions_list:
            raise ValueError("GatewayDirection must be one of specified values: 'Unspecified', 'Converging', "
                             "'Diverging', 'Mixed'")
        else:
            self.__gateway_direction = value
