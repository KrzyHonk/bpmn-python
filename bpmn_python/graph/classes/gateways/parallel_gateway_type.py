# coding=utf-8
"""
Class used for representing tParallelGateway of BPMN 2.0 graph
"""
import graph.classes.gateways.gateway_type as gateway


class ParallelGateway(gateway.Gateway):
    """
    Class used for representing tParallelGateway of BPMN 2.0 graph
    """

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        super(ParallelGateway, self).__init__()
