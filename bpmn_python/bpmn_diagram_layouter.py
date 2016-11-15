# coding=utf-8
"""
Package with BPMNDiagramGraph - graph representation of BPMN diagram
"""


def generate_layout(bpmn_diagram):
    """
    :param bpmn_diagram: an instance of BPMNDiagramGraph class.
    """
    classification = generate_elements_clasification(bpmn_diagram)
    print("End")


def generate_elements_clasification(bpmn_diagram):
    """
    Edge Sequence flow, message flow, data flow
    Element Every element of the process which is not an edge
    Start Event All types of start events
    End Event All types of end events

    Join An element with more than one incoming edge
    Split An element with more than one outgoing edge
    :param bpmn_diagram:
    :return:
    """
    elements_classification = []
    task_list = bpmn_diagram.get_nodes("task")
    for element in task_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    subprocess_list = bpmn_diagram.get_nodes("subProcess")
    for element in subprocess_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    complex_gateway_list = bpmn_diagram.get_nodes("complexGateway")
    for element in complex_gateway_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    event_based_gateway_list = bpmn_diagram.get_nodes("eventBasedGateway")
    for element in event_based_gateway_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    inclusive_gateway_list = bpmn_diagram.get_nodes("inclusiveGateway")
    for element in inclusive_gateway_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    exclusive_gateway_list = bpmn_diagram.get_nodes("exclusiveGateway")
    for element in exclusive_gateway_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    parallel_gateway_list = bpmn_diagram.get_nodes("parallelGateway")
    for element in parallel_gateway_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    start_event_list = bpmn_diagram.get_nodes("startEvent")
    for element in start_event_list:
        tmp = {"Element", "Start Event"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    intermediate_catch_event_list = bpmn_diagram.get_nodes("intermediateCatchEvent")
    for element in intermediate_catch_event_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    end_event_list = bpmn_diagram.get_nodes("endEvent")
    for element in end_event_list:
        tmp = {"Element", "End Event"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    intermediate_throw_event_list = bpmn_diagram.get_nodes("intermediateThrowEvent")
    for element in intermediate_throw_event_list:
        tmp = {"Element"}
        if len(element[1]["incoming"]) >= 2:
            tmp.add("Join")
        if len(element[1]["outgoing"]) >= 2:
            tmp.add("Split")
        elements_classification += (element, tmp)

    edges_classification = []
    eges_list = bpmn_diagram.get_edges()
    for edge in eges_list:
        edges_classification += (edge, "Edge")

    return (elements_classification, edges_classification)


def topological_sort():
    """
    :return:
    """
    pass
