import networkx as nx
from xml.dom import minidom
import xml.etree.cElementTree as etree

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
    def add_flownode_to_graph(self, element, element_id):
        self.diagram_graph.add_node(element_id)
        self.diagram_graph.node[element_id]["type"] = remove_namespace_from_tag_name(element.tagName)
        self.diagram_graph.node[element_id]["name"] = element.getAttribute("name") if element.hasAttribute("name") else ""

        # add incoming flow node list
        incoming_xml = element.getElementsByTagNameNS("*","incoming")
        length = len(incoming_xml)
        incoming_list = [None] * length
        for index in range(length):
            incoming_tmp = incoming_xml[index].firstChild.nodeValue
            incoming_list[index] = incoming_tmp
        self.diagram_graph.node[element_id]["incoming"] = incoming_list

        # add outgoing flow node list
        outgoing_xml = element.getElementsByTagNameNS("*","outgoing")
        length = len(outgoing_xml)
        outgoing_list = [None] * length
        for index in range(length):
            outgoing_tmp = outgoing_xml[index].firstChild.nodeValue
            outgoing_list[index] = outgoing_tmp
        self.diagram_graph.node[element_id]["outgoing"] = outgoing_list

    """
    Adds to graph the new element that represents BPMN task.
    In our representation tasks have only basic attributes and elements, inherited from Activity type, so this method only needs to call add_flownode_to_graph.
    """
    def add_task_to_graph(self, element, element_id):
        self.add_flownode_to_graph(element, element_id)

    """
    Adds to graph the new element that represents BPMN subprocess.
    In addition to attributes inherited from FlowNode type, SubProcess has additional attribute tiggeredByEvent (boolean type, default value - false).
    """
    def add_subprocess_to_graph(self, element, element_id):
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["triggeredByEvent"] = element.getAttribute("triggeredByEvent") if element.hasAttribute("triggeredByEvent") else "false"

    """
    Adds to graph the new element that represents BPMN gateway.
    In addition to attributes inherited from FlowNode type, Gateway has additional attribute gatewayDirection (simple type, default value - Unspecified).
    """
    def add_gateway_to_graph(self, element, element_id):
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["gatewayDirection"] = element.getAttribute("gatewayDirection") if element.hasAttribute("gatewayDirection") else "Unspecified"

    """
    Adds to graph the new element that represents BPMN complex gateway.
    In addition to attributes inherited from Gateway type, complex gateway has additional attribute default flow (default value - none).
    """
    def add_complex_gateway_to_graph(self, element, element_id):
        self.add_gateway_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["default"] = element.getAttribute("default") if element.hasAttribute("default") else None
        # TODO sequence of conditions
        # Can't get any working example of Complex gateway, so I'm not sure how exactly those conditions are kept

    """
    Adds to graph the new element that represents BPMN event based gateway.
    In addition to attributes inherited from Gateway type, event based gateway has additional attributes instantiate (boolean type, default value - false) and eventGatewayType (custom type tEventBasedGatewayType, default value - Exclusive).
    """
    def add_event_based_gateway_to_graph(self, element, element_id):
        self.add_gateway_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["instantiate"] = element.getAttribute("instantiate") if element.hasAttribute("instantiate") else "false"
        self.diagram_graph.node[element_id]["eventGatewayType"] = element.getAttribute("eventGatewayType") if element.hasAttribute("eventGatewayType") else "Exclusive"

    """
    Adds to graph the new element that represents BPMN inclusive or eclusive gateway.
    In addition to attributes inherited from Gateway type, inclusive and exclusive gateway have additional attribute default flow (default value - none).
    """
    def add_inclusive_or_exclusive_gateway_to_graph(self, element, element_id):
        self.add_gateway_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["default"] = element.getAttribute("default") if element.hasAttribute("default") else None

    """
    Adds to graph the new element that represents BPMN parallel gateway.
    Parallel gateway doesn't have additional attributes. Separate method is used to improve code readability.
    """
    def add_parallel_gateway_to_graph(self, element, element_id):
        self.add_gateway_to_graph(element, element_id)

    """
    Adds to graph the new element that represents BPMN start event.
    Start event inherits attribute parallelMultiple from CatchEvent type and sequence of eventDefinitionRef from Event type.
    Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).
    """
    def add_start_event_to_graph(self, element, element_id):
        start_event_definitions = {'messageEventDefinition', 'timerEventDefinition', 'conditionalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["parallelMultiple"] = element.getAttribute("parallelMultiple") if element.hasAttribute("parallelMultiple") else "false"

        # TODO Repeated code
        # add event definitions elements
        event_def_list = []
        for definition_type in start_event_definitions:
            event_def_xml = element.getElementsByTagNameNS("*",definition_type)
            length = len(event_def_xml)
            for index in range(length):
                event_def_tmp = (definition_type, event_def_xml[index].getAttribute("id")) # tuple - definition type, definition id
                event_def_list.append(event_def_tmp)
        self.diagram_graph.node[element_id]["event_definitions"] = event_def_list

    """
    Adds to graph the new element that represents BPMN intermediate catch event.
    Intermediate catch event inherits attribute parallelMultiple from CatchEvent type and sequence of eventDefinitionRef from Event type.
    Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).
    """
    def add_intermediate_catch_event_to_graph(self, element, element_id):
        intermediate_catch_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'conditionalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["parallelMultiple"] = element.getAttribute("parallelMultiple") if element.hasAttribute("parallelMultiple") else "false"

        # TODO Repeated code
        # add event definitions elements
        event_def_list = []
        for definition_type in intermediate_catch_event_definitions:
            event_def_xml = element.getElementsByTagNameNS("*",definition_type)
            length = len(event_def_xml)
            for index in range(length):
                event_def_tmp = (definition_type, event_def_xml[index].getAttribute("id")) # tuple - definition type, definition id
                event_def_list.append(event_def_tmp)
        self.diagram_graph.node[element_id]["event_definitions"] = event_def_list

    """
    Adds to graph the new element that represents BPMN end event.
    End event inherits sequence of eventDefinitionRef from Event type.
    Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).
    """
    def add_end_event_to_graph(self, element, element_id):
        end_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)

        # TODO Repeated code
        # add event definitions elements
        event_def_list = []
        for definition_type in end_event_definitions:
            event_def_xml = element.getElementsByTagNameNS("*",definition_type)
            length = len(event_def_xml)
            for index in range(length):
                event_def_tmp = (definition_type, event_def_xml[index].getAttribute("id")) # tuple - definition type, definition id
                event_def_list.append(event_def_tmp)
        self.diagram_graph.node[element_id]["event_definitions"] = event_def_list

    """
    Adds to graph the new element that represents BPMN intermediate throw event.
    Intermediate throw event inherits sequence of eventDefinitionRef from Event type.
    Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).
    """
    def add_intermediate_throw_event_to_graph(self, element, element_id):
        intermediate_throw_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)

        # TODO Repeated code
        # add event definitions elements
        event_def_list = []
        for definition_type in intermediate_throw_event_definitions:
            event_def_xml = element.getElementsByTagNameNS("*",definition_type)
            length = len(event_def_xml)
            for index in range(length):
                event_def_tmp = (definition_type, event_def_xml[index].getAttribute("id")) # tuple - definition type, definition id
                event_def_list.append(event_def_tmp)
        self.diagram_graph.node[element_id]["event_definitions"] = event_def_list

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
        self.diagram_graph.node[element_id]["width"] = bounds.getAttribute("width")
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
            tag_name = remove_namespace_from_tag_name(element.tagName)
            if tag_name == "task":
                inner_rep.add_task_to_graph(element, element.getAttribute("id"))
            elif tag_name == "subProcess":
                inner_rep.add_subprocess_to_graph(element, element.getAttribute("id"))
            elif tag_name == "inclusiveGateway" or tag_name == "exclusiveGateway":
                inner_rep.add_inclusive_or_exclusive_gateway_to_graph(element, element.getAttribute("id"))
            elif tag_name == "parallelGateway":
                inner_rep.add_parallel_gateway_to_graph(element, element.getAttribute("id"))
            elif tag_name == "eventBasedGateway":
                inner_rep.add_event_based_gateway_to_graph(element, element.getAttribute("id")) # TODO test this
            elif tag_name == "complexGateway":
                inner_rep.add_complex_gateway_to_graph(element, element.getAttribute("id")) # TODO test this
            elif tag_name == "startEvent":
                inner_rep.add_start_event_to_graph(element, element.getAttribute("id")) # TODO test this
            elif tag_name == "endEvent":
                inner_rep.add_end_event_to_graph(element, element.getAttribute("id")) # TODO test this
            elif tag_name == "intermediateCatchEvent":
                inner_rep.add_intermediate_catch_event_to_graph(element, element.getAttribute("id")) # TODO test this
            elif tag_name == "intermediateThrowEvent":
                inner_rep.add_intermediate_throw_event_to_graph(element, element.getAttribute("id")) # TODO test this

    for flow in iterate_elements(process_element):
        if flow.nodeType != flow.TEXT_NODE:
            tag_name = remove_namespace_from_tag_name(flow.tagName)
            if tag_name == "sequenceFlow":
                inner_rep.add_edge_to_graph(flow)

    for element in iterate_elements(plane_element):
        if element.nodeType != element.TEXT_NODE:
            tag_name = remove_namespace_from_tag_name(element.tagName)
            if tag_name == "BPMNShape":
                inner_rep.add_shape_DI(element)
            elif tag_name == "BPMNEdge":
                inner_rep.add_edge_DI(element)

    return inner_rep

