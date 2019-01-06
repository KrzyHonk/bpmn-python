# coding=utf-8
"""
Package provides set of functions for calculating complexity metrics
of BPMN 2.0 XML models represented by objects of BpmnDiagramGraph class.
"""

from collections import Counter

from math import sqrt

GATEWAY_TYPES = ['inclusiveGateway', 'exclusiveGateway', 'parallelGateway', 'eventBasedGateway', 'complexGateway']
EVENT_TYPES = ['startEvent', 'endEvent', 'intermediateCatchEvent', 'intermediateThrowEvent']


def get_nodes_count(bpmn_graph, node_type=None):
    """
    Gets the count of nodes of the requested type.
    If no type is provided,
    the count of all nodes in BPMN diagram graph is returned.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :param node_type: string with valid BPMN XML tag name
                      (e.g. 'task', 'sequenceFlow').
    """

    return len(bpmn_graph.get_nodes(node_type=node_type))


def get_all_gateways(bpmn_graph):
    """
    Returns a list with all gateways in diagram

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: a list with all gateways in diagram
    """
    gateways = filter(lambda node: node[1]['type'] in GATEWAY_TYPES, bpmn_graph.get_nodes())

    return gateways


def get_gateway_counts(bpmn_graph):
    """
    Returns the count of the different types of gateways
    in the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: count of the different types of gateways in the BPMNDiagramGraph instance
    """

    return {gateway_type: get_nodes_count(bpmn_graph, node_type=gateway_type)
            for gateway_type in GATEWAY_TYPES}


def get_events_counts(bpmn_graph):
    """
    Returns the count of the different types of event elements
    in the BPMNDiagramGraph instance.
    
    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: count of the different types of event elements in the BPMNDiagramGraph instance
    """

    return {event_type: get_nodes_count(bpmn_graph, node_type=event_type)
            for event_type in EVENT_TYPES}


def get_activities_counts(bpmn_graph):
    """
    Returns the count of the different types of activities
    in the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: count of the different types of activities in the BPMNDiagramGraph instance
    """

    return {
        "task": get_nodes_count(bpmn_graph,
                                node_type="task"),
        "subProcess": get_nodes_count(bpmn_graph,
                                      node_type="subProcess"),
    }


def all_activities_count(bpmn_graph):
    """
    Returns the total count of all activities in the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: total count of the activities in the BPMNDiagramGraph instance
    """

    return sum([
                   count for name, count in get_activities_counts(bpmn_graph).items()
                   ])


def all_gateways_count(bpmn_graph):
    """
    Returns the total count of all gateway elements
    in the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: total count of the gateway elements in the BPMNDiagramGraph instance
    """

    return sum([
                   count for name, count in get_gateway_counts(bpmn_graph).items()
                   ])


def all_control_flow_elements_count(bpmn_graph):
    """
    Returns the total count of all control flow elements
    in the BPMNDiagramGraph instance.
    

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: total count of the control flow elements in the BPMNDiagramGraph instance
    """

    gateway_counts = get_gateway_counts(bpmn_graph)
    events_counts = get_events_counts(bpmn_graph)
    control_flow_elements_counts = gateway_counts.copy()
    control_flow_elements_counts.update(events_counts)

    return sum([
                   count for name, count in control_flow_elements_counts.items()
                   ])


def all_events_count(bpmn_graph):
    """
    Returns the total count of all events elements
    in the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    :return: total count of the events elements elements in the BPMNDiagramGraph instance
    """

    return sum([
                   count for name, count in get_events_counts(bpmn_graph).items()
                   ])


def TNSE_metric(bpmn_graph):
    """
    Returns the value of the TNSE metric (Total Number of Start Events of the Model)
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    return get_nodes_count(bpmn_graph, node_type='startEvent')


def TNIE_metric(bpmn_graph):
    """
    Returns the value of the TNIE metric (Total Number of Intermediate Events of the Model)
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    return get_nodes_count(bpmn_graph, node_type='intermediateCatchEvent') + \
           get_nodes_count(bpmn_graph, node_type='intermediateThrowEvent')


def TNEE_metric(bpmn_graph):
    """
    Returns the value of the TNEE metric (Total Number of End Events of the Model)
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    return get_nodes_count(bpmn_graph, node_type='endEvent')


def TNE_metric(bpmn_graph):
    """
    Returns the value of the TNE metric (Total Number of Events of the Model)
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    events_counts = get_events_counts(bpmn_graph)

    return sum(
        [count for _, count in events_counts.items()]
    )


def NOA_metric(bpmn_graph):
    """
    Returns the value of the NOA metric (Number of Activities)
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    activities_counts = get_activities_counts(bpmn_graph)

    return activities_counts["task"] + activities_counts["subProcess"]


def NOAC_metric(bpmn_graph):
    """
    Returns the value of the NOAC metric (Number of Activities and control flow elements)
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    activities_count = all_activities_count(bpmn_graph)
    control_flow_count = all_control_flow_elements_count(bpmn_graph)

    return activities_count + control_flow_count


def NOAJS_metric(bpmn_graph):
    """
    Returns the value of the NOAJS metric (Number of Activities, joins and splits)
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    activities_count = all_activities_count(bpmn_graph)
    gateways_count = all_gateways_count(bpmn_graph)

    return activities_count + gateways_count


def NumberOfNodes_metric(bpmn_graph):
    """
    Returns the value of the Number of Nodes metric
    ("Number of activities and routing elements in a model")
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    activities_count = all_activities_count(bpmn_graph)
    control_flow_count = all_control_flow_elements_count(bpmn_graph)

    return activities_count + control_flow_count


def GatewayHeterogenity_metric(bpmn_graph):
    """
    Returns the value of the Gateway Heterogenity metric
    ("Number of different types of gateways used in a mode")
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    gateway_counts = get_gateway_counts(bpmn_graph)
    present_gateways = [gateway_name
                        for gateway_name, count in gateway_counts.items()
                        if count > 0]

    return len(present_gateways)


def CoefficientOfNetworkComplexity_metric(bpmn_graph):
    """
    Returns the value of the Coefficient of Network Complexity metric
    ("Ratio of the total number of arcs in a process model to its total number of nodes.")
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    return float(len(bpmn_graph.get_flows())) / float(len(bpmn_graph.get_nodes()))


def AverageGatewayDegree_metric(bpmn_graph):
    """
    Returns the value of the Average Gateway Degree metric
    ("Average of the number of both incoming and outgoing arcs of the gateway nodes in the process model")
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    gateways_ids = [gateway[0] for gateway in get_all_gateways(bpmn_graph)]
    all_nodes_degrees = bpmn_graph.diagram_graph.degree()
    gateways_degree_values = [all_nodes_degrees[gateway_id] for gateway_id in gateways_ids]

    return float(sum(gateways_degree_values)) / float(len(gateways_degree_values))


def DurfeeSquare_metric(bpmn_graph):
    """
    Returns the value of the Durfee Square metric
     ("Durfee Square equals d if there are d types of elements
     which occur at least d times in the model (each),
     and the other types of elements occur no more than d times (each)")
     for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    all_types_count = Counter([node[1]['type'] for node in bpmn_graph.get_nodes() if node[1]['type']])
    length = len(all_types_count)

    histogram = [0] * (length + 1)
    for _, count in all_types_count.items():
        histogram[min(count, length)] += 1

    sum_ = 0
    for i, count in reversed(list(enumerate(histogram))):
        sum_ += count
        if sum_ >= i:
            return i

    return 0


def PerfectSquare_metric(bpmn_graph):
    """
    Returns the value of the Perfect Square metric
    ("Given a set of element types ranked
    in decreasing order of the number of their instances,
    the PSM is the (unique) largest number
    such that the top p types occur(together)
    at least p2 times.")
    for the BPMNDiagramGraph instance.

    :param bpmn_graph: an instance of BpmnDiagramGraph representing BPMN model.
    """

    all_types_count = Counter([node[1]['type'] for node in bpmn_graph.get_nodes() if node[1]['type']])
    sorted_counts = [count for _, count in all_types_count.most_common()]

    potential_perfect_square = min(len(sorted_counts), int(sqrt(sum(sorted_counts))))

    for i in range(potential_perfect_square, 0, -1):
        if sum(sorted_counts[:potential_perfect_square]) >= potential_perfect_square * potential_perfect_square:
            return potential_perfect_square
        else:
            potential_perfect_square -= 1

    return 0
