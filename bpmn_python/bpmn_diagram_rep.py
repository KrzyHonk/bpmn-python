import networkx as nx
import uuid
from xml.dom import minidom
import xml.etree.cElementTree as eTree


class BPMNDiagramGraph:
    """
    Class BPMNDiagramGraph implements simple inner representation of BPMN 2.0 diagram, based on NetworkX graph implementation

    Fields:
    - diagram_graph - networkx.Graph object, stores elements of BPMN diagram as nodes. Each edge of graph represents
    sequenceFlow element. Edges are identified by IDs of nodes connected by edge,
    - sequence_flows - dictionary (associative list) that uses sequenceFlow ID attribute as key
    and tuple of (sourceRef, targetRef) parameters as value. It is used to help searching edges by ID parameter,
    - process_attributes - dictionary that contains BPMN process element attributes,
    - diagram_attributes - dictionary that contains BPMN diagram element attributes,
    - plane_attributes - dictionary that contains BPMN plane element attributes.
    """

    # String "constants" used in multiple places
    id_prefix = "id"
    bpmndi_namespace = "bpmndi:"

    def __init__(self):
        """
        Default constructor, initializes object fields with new instances.
        """
        self.diagram_graph = nx.Graph()
        self.sequence_flows = {}
        self.process_attributes = {}
        self.diagram_attributes = {}
        self.plane_attributes = {}

    def add_process_attributes(self, process_element):
        """
        Adds attributes of BPMN process element to appropriate field process_attributes.
        Diagram inner representation contains following process attributes:
        - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
        - isClosed - optional parameter, default value 'false',
        - isExecutable - optional parameter, default value 'false',
        - processType - optional parameter, default value 'None',

        :param process_element: object representing a BPMN XML 'process' element.
        """
        self.process_attributes["id"] = process_element.getAttribute("id")
        self.process_attributes["isClosed"] = process_element.getAttribute("isClosed") if process_element.hasAttribute("isClosed") else "false"
        self.process_attributes["isExecutable"] = process_element.getAttribute("isExecutable") if process_element.hasAttribute("isExecutable") else "false"
        self.process_attributes["processType"] = process_element.getAttribute("processType") if process_element.hasAttribute("processType") else "None"

    def add_diagram_and_plane_attributes(self, diagram_element, plane_element):
        """
        Adds attributes of BPMN diagram and plane elements to appropriate fields diagram_attributes and plane_attributes.
        Diagram inner representation contains following diagram element attributes:
        - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
        - name - optional parameter, empty string by default,
        Diagram inner representation contains following plane element attributes:
        - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
        - bpmnElement - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,

        :param diagram_element: object representing a BPMN XML 'diagram' element,
        :param plane_element: object representing a BPMN XML 'plane' element.
        """
        self.diagram_attributes["id"] = diagram_element.getAttribute("id")
        self.diagram_attributes["name"] = diagram_element.getAttribute("name") if diagram_element.hasAttribute("name") else ""

        self.plane_attributes["id"] = plane_element.getAttribute("id")
        self.plane_attributes["bpmnElement"] = plane_element.getAttribute("bpmnElement")

    def add_flownode_to_graph(self, element, element_id):
        """
        Adds a new node to graph.
        Input parameter is object of class xml.dom.Element.
        Nodes are identified by ID attribute of Element.
        Method adds basic attributes (shared by all BPMN elements) to node. Those elements are:
        - id - added as key value, we assume that this is a required value,
        - type - tagName of element, used to identify type of BPMN diagram element,
        - name - optional attribute, empty string by default.

        :param element: object representing a BPMN XML element corresponding to given flownode,
        :param element_id: string with ID attribute value.
        """
        self.diagram_graph.add_node(element_id)
        self.diagram_graph.node[element_id]["type"] = self.remove_namespace_from_tag_name(element.tagName)
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

    def add_task_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN task.
        In our representation tasks have only basic attributes and elements, inherited from Activity type, so this method only needs to call add_flownode_to_graph.

        :param element: object representing a BPMN XML 'task' element,
        :param element_id: string with ID attribute value.
        """
        self.add_flownode_to_graph(element, element_id)

    def add_subprocess_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN subprocess.
        In addition to attributes inherited from FlowNode type, SubProcess has additional attribute tiggeredByEvent (boolean type, default value - false).

        :param element: object representing a BPMN XML 'subprocess' element,
        :param element_id: string with ID attribute value.
        """
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["triggeredByEvent"] = element.getAttribute("triggeredByEvent") if element.hasAttribute("triggeredByEvent") else "false"

    def add_gateway_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN gateway.
        In addition to attributes inherited from FlowNode type, Gateway has additional attribute gatewayDirection (simple type, default value - Unspecified).

        :param element: object representing a BPMN XML element of Gateway type extension,
        :param element_id: string with ID attribute value.
        """
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["gatewayDirection"] = element.getAttribute("gatewayDirection") if element.hasAttribute("gatewayDirection") else "Unspecified"

    def add_complex_gateway_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN complex gateway.
        In addition to attributes inherited from Gateway type, complex gateway has additional attribute default flow (default value - none).

        :param element: object representing a BPMN XML 'complexGateway' element,
        :param element_id: string with ID attribute value.
        """
        self.add_gateway_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["default"] = element.getAttribute("default") if element.hasAttribute("default") else None
        # TODO sequence of conditions
        # Can't get any working example of Complex gateway, so I'm not sure how exactly those conditions are kept

    def add_event_based_gateway_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN event based gateway.
        In addition to attributes inherited from Gateway type, event based gateway has additional attributes - instantiate
        (boolean type, default value - false) and eventGatewayType (custom type tEventBasedGatewayType, default value - Exclusive).

        :param element: object representing a BPMN XML 'eventBasedGateway' element,
        :param element_id: string with ID attribute value.
        """
        self.add_gateway_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["instantiate"] = element.getAttribute("instantiate") if element.hasAttribute("instantiate") else "false"
        self.diagram_graph.node[element_id]["eventGatewayType"] = element.getAttribute("eventGatewayType") if element.hasAttribute("eventGatewayType") else "Exclusive"

    def add_inclusive_or_exclusive_gateway_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN inclusive or eclusive gateway.
        In addition to attributes inherited from Gateway type, inclusive and exclusive gateway have additional attribute default flow (default value - none).

        :param element: object representing a BPMN XML 'inclusiveGateway' or 'exclusiveGateway' element,
        :param element_id: string with ID attribute value.
        """
        self.add_gateway_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["default"] = element.getAttribute("default") if element.hasAttribute("default") else None

    def add_parallel_gateway_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN parallel gateway.
        Parallel gateway doesn't have additional attributes. Separate method is used to improve code readability.

        :param element: object representing a BPMN XML 'parallelGateway',
        :param element_id: string with ID attribute value.
        """
        self.add_gateway_to_graph(element, element_id)

    def add_event_definition_elements(self, element, element_id, event_definitions):
        """
        Helper function, that adds event definition elements (defines special types of events) to corresponding events.

        :param element: object representing a BPMN XML event element,
        :param element_id: string with ID attribute value,
        :param event_definitions: list of event definitions, that belongs to given event.
        """
        event_def_list = []
        for definition_type in event_definitions:
            event_def_xml = element.getElementsByTagNameNS("*",definition_type)
            length = len(event_def_xml)
            for index in range(length):
                event_def_tmp = (definition_type, event_def_xml[index].getAttribute("id")) # tuple - definition type, definition id
                event_def_list.append(event_def_tmp)
        self.diagram_graph.node[element_id]["event_definitions"] = event_def_list

    # TODO Add isInterrupting?
    def add_start_event_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN start event.
        Start event inherits attribute parallelMultiple from CatchEvent type and sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).

        :param element: object representing a BPMN XML 'startEvent' element,
        :param element_id: string with ID attribute value.
        """
        start_event_definitions = {'messageEventDefinition', 'timerEventDefinition', 'conditionalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["parallelMultiple"] = element.getAttribute("parallelMultiple") if element.hasAttribute("parallelMultiple") else "false"
        self.add_event_definition_elements(element, element_id, start_event_definitions)

    def add_intermediate_catch_event_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN intermediate catch event.
        Intermediate catch event inherits attribute parallelMultiple from CatchEvent type and sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).

        :param element: object representing a BPMN XML 'intermediateCatchEvent' element,
        :param element_id: string with ID attribute value.
        """
        intermediate_catch_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'conditionalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)
        self.diagram_graph.node[element_id]["parallelMultiple"] = element.getAttribute("parallelMultiple") if element.hasAttribute("parallelMultiple") else "false"
        self.add_event_definition_elements(element, element_id, intermediate_catch_event_definitions)

    def add_end_event_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN end event.
        End event inherits sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).

        :param element: object representing a BPMN XML 'endEvent' element,
        :param element_id: string with ID attribute value.
        """
        end_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)
        self.add_event_definition_elements(element, element_id, end_event_definitions)

    def add_intermediate_throw_event_to_graph(self, element, element_id):
        """
        Adds to graph the new element that represents BPMN intermediate throw event.
        Intermediate throw event inherits sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants (Message, Error, Signal etc.).

        :param element: object representing a BPMN XML 'intermediateThrowEvent' element,
        :param element_id: string with ID attribute value.
        """
        intermediate_throw_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'escalationEventDefinition'}
        self.add_flownode_to_graph(element, element_id)
        self.add_event_definition_elements(element, element_id, intermediate_throw_event_definitions)

    def add_edge_to_graph(self, flow):
        """
        Adds a new edge to graph and a record to sequence_flows dictionary.
        Input parameter is object of class xml.dom.Element.
        Edges are identified by pair of sourceRef and targetRef attributes of BPMNFlow element. We also provide a dictionary, that maps sequenceFlow ID attribute with its sourceRef and targetRef.
        Method adds basic attributes of sequenceFlow element to edge. Those elements are:
        - id - added as edge attribute, we assume that this is a required value,
        - name - optional attribute, empty string by default.

        :param flow: object representing a BPMN XML 'sequenceFlow' element.
        """
        flow_id = flow.getAttribute("id")
        source_ref = flow.getAttribute("sourceRef")
        target_ref = flow.getAttribute("targetRef")
        self.sequence_flows[flow_id] = (source_ref, target_ref)
        self.diagram_graph.add_edge(source_ref, target_ref)
        self.diagram_graph.edge[source_ref][target_ref]["id"] = flow.getAttribute("id")
        self.diagram_graph.edge[source_ref][target_ref]["name"] = flow.getAttribute("name") if flow.hasAttribute("name") else ""

    def add_shape_DI(self, element_graphic):
        """
        Adds Diagram Interchange information (information about rendering a diagram) to appropriate BPMN diagram element in graph node.
        We assume that those attributes are required for each BPMNShape:
        - width - width of BPMNShape,
        - height - height of BPMNShape,
        - x - first coordinate of BPMNShape,
        - y - second coordinate of BPMNShape.

        :param element_graphic: object representing a BPMN XML 'BPMNShape' element.
        """
        element_id = element_graphic.getAttribute("bpmnElement")
        bounds = element_graphic.getElementsByTagNameNS("*","Bounds")[0]
        self.diagram_graph.node[element_id]["width"] = bounds.getAttribute("width")
        self.diagram_graph.node[element_id]["height"] = bounds.getAttribute("height")
        self.diagram_graph.node[element_id]["x"] = bounds.getAttribute("x")
        self.diagram_graph.node[element_id]["y"] = bounds.getAttribute("y")

    def add_edge_DI(self, flow_graphic):
        """
        Adds Diagram Interchange information (information about rendering a diagram) to appropriate BPMN sequence flow represented as graph edge.
        We assume that each BPMNEdge has a list of 'waypoint' elements. BPMN 2.0 XML Schema states, that each BPMNEdge must have at least two waypoints.

        :param flow_graphic: object representing a BPMN XML 'BPMNEdge' element.
        """
        flow_id = flow_graphic.getAttribute("bpmnElement")
        waypoints_xml = flow_graphic.getElementsByTagNameNS("*","waypoint")
        length = len(waypoints_xml)
        waypoints = [None] * length
        for index in range(length):
            waypoint_tmp = (waypoints_xml[index].getAttribute("x"), waypoints_xml[index].getAttribute("y"))
            waypoints[index] = waypoint_tmp
        (source_ref, target_ref) = self.sequence_flows[flow_id]
        self.diagram_graph.edge[source_ref][target_ref]["waypoints"] = waypoints

    def load_diagram_from_xml(self, filepath):
        """
        Reads an XML file from given filepath and maps it into inner representation of BPMN diagram.
        Returns an instance of BPMNDiagramGraph class.

        :param filepath: string with output filepath.
        """
        document = self.read_xml_file(filepath)
        process_element = document.getElementsByTagNameNS("*","process")[0] # We assume that there's only one process element
        diagram_element = document.getElementsByTagNameNS("*","BPMNDiagram")[0] # We assume that there's only one diagram element with one plane element
        plane_element = diagram_element.getElementsByTagNameNS("*","BPMNPlane")[0]

        self.add_process_attributes(process_element)
        self.add_diagram_and_plane_attributes(diagram_element, plane_element)

        for element in self.iterate_elements(process_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = self.remove_namespace_from_tag_name(element.tagName)
                if tag_name == "task":
                    self.add_task_to_graph(element, element.getAttribute("id"))
                elif tag_name == "subProcess":
                    self.add_subprocess_to_graph(element, element.getAttribute("id"))
                elif tag_name == "inclusiveGateway" or tag_name == "exclusiveGateway":
                    self.add_inclusive_or_exclusive_gateway_to_graph(element, element.getAttribute("id"))
                elif tag_name == "parallelGateway":
                    self.add_parallel_gateway_to_graph(element, element.getAttribute("id"))
                elif tag_name == "eventBasedGateway":
                    self.add_event_based_gateway_to_graph(element, element.getAttribute("id"))
                elif tag_name == "complexGateway":
                    self.add_complex_gateway_to_graph(element, element.getAttribute("id"))
                elif tag_name == "startEvent":
                    self.add_start_event_to_graph(element, element.getAttribute("id"))
                elif tag_name == "endEvent":
                    self.add_end_event_to_graph(element, element.getAttribute("id"))
                elif tag_name == "intermediateCatchEvent":
                    self.add_intermediate_catch_event_to_graph(element, element.getAttribute("id"))
                elif tag_name == "intermediateThrowEvent":
                    self.add_intermediate_throw_event_to_graph(element, element.getAttribute("id"))

        for flow in self.iterate_elements(process_element):
            if flow.nodeType != flow.TEXT_NODE:
                tag_name = self.remove_namespace_from_tag_name(flow.tagName)
                if tag_name == "sequenceFlow":
                    self.add_edge_to_graph(flow)

        for element in self.iterate_elements(plane_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = self.remove_namespace_from_tag_name(element.tagName)
                if tag_name == "BPMNShape":
                    self.add_shape_DI(element)
                elif tag_name == "BPMNEdge":
                    self.add_edge_DI(element)

    # TODO Add params to docstrings
    # Exporting to XML methods
    def export_task_info(self, node_params, output_element):
        """
        Adds Task node attributes to exported XML element
        """
        pass

    def export_subprocess_info(self, node_params, output_element):
        """
        Adds Subprocess node attributes to exported XML element
        """
        output_element.set("triggeredByEvent", node_params["triggeredByEvent"])

    # TODO sequence of conditions
    def export_complex_gateway_info(self, node_params, output_element):
        """
        Adds ComplexGateway node attributes to exported XML element
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])
        if node_params["default"] != None:
             output_element.set("default", node_params["default"])

    def export_event_based_gateway_info(self, node_params, output_element):
        """
        Adds EventBasedGateway node attributes to exported XML element
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])
        output_element.set("instantiate", node_params["instantiate"])
        output_element.set("eventGatewayType", node_params["eventGatewayType"])

    def export_inclusive_exclusive_gateway_info(self, node_params, output_element):
        """
        Adds InclusiveGateway or ExclusiveGateway node attributes to exported XML element
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])
        if node_params["default"] != None:
             output_element.set("default", node_params["default"])

    def export_parallel_gateway_info(self, node_params, output_element):
        """
        Adds Subprocess node attributes to exported XML element
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])

    def export_catch_event_info(self, node_params, output_element):
        """
        Adds StartEvent or IntermediateCatchEvent attributes to exported XML element
        """
        output_element.set("parallelMultiple", node_params["parallelMultiple"])
        definitions = node_params["event_definitions"]
        for definition in definitions:
            definition_type = definition[0]
            definition_id = definition[1]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set("id", definition_id)

    def export_throw_event_info(self, node_params, output_element):
        """
        Adds EndEvent or IntermediateThrowingEvent attributes to exported XML element
        """
        definitions = node_params["event_definitions"]
        for definition in definitions:
            definition_type = definition[0]
            definition_id = definition[1]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set("id", definition_id)

    def export_xml_file(self, output_path):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (with Diagram Interchange data).
        """
        [root, process] = self.create_root_process_output()
        [diagram, plane] = self.create_diagram_plane_output(root)

        # for each node in graph add correct type of element, its attributes and BPMNShape element
        nodes = self.diagram_graph.nodes(data=True)
        for node in nodes:
            id = node[0]
            params = node[1]
            self.export_node_process_data(id, params, process)
            self.export_node_di_data(id, params, plane)

        # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
        edges = self.diagram_graph.edges(data=True)
        for flow in edges:
            params = flow[2]
            (source_ref, target_ref) = self.sequence_flows[params["id"]]
            self.export_edge_process_data(params, process, source_ref, target_ref)
            self.export_edge_di_data(params, plane)

        self.indent(root)
        tree = eTree.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)

    def export_xml_file_no_di(self, output_path):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (without Diagram Interchange data).
        """
        [root, process] = self.create_root_process_output()

        # for each node in graph add correct type of element, its attributes and BPMNShape element
        nodes = self.diagram_graph.nodes(data=True)
        for node in nodes:
            id = node[0]
            params = node[1]
            self.export_node_process_data(id, params, process)

        # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
        edges = self.diagram_graph.edges(data=True)
        for flow in edges:
            params = flow[2]
            (source_ref, target_ref) = self.sequence_flows[params["id"]]
            self.export_edge_process_data(params, process, source_ref, target_ref)

        self.indent(root)
        tree = eTree.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)

    def create_root_process_output(self):
        """
        Creates root element ('definitions') and 'process' element for exported BPMN XML file.
        Returns a tuple (root, process).
        """
        root = eTree.Element("definitions")
        root.set("xmlns", "http://www.omg.org/spec/BPMN/20100524/MODEL")
        root.set("xmlns:bpmndi", "http://www.omg.org/spec/BPMN/20100524/DI")
        root.set("xmlns:omgdc", "http://www.omg.org/spec/DD/20100524/DC")
        root.set("xmlns:omgdi", "http://www.omg.org/spec/DD/20100524/DI")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("targetNamespace", "http://www.signavio.com/bpmn20")
        root.set("typeLanguage", "http://www.w3.org/2001/XMLSchema")
        root.set("expressionLanguage", "http://www.w3.org/1999/XPath")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")

        process = eTree.SubElement(root, "process")
        process.set("id", self.process_attributes["id"])
        process.set("isClosed", self.process_attributes["isClosed"])
        process.set("isExecutable", self.process_attributes["isExecutable"])
        process.set("processType", self.process_attributes["processType"])

        return root, process

    def create_diagram_plane_output(self, root):
        """
        Creates 'diagram' and 'plane' elements for exported BPMN XML file.
        Returns a tuple (diagram, plane).
        """
        diagram = eTree.SubElement(root, self.bpmndi_namespace + "BPMNDiagram")
        diagram.set("id", self.diagram_attributes["id"])
        diagram.set("name", self.diagram_attributes["name"])

        plane = eTree.SubElement(diagram, self.bpmndi_namespace + "BPMNPlane")
        plane.set("id", self.plane_attributes["id"])
        plane.set("bpmnElement", self.plane_attributes["bpmnElement"])

        return diagram, plane

    def export_node_process_data(self, id, params, process):
        """
        Creates a new XML element (depends on node type) for given node parameters and adds it to 'process' element.
        """
        node_type = params["type"]
        output_element = eTree.SubElement(process, node_type)
        output_element.set("id", id)
        output_element.set("name", params["name"])

        for incoming in params["incoming"]:
            incoming_element = eTree.SubElement(output_element, "incoming")
            incoming_element.text = incoming
        for outgoing in params["outgoing"]:
            outgoing_element = eTree.SubElement(output_element, "outgoing")
            outgoing_element.text = outgoing

        if node_type == "task":
            self.export_task_info(params, output_element)
        elif node_type == "subProcess":
            self.export_subprocess_info(params, output_element)
        elif node_type == "complexGateway":
            self.export_complex_gateway_info(params, output_element)
        elif node_type == "eventBasedGateway":
            self.export_event_based_gateway_info(params, output_element)
        elif node_type == "inclusiveGateway" or node_type == "exclusiveGateway":
            self.export_inclusive_exclusive_gateway_info(params, output_element)
        elif node_type == "parallelGateway":
            self.export_parallel_gateway_info(params, output_element)
        elif node_type == "startEvent" or node_type == "intermediateCatchEvent":
            self.export_catch_event_info(params, output_element)
        elif node_type == "endEvent" or node_type == "intermediateThrowEvent":
            self.export_throw_event_info(params, output_element)

    def export_node_di_data(self, id, params, plane):
        """
        Creates a new BPMNShape XML element for given node parameters and adds it to 'plane' element.
        """
        output_element_di = eTree.SubElement(plane, self.bpmndi_namespace + "BPMNShape")
        output_element_di.set("id", id + "_gui")
        output_element_di.set("bpmnElement", id)
        bounds = eTree.SubElement(output_element_di, "omgdc:Bounds")
        bounds.set("width", params["width"])
        bounds.set("height", params["height"])
        bounds.set("x", params["x"])
        bounds.set("y", params["y"])

    def export_edge_process_data(self, params, process, source_ref, target_ref):
        """
        Creates a new SequenceFlow XML element for given edge parameters and adds it to 'process' element.
        """
        output_flow = eTree.SubElement(process, "sequenceFlow")
        output_flow.set("id", params["id"])
        output_flow.set("name", params["name"])
        output_flow.set("sourceRef", source_ref)
        output_flow.set("targetRef", target_ref)

    def export_edge_di_data(self, params, plane):
        """
        Creates a new BPMNEdge XML element for given edge parameters and adds it to 'plane' element.
        """
        output_flow_edge = eTree.SubElement(plane, self.bpmndi_namespace + "BPMNEdge")
        output_flow_edge.set("id", params["id"] + "_gui")
        output_flow_edge.set("bpmnElement", params["id"])
        waypoints = params["waypoints"]
        for waypoint in waypoints:
            waypoint_element = eTree.SubElement(output_flow_edge, "omgdi:waypoint")
            waypoint_element.set("x", waypoint[0])
            waypoint_element.set("y", waypoint[1])

    def iterate_elements(self, parent):
        """
        Helper function that iterates over child Nodes/Elements of parent Node/Element.
        """
        element = parent.firstChild
        while element is not None:
            yield element
            element = element.nextSibling

    def read_xml_file(self, filepath):
        """
        Reads BPMN 2.0 XML file from given filepath and returns xml.dom.xminidom.Document object.
        """
        dom_tree = minidom.parse(filepath)
        return dom_tree

    def indent(self, elem, level=0):
        """
        Helper function, adds indentation to XML output.
        """
        i = "\n" + level*"  "
        j = "\n" + (level-1)*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem

    def remove_namespace_from_tag_name(self, tag_name):
        """
        Helper function, removes namespace annotation from tag name
        """
        return tag_name.split(':')[-1]

    # Querying methods
    def get_nodes(self, type = ""):
        """
        Gets all nodes of requested type. If no type is provided by user, method returns all nodes in BPMN diagram graph.
        Returns a dictionary, where key is an ID of node, value is a dictionary of all node attributes.
        """
        tmp_nodes = self.diagram_graph.nodes(True)
        if type == "":
            return tmp_nodes
        else:
            nodes = []
            for node in tmp_nodes:
                if node[1]["type"] == type:
                    nodes.append(node)
            return nodes

    def get_node_by_id(self, node_id):
        """
        Gets a node with requested ID.
        Returns a tuple, where first value is node ID, second - a dictionary of all node attributes.
        """
        tmp_nodes = self.diagram_graph.nodes(data=True)
        for node in tmp_nodes:
            if node[1]["id"] == node_id:
                return node

    def get_edges(self):
        """
        Gets all graph edges.
        Returns a two-dimensional dictionary, where keys are IDs of nodes connected by edge, value is a dictionary of all edge attributes.
        """
        return self.diagram_graph.edges(data=True)

    def get_edge_by_id(self, edge_id):
        """
        Gets an edge with requested ID.
        Returns a tuple, where first value is node ID, second - a dictionary of all node attributes.
        """
        tmp_edges = self.diagram_graph.edges(data=True)
        for edge in tmp_edges:
            if edge[2]["id"] == edge_id:
                return edge

    # Diagram creating methods
    def create_new_diagram_graph(self, process_is_closed = False, process_is_executable = False, process_type = "None", diagram_name = ""):
        """
        Initializes a new BPMN diagram and sets up a basic process, diagram and plane attributes.
        Accepts a user-defined values for following attributes:
        (Process element)
        - isClosed - default value false,
        - isExecutable - default value false,
        - processType - default value None.
        (Diagram element)
        - name - default value empty string.
        """
        self.__init__()
        process_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        diagram_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        plane_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.process_attributes["id"] = process_id
        self.process_attributes["isClosed"] = "true" if process_is_closed else "false"
        self.process_attributes["isExecutable"] = "true" if process_is_executable else "false"
        self.process_attributes["processType"] = process_type

        self.diagram_attributes["id"] = diagram_id
        self.diagram_attributes["name"] = diagram_name

        self.plane_attributes["id"] = plane_id
        self.plane_attributes["bpmnElement"] = process_id

    def add_flow_node_to_diagram(self, node_type, node_id, node_name):
        """
        Helper function that adds a new Flow Node to diagram. It is used to add a new node of specified type.
        Adds a basic information inherited from Flow Node type.
        """
        self.diagram_graph.add_node(node_id)
        self.diagram_graph.node[node_id]["type"] = node_type
        self.diagram_graph.node[node_id]["name"] = node_name
        self.diagram_graph.node[node_id]["incoming"] = []
        self.diagram_graph.node[node_id]["outgoing"] = []

        # TODO Automated generation of rendering parameters
        self.diagram_graph.node[node_id]["width"] = "100"
        self.diagram_graph.node[node_id]["height"] = "100"
        self.diagram_graph.node[node_id]["x"] = "100"
        self.diagram_graph.node[node_id]["y"] = "100"

    def add_task_to_diagram(self, task_name = ""):
        """
        Adds a Task element to BPMN diagram.
        User-defined attributes:
        - name
        Returns a tuple, where first value is task ID, second a reference to created object.
        """
        task_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("task", task_id, task_name)
        return (task_id, self.diagram_graph.node[task_id])

    # TODO add isExpanded?
    def add_subprocess_to_diagram(self, subprocess_name, triggered_by_event = False):
        """
        Adds a SubProcess element to BPMN diagram.
        User-defined attributes:
        - name
        - triggered_by_event
        Returns a tuple, where first value is subProcess ID, second a reference to created object.
        """
        subprocess_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("subProcess", subprocess_id, subprocess_name)
        self.diagram_graph.node[subprocess_id]["triggeredByEvent"] = "true" if triggered_by_event else "false"
        return (subprocess_id, self.diagram_graph.node[subprocess_id])

    def add_start_event_to_diagram(self, start_event_name = "", start_event_definition = None, parallel_multiple = False):
        """
        Adds a StartEvent element to BPMN diagram.
        User-defined attributes:
        - name
        - parallel_multiple
        Returns a tuple, where first value is startEvent ID, second a reference to created object.
        """
        start_event_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("startEvent", start_event_id, start_event_name)
        self.diagram_graph.node[start_event_id]["parallelMultiple"] = "true" if parallel_multiple else "false"
        # TODO Add event definition
        self.diagram_graph.node[start_event_id]["event_definitions"] = []
        return (start_event_id, self.diagram_graph.node[start_event_id])

    def add_end_event_to_diagram(self, end_event_name = "", end_event_definition = None):
        """
        Adds an EndEvent element to BPMN diagram.
        User-defined attributes:
        - name
        Returns a tuple, where first value is endEvent ID, second a reference to created object.
        """
        end_event_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("endEvent", end_event_id, end_event_name)
        # TODO Add event definition
        self.diagram_graph.node[end_event_id]["event_definitions"] = []
        return (end_event_id, self.diagram_graph.node[end_event_id])

    def add_exclusive_gateway_to_diagram(self):
        """
        """
        pass

    def add_inclusive_gateway_to_diagram(self):
        """
        """
        pass

    def add_parallel_gateway_to_diagram(self):
        """
        """
        pass

    def add_sequence_flow_to_diagram(self, source_ref_id, target_ref_id, sequence_flow_name = ""):
        """
        Adds a SequenceFlow element to BPMN diagram.
        Requires that user passes a sourceRef and targetRef as parameters.
        User-defined attributes:
        - name
        Returns a tuple, where first value is sequenceFlow ID, second a reference to created object.
        """
        sequence_flow_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.sequence_flows[sequence_flow_id] = (source_ref_id, target_ref_id)
        self.diagram_graph.add_edge(source_ref_id, target_ref_id)
        self.diagram_graph.edge[source_ref_id][target_ref_id]["id"] = sequence_flow_id
        self.diagram_graph.edge[source_ref_id][target_ref_id]["name"] = sequence_flow_name
        self.diagram_graph.edge[source_ref_id][target_ref_id]["waypoints"] = [(self.diagram_graph.node[source_ref_id]["x"], self.diagram_graph.node[source_ref_id]["y"]),
                                                                              (self.diagram_graph.node[target_ref_id]["x"], self.diagram_graph.node[target_ref_id]["y"])]

        # add target node (target_ref_id) as outgoing node from source node (source_ref_id)
        self.diagram_graph.node[source_ref_id]["outgoing"].append(target_ref_id)

        # add source node (source_ref_id) as incoming node to target node (target_ref_id)
        self.diagram_graph.node[target_ref_id]["incoming"].append(source_ref_id)
        return (sequence_flow_id, self.diagram_graph.edge[source_ref_id][target_ref_id])