"""
Adds Task node attributes to exported XML element
"""
def export_task_info(node_params, output_element):
    pass

"""
Adds Subprocess node attributes to exported XML element
"""
def export_subprocess_info(node_params, output_element):
    output_element.set("triggeredByEvent", node_params["triggeredByEvent"])

"""
Adds ComplexGateway node attributes to exported XML element
"""
# TODO Conditions
def export_complex_gateway_info(node_params, output_element):
    # TODO Repeated for every gateway info export. Clean this up
    output_element.set("gatewayDirection", node_params["gatewayDirection"])
    if node_params["default"] != None:
         output_element.set("default", node_params["default"])

"""
Adds EventBasedGateway node attributes to exported XML element
"""
def export_event_based_gateway_info(node_params, output_element):
    # TODO Repeated for every gateway info export. Clean this up
    output_element.set("gatewayDirection", node_params["gatewayDirection"])
    output_element.set("instantiate", node_params["instantiate"])
    output_element.set("eventGatewayType", node_params["eventGatewayType"])

"""
Adds InclusiveGateway or ExclusiveGateway node attributes to exported XML element
"""
def export_inclusive_exclusive_gateway_info(node_params, output_element):
    # TODO Repeated for every gateway info export. Clean this up
    output_element.set("gatewayDirection", node_params["gatewayDirection"])
    if node_params["default"] != None:
         output_element.set("default", node_params["default"])

"""
Adds Subprocess node attributes to exported XML element
"""
def export_parallel_gateway_info(node_params, output_element):
    # TODO Repeated for every gateway info export. Clean this up
    output_element.set("gatewayDirection", node_params["gatewayDirection"])

"""
Adds StartEvent or IntermediateCatchEvent attributes to exported XML element
"""
def export_catch_event_info(node_params, output_element):
    output_element.set("parallelMultiple", node_params["parallelMultiple"])
    definitions = node_params["event_definitions"]
    for definition in definitions:
        definition_type = definition[0]
        definition_id = definition[1]
        output_definition = etree.SubElement(output_element, definition_type)
        if definition_id != "":
            output_definition.set("id", definition_id)

"""
Adds EndEvent or IntermediateThrowingEvent attributes to exported XML element
"""
def export_throw_event_info(node_params, output_element):
    definitions = node_params["event_definitions"]
    for definition in definitions:
        definition_type = definition[0]
        definition_id = definition[1]
        output_definition = etree.SubElement(output_element, definition_type)
        if definition_id != "":
            output_definition.set("id", definition_id)

"""
Exports diagram inner graph to BPMN 2.0 XML file.
"""
def export_xml_file(diagram_inner_rep, output_path):
    bpmndi_namespace = "bpmndi:"

    # Create root 'definitons' element and add required attirbutes
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

    # Create 'process' element and add attirbutes
    process = etree.SubElement(root, "process")
    process.set("id", diagram_inner_rep.process_attributes["id"])
    process.set("isClosed", diagram_inner_rep.process_attributes["isClosed"])
    process.set("isExecutable", diagram_inner_rep.process_attributes["isExecutable"])
    process.set("processType", diagram_inner_rep.process_attributes["processType"])

    # Create 'diagram' element and add attirbutes
    diagram = etree.SubElement(root, bpmndi_namespace + "BPMNDiagram")
    diagram.set("id", diagram_inner_rep.diagram_attributes["id"])
    diagram.set("name", diagram_inner_rep.diagram_attributes["name"])

    # Create 'plane' element and add attirbutes
    plane = etree.SubElement(diagram, bpmndi_namespace + "BPMNPlane")
    plane.set("id", diagram_inner_rep.plane_attributes["id"])
    plane.set("bpmnElement", diagram_inner_rep.plane_attributes["bpmnElement"])

    # for each node in graph add correct type of element, its attributes and BPMNShape element
    nodes = diagram_inner_rep.diagram_graph.nodes(data=True)
    for node in nodes:
        id = node[0]
        params = node[1]
        node_type = params["type"]
        output_element = etree.SubElement(process, node_type)
        output_element.set("id", id)
        output_element.set("name", params["name"])

        for incoming in params["incoming"]:
            incoming_element = etree.SubElement(output_element, "incoming")
            incoming_element.text = incoming
        for outgoing in params["outgoing"]:
            outgoing_element = etree.SubElement(output_element, "outgoing")
            outgoing_element.text = outgoing

        if node_type == "task":
            export_task_info(params, output_element)
        elif node_type == "subProcess":
            export_subprocess_info(params, output_element)
        elif node_type == "complexGateway":
            export_complex_gateway_info(params, output_element)
        elif node_type == "eventBasedGateway":
            export_event_based_gateway_info(params, output_element)
        elif node_type == "inclusiveGateway" or node_type == "exclusiveGateway":
            export_inclusive_exclusive_gateway_info(params, output_element)
        elif node_type == "parallelGateway":
            export_parallel_gateway_info(params, output_element)
        elif node_type == "startEvent" or node_type == "intermediateCatchEvent":
            export_catch_event_info(params, output_element)
        elif node_type == "endEvent" or node_type == "intermediateThrowEvent":
            export_throw_event_info(params, output_element)

        output_element_di = etree.SubElement(plane, bpmndi_namespace + "BPMNShape")
        output_element_di.set("id", id + "_gui")
        output_element_di.set("bpmnElement", id)
        bounds = etree.SubElement(output_element_di, "omgdc:Bounds")
        bounds.set("width", params["width"])
        bounds.set("height", params["height"])
        bounds.set("x", params["x"])
        bounds.set("y", params["y"])

    # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
    edges = diagram_inner_rep.diagram_graph.edges(data=True)
    for flow in edges:
        params = flow[2]
        (sourceRef, targetRef) = diagram_inner_rep.sequence_flows[params["id"]]
        output_flow = etree.SubElement(process, "sequenceFlow")
        output_flow.set("id", params["id"])
        output_flow.set("name", params["name"])
        output_flow.set("sourceRef", sourceRef)
        output_flow.set("targetRef", targetRef)

        output_flow_edge = etree.SubElement(plane, bpmndi_namespace + "BPMNEdge")
        output_flow_edge.set("id", params["id"] + "_gui")
        output_flow_edge.set("bpmnElement", params["id"])
        waypoints = params["waypoints"]
        for waypoint in waypoints:
            waypoint_element = etree.SubElement(output_flow_edge, "omgdi:waypoint")
            waypoint_element.set("x", waypoint[0])
            waypoint_element.set("y", waypoint[1])

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

"""
Helper function, removes namespace annotation from tag name
"""
def remove_namespace_from_tag_name(tag_name):
    return tag_name.split(':')[-1]