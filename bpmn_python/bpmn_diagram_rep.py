import networkx as nx
from xml.dom import minidom
import xml.etree.cElementTree as etree
from xml.etree import ElementTree

"""
Class BPMNDiagramGraph implements simple inner representation of BPMN 2.0 diagram, based on NetworkX graph implementation

Fields:
- diagram_graph - networkx.Graph object, stores elements of BPMN diagram as nodes. Each edge of graph represents sequenceFlow element. Edges are identified by IDs of nodes connected by edge,
- sequence_flows - dictionary (associative list) that uses sequenceFlow ID attribute as key and tuple of (sourceRef, targetRef) parameters as value. It is used to help searching edges by ID parameter,
- process_attributes - dictionary that contains BPMN process element attributes,
- diagram_attributes - dictionary that contains BPMN diagram element attributes,
- plane_attributes - dictionary that contains BPMN plane element attributes.
"""


class BPMNDiagramGraph:

    """
    Default constructor, initializes object fields with new instances.
    """
    def __init__(self):
        self.diagram_graph = nx.Graph()
        self.sequence_flows = {}
        self.process_attributes = {}
        self.diagram_attributes = {}
        self.plane_attributes = {}

    """
    Adds attributes of BPMN process element to appropriate field process_attributes.
    Diagram inner representation contains following process attributes:
    - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
    - isClosed - optional parameter, default value 'false',
    - isExecutable - optional parameter, default value 'false',
    - processType - optional parameter, default value 'None',
    """
    def add_process_attributes(self, process_element):
        self.process_attributes["id"] = process_element.getAttribute("id")
        self.process_attributes["isClosed"] = process_element.getAttribute("isClosed") if process_element.hasAttribute("isClosed") else "false"
        self.process_attributes["isExecutable"] = process_element.getAttribute("isExecutable") if process_element.hasAttribute("isExecutable") else "false"
        self.process_attributes["processType"] = process_element.getAttribute("processType") if process_element.hasAttribute("processType") else "None"

    """
    Adds attributes of BPMN diagram and plane elements to appropriate fields diagram_attributes and plane_attributes.
    Diagram inner representation contains following diagram element attributes:
    - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
    - name - optional parameter, empty string by default,
    Diagram inner representation contains following plane element attributes:
    - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
    - bpmnElement - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
    """
    def add_diagram_and_plane_attributes(self, diagram_element, plane_element):
        self.diagram_attributes["id"] = diagram_element.getAttribute("id")
        self.diagram_attributes["name"] = diagram_element.getAttribute("name") if diagram_element.hasAttribute("name") else ""

        self.plane_attributes["id"] = plane_element.getAttribute("id")
        self.plane_attributes["bpmnElement"] = plane_element.getAttribute("bpmnElement")

    """
    Adds a new node to graph.
    Input parameter is object of class xml.dom.Element.
    Nodes are identified by ID attribute of Element.
    Method adds basic attributes (shared by all BPMN elements) to node. Those elements are:
    - id - added as key value, we assume that this is a required value,
    - type - tagName of element, used to identify type of BPMN diagram element,
    - name - optional attribute, empty string by default.
    """
    def add_node_to_graph(self, element):
        elem_id = element.getAttribute("id")
        self.diagram_graph.add_node(elem_id)
        self.diagram_graph.node[elem_id]["type"] = element.tagName
        self.diagram_graph.node[elem_id]["name"] = element.getAttribute("name") if element.hasAttribute("name") else ""

    """
    Adds a new edge to graph and a record to sequence_flows dictionary.
    Input parameter is object of class xml.dom.Element.
    Edges are identified by pair of sourceRef and targetRef attributes of BPMNFlow element. We also provide a dictionary, that maps sequenceFlow ID attribute with its sourceRef and targetRef.
    Method adds basic attributes of sequenceFlow element to edge. Those elements are:
    - id - added as edge attribute, we assume that this is a required value,
    - name - optional attribute, empty string by default.
    """
    def add_edge_to_graph(self, flow):
        flow_id = flow.getAttribute("id")
        source_ref = flow.getAttribute("sourceRef")
        target_ref = flow.getAttribute("targetRef")
        self.sequence_flows[flow_id] = (source_ref, target_ref)
        self.diagram_graph.add_edge(source_ref, target_ref)
        self.diagram_graph.edge[source_ref][target_ref]["id"] = flow.getAttribute("id")
        self.diagram_graph.edge[source_ref][target_ref]["name"] = flow.getAttribute("name") if flow.hasAttribute("name") else ""

    """
    Adds Diagram Interchange information (information about rendering a diagram) to appropriate BPMN diagram element in graph node.
    We assume that those attributes are required for each BPMNShape:
    - width - width of BPMNShape,
    - height - height of BPMNShape,
    - x - first coordinate of BPMNShape,
    - y - second coordinate of BPMNShape.
    """
    def add_shape_DI(self, element_graphic):
        element_id = element_graphic.getAttribute("bpmnElement")
        bounds = element_graphic.getElementsByTagNameNS("*","Bounds")[0]
        self.diagram_graph.node[element_id]["widht"] = bounds.getAttribute("width")
        self.diagram_graph.node[element_id]["height"] = bounds.getAttribute("height")
        self.diagram_graph.node[element_id]["x"] = bounds.getAttribute("x")
        self.diagram_graph.node[element_id]["y"] = bounds.getAttribute("y")

    """
    Adds Diagram Interchange information (information about rendering a diagram) to appropriate BPMN sequence flow represented as graph edge.
    We assume that each BPMNEdge has a list of 'waypoint' elements. BPMN 2.0 XML Schema states, that each BPMNEdge must have at least two waypoints.
    """
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

