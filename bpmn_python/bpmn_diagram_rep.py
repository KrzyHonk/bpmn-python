import networkx as nx
import bpmn_python.xml_reader as reader

class BPMNDiagramGraph:
    def __init__(self):
        self.diagram_graph = nx.Graph() # nx.Graph(), each node represents a BPMN element, edge - represents flow
        self.sequence_flows = {} # dictonary helper, key - sequence flows ID, values - sourceRef, target_ref

    def add_node_to_graph(self, element):
        elem_id = element.getAttribute("id")
        self.diagram_graph.add_node(elem_id)
        self.diagram_graph.node[elem_id]["type"] = element.tagName
        self.diagram_graph.node[elem_id]["name"] = element.getAttribute("name") if element.hasAttribute("name") else ""

    def add_edge_to_graph(self, flow):
        flow_id = flow.getAttribute("id")
        source_ref = flow.getAttribute("sourceRef")
        target_ref = flow.getAttribute("targetRef")
        self.sequence_flows[flow_id] = (source_ref, target_ref)
        self.diagram_graph.add_edge(source_ref, target_ref)
        self.diagram_graph.edge[source_ref][target_ref]["id"] = flow.getAttribute("id")
        self.diagram_graph.edge[source_ref][target_ref]["name"] = flow.getAttribute("name") if flow.hasAttribute("name") else ""

    def add_shape_DI(self, element_graphic):
        element_id = element_graphic.getAttribute("bpmnElement")
        bounds = element_graphic.getElementsByTagNameNS("*","Bounds")[0]
        self.diagram_graph.node[element_id]["widht"] = bounds.getAttribute("width")
        self.diagram_graph.node[element_id]["height"] = bounds.getAttribute("height")
        self.diagram_graph.node[element_id]["x"] = bounds.getAttribute("x")
        self.diagram_graph.node[element_id]["y"] = bounds.getAttribute("y")

    def add_edge_DI(self, flow_graphic):
        flow_id = flow_graphic.getAttribute("bpmnElement")
        waypoints_xml = flow_graphic.getElementsByTagNameNS("*","waypoint")
        length = len(waypoints_xml)
        waypoints = [None] * length
        for index in range(length):
            waypoint_tmp = (waypoints_xml[index].getAttribute("x"), waypoints_xml[index].getAttribute("y"))
            waypoints[index] = waypoint_tmp
        (source_ref, target_ref) = self.sequence_flows[flow_id]
        self.diagram_graph.edge[source_ref][target_ref]["waypoints"] = waypoints

def xml_to_inner(filepath):
    inner_rep = BPMNDiagramGraph()

    document = reader.readXmlFile(filepath)
    process_element = document.getElementsByTagNameNS("*","process")[0] # We assume that there's only one process element
    plane_element = document.getElementsByTagNameNS("*","BPMNDiagram")[0].getElementsByTagNameNS("*","BPMNPlane")[0] # We assume that there's only one diagram element with one plne element

    for element in iterate_elements(process_element):
        if element.nodeType != element.TEXT_NODE:
            tag_name = element.tagName.split(':')[-1] # Removing namespace from tag name
            if tag_name == "task":
                inner_rep.add_node_to_graph(element)
            elif tag_name == "startEvent" or tag_name == "endEvent":
                inner_rep.add_node_to_graph(element)
            elif tag_name == "intermediateThrowEvent" or tag_name == "intermediateCatchEvent":
                inner_rep.add_node_to_graph(element)
            elif tag_name == "parallelGateway" or tag_name == "inclusiveGateway" or tag_name == "exclusiveGateway":
                inner_rep.add_node_to_graph(element)

    for flow in iterate_elements(process_element):
        if flow.nodeType != flow.TEXT_NODE:
            tag_name = flow.tagName
            if tag_name == "sequenceFlow":
                inner_rep.add_edge_to_graph(flow)

    for element in iterate_elements(plane_element):
        if element.nodeType != element.TEXT_NODE:
            tag_name = element.tagName.split(':')[-1] # Removing namespace from tag name
            if tag_name == "BPMNShape":
                inner_rep.add_shape_DI(element)
            elif tag_name == "BPMNEdge":
                inner_rep.add_edge_DI(element)

    return inner_rep

def iterate_elements(parent):
    element = parent.firstChild
    while element is not None:
        yield element
        element = element.nextSibling