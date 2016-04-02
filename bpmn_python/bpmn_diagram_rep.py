import networkx as nx
import bpmn_python.xml_reader as reader

class BPMNDiagramGraph:
    def __init__(self):
        self.diagram_graph = None

    def iterate_elements(self, parent):
        element = parent.firstChild
        while element is not None:
            yield element
            element = element.nextSibling

    def add_node_to_graph(self, element):
        elemID = element.getAttribute("id")
        self.diagram_graph.add_node(elemID)
        self.diagram_graph.node[elemID]["type"] = element.tagName
        self.diagram_graph.node[elemID]["name"] = element.getAttribute("name") if element.hasAttribute("name") else ""

    def add_edge_to_graph(self, flow):
        sourceRef = flow.getAttribute("sourceRef")
        targetRef = flow.getAttribute("targetRef")
        self.diagram_graph.add_edge(sourceRef, targetRef)
        self.diagram_graph.edge[sourceRef][targetRef]["id"] = flow.getAttribute("id")
        self.diagram_graph.edge[sourceRef][targetRef]["name"] = flow.getAttribute("name") if flow.hasAttribute("name") else ""

def xml_to_inner(filepath):
    inner_rep = BPMNDiagramGraph()
    inner_rep.diagram_graph = nx.Graph()

    document = reader.readXmlFile(filepath)
    processElement = document.getElementsByTagNameNS("*","process")[0] # We assume that there's only one process element
    diagramElement = document.getElementsByTagNameNS("*","BPMNDiagram")[0] # We assume that there's only one diagram element

    for element in inner_rep.iterate_elements(processElement):
        if element.nodeType != element.TEXT_NODE:
            tag_name = element.tagName
            if tag_name == "task":
                inner_rep.add_node_to_graph(element)
            elif tag_name == "startEvent" or tag_name == "endEvent":
                inner_rep.add_node_to_graph(element)
            elif tag_name == "intermediateThrowEvent" or tag_name == "intermediateCatchEvent":
                inner_rep.add_node_to_graph(element)
            elif tag_name == "parallelGateway" or tag_name == "inclusiveGateway" or tag_name == "exclusiveGateway":
                inner_rep.add_node_to_graph(element)

    for flow in inner_rep.iterate_elements(processElement):
        if flow.nodeType != flow.TEXT_NODE:
            tag_name = flow.tagName
            if tag_name == "sequenceFlow":
                inner_rep.add_edge_to_graph(flow)

    return inner_rep