"""
Reads an XML file from given filepath and maps it into inner representation of BPMN diagram.
Returns an instance of BPMNDiagramGraph class.
"""
def xml_to_inner(filepath):
    inner_rep = BPMNDiagramGraph()

    document = read_xml_file(filepath)
    process_element = document.getElementsByTagNameNS("*","process")[0] # We assume that there's only one process element
    diagram_element = document.getElementsByTagNameNS("*","BPMNDiagram")[0] # We assume that there's only one diagram element with one plane element
    plane_element = diagram_element.getElementsByTagNameNS("*","BPMNPlane")[0]

    inner_rep.add_process_attributes(process_element)
    inner_rep.add_diagram_and_plane_attributes(diagram_element, plane_element)

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

"""
Exports diagram inner graph to BPMN 2.0 XML file.
"""
def export_xml_file(diagram_inner_rep, output_path):
    root = etree.Element("definitions")
    root.set("xmlns", "http://www.omg.org/spec/BPMN/20100524/MODEL")
    root.set("xmlns:bpmndi", "http://www.omg.org/spec/BPMN/20100524/DI")
    root.set("xmlns:omgdc", "http://www.omg.org/spec/DD/20100524/DC")
    root.set("xmlns:omgdi", "http://www.omg.org/spec/DD/20100524/DI")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("targetNamespace", "http://www.signavio.com/bpmn20")
    root.set("typeLanguage", "http://www.w3.org/2001/XMLSchema")
    root.set("expressionLanguage", "http://www.w3.org/1999/XPath")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")

    process = etree.SubElement(root, "process")
    diagram = etree.SubElement(root, "bpmndi:BPMNDiagram")
    indent(root)
    tree = etree.ElementTree(root)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

"""
Helper function that iterates over child Nodes/Elements of parent Node/Element.
"""
def iterate_elements(parent):
    element = parent.firstChild
    while element is not None:
        yield element
        element = element.nextSibling

"""
Reads BPMN 2.0 XML file from given filepath and returns xml.dom.xminidom.Document object.
"""
def read_xml_file(filepath):
    dom_tree = minidom.parse(filepath)
    return dom_tree

"""
Helper function, adds indentation to XML output.
"""
def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem