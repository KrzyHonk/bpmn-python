from xml.dom import minidom


class BPMNDiagramGraphImport:
    """
    Class BPMNDiagramGraphImport provides methods for importing BPMN 2.0 XML file.
    As a utility class, it only contains static methods.
    This class is meant to be used from BPMNDiagramGraph class.
    """

    @staticmethod
    def add_process_attributes(process_attributes, process_element):
        """
        Adds attributes of BPMN process element to appropriate field process_attributes.
        Diagram inner representation contains following process attributes:
        - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
        - isClosed - optional parameter, default value 'false',
        - isExecutable - optional parameter, default value 'false',
        - processType - optional parameter, default value 'None',

        :param process_attributes: dictionary that holds attribute values for imported 'process' element,
        :param process_element: object representing a BPMN XML 'process' element.
        """
        process_attributes["id"] = process_element.getAttribute("id")
        process_attributes["isClosed"] = process_element.getAttribute("isClosed") \
            if process_element.hasAttribute("isClosed") else "false"
        process_attributes["isExecutable"] = process_element.getAttribute("isExecutable") \
            if process_element.hasAttribute("isExecutable") else "false"
        process_attributes["processType"] = process_element.getAttribute("processType") \
            if process_element.hasAttribute("processType") else "None"

    @staticmethod
    def add_diagram_and_plane_attributes(diagram_attributes, plane_attributes, diagram_element, plane_element):
        """
        Adds attributes of BPMN diagram and plane elements to appropriate
        fields diagram_attributes and plane_attributes.
        Diagram inner representation contains following diagram element attributes:
        - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
        - name - optional parameter, empty string by default,
        Diagram inner representation contains following plane element attributes:
        - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
        - bpmnElement - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,

        :param diagram_attributes: dictionary that holds attribute values for imported 'BPMNDiagram' element,
        :param plane_attributes: dictionary that holds attribute values for imported 'BPMNPlane' element,
        :param diagram_element: object representing a BPMN XML 'diagram' element,
        :param plane_element: object representing a BPMN XML 'plane' element.
        """
        diagram_attributes["id"] = diagram_element.getAttribute("id")
        diagram_attributes["name"] = diagram_element.getAttribute("name") \
            if diagram_element.hasAttribute("name") else ""

        plane_attributes["id"] = plane_element.getAttribute("id")
        plane_attributes["bpmnElement"] = plane_element.getAttribute("bpmnElement")

    @staticmethod
    def add_flownode_to_graph(diagram_graph, element, element_id):
        """
        Adds a new node to graph.
        Input parameter is object of class xml.dom.Element.
        Nodes are identified by ID attribute of Element.
        Method adds basic attributes (shared by all BPMN elements) to node. Those elements are:
        - id - added as key value, we assume that this is a required value,
        - type - tagName of element, used to identify type of BPMN diagram element,
        - name - optional attribute, empty string by default.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML element corresponding to given flownode,
        :param element_id: string with ID attribute value.
        """
        diagram_graph.add_node(element_id)
        diagram_graph.node[element_id]["type"] = BPMNDiagramGraphImport.remove_namespace_from_tag_name(element.tagName)
        diagram_graph.node[element_id]["name"] = element.getAttribute("name") if element.hasAttribute("name") else ""

        # add incoming flow node list
        incoming_xml = element.getElementsByTagNameNS("*", "incoming")
        length = len(incoming_xml)
        incoming_list = [None] * length
        for index in range(length):
            incoming_tmp = incoming_xml[index].firstChild.nodeValue
            incoming_list[index] = incoming_tmp
        diagram_graph.node[element_id]["incoming"] = incoming_list

        # add outgoing flow node list
        outgoing_xml = element.getElementsByTagNameNS("*", "outgoing")
        length = len(outgoing_xml)
        outgoing_list = [None] * length
        for index in range(length):
            outgoing_tmp = outgoing_xml[index].firstChild.nodeValue
            outgoing_list[index] = outgoing_tmp
        diagram_graph.node[element_id]["outgoing"] = outgoing_list

    @staticmethod
    def add_task_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN task.
        In our representation tasks have only basic attributes and elements, inherited from Activity type,
        so this method only needs to call add_flownode_to_graph.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'task' element,
        :param element_id: string with ID attribute value.
        """
        BPMNDiagramGraphImport.add_flownode_to_graph(diagram_graph, element, element_id)

    @staticmethod
    def add_subprocess_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN subprocess.
        In addition to attributes inherited from FlowNode type, SubProcess
        has additional attribute tiggeredByEvent (boolean type, default value - false).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'subprocess' element,
        :param element_id: string with ID attribute value.
        """
        BPMNDiagramGraphImport.add_flownode_to_graph(diagram_graph, element, element_id)
        diagram_graph.node[element_id]["triggeredByEvent"] = element.getAttribute("triggeredByEvent") \
            if element.hasAttribute("triggeredByEvent") else "false"

    @staticmethod
    def add_gateway_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN gateway.
        In addition to attributes inherited from FlowNode type, Gateway
        has additional attribute gatewayDirection (simple type, default value - Unspecified).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML element of Gateway type extension,
        :param element_id: string with ID attribute value.
        """
        BPMNDiagramGraphImport.add_flownode_to_graph(diagram_graph, element, element_id)
        diagram_graph.node[element_id]["gatewayDirection"] = element.getAttribute("gatewayDirection") \
            if element.hasAttribute("gatewayDirection") else "Unspecified"

    @staticmethod
    def add_complex_gateway_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN complex gateway.
        In addition to attributes inherited from Gateway type, complex gateway
        has additional attribute default flow (default value - none).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'complexGateway' element,
        :param element_id: string with ID attribute value.
        """
        BPMNDiagramGraphImport.add_gateway_to_graph(diagram_graph, element, element_id)
        diagram_graph.node[element_id]["default"] = element.getAttribute("default") \
            if element.hasAttribute("default") else None
        # TODO sequence of conditions
        # Can't get any working example of Complex gateway, so I'm not sure how exactly those conditions are kept

    @staticmethod
    def add_event_based_gateway_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN event based gateway.
        In addition to attributes inherited from Gateway type, event based gateway has additional
        attributes - instantiate (boolean type, default value - false) and eventGatewayType
        (custom type tEventBasedGatewayType, default value - Exclusive).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'eventBasedGateway' element,
        :param element_id: string with ID attribute value.
        """
        BPMNDiagramGraphImport.add_gateway_to_graph(diagram_graph, element, element_id)
        diagram_graph.node[element_id]["instantiate"] = element.getAttribute("instantiate") \
            if element.hasAttribute("instantiate") else "false"
        diagram_graph.node[element_id]["eventGatewayType"] = element.getAttribute("eventGatewayType") \
            if element.hasAttribute("eventGatewayType") else "Exclusive"

    @staticmethod
    def add_inclusive_or_exclusive_gateway_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN inclusive or eclusive gateway.
        In addition to attributes inherited from Gateway type, inclusive and exclusive gateway have additional
        attribute default flow (default value - none).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'inclusiveGateway' or 'exclusiveGateway' element,
        :param element_id: string with ID attribute value.
        """
        BPMNDiagramGraphImport.add_gateway_to_graph(diagram_graph, element, element_id)
        diagram_graph.node[element_id]["default"] = element.getAttribute("default") \
            if element.hasAttribute("default") else None

    @staticmethod
    def add_parallel_gateway_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN parallel gateway.
        Parallel gateway doesn't have additional attributes. Separate method is used to improve code readability.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'parallelGateway',
        :param element_id: string with ID attribute value.
        """
        BPMNDiagramGraphImport.add_gateway_to_graph(diagram_graph, element, element_id)

    @staticmethod
    def add_event_definition_elements(diagram_graph, element, element_id, event_definitions):
        """
        Helper function, that adds event definition elements (defines special types of events) to corresponding events.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML event element,
        :param element_id: string with ID attribute value,
        :param event_definitions: list of event definitions, that belongs to given event.
        """
        event_def_list = []
        for definition_type in event_definitions:
            event_def_xml = element.getElementsByTagNameNS("*", definition_type)
            length = len(event_def_xml)
            for index in range(length):
                # tuple - definition type, definition id
                event_def_tmp = (definition_type, event_def_xml[index].getAttribute("id"))
                event_def_list.append(event_def_tmp)
        diagram_graph.node[element_id]["event_definitions"] = event_def_list

    # TODO Add isInterrupting?
    @staticmethod
    def add_start_event_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN start event.
        Start event inherits attribute parallelMultiple from CatchEvent type
        and sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'startEvent' element,
        :param element_id: string with ID attribute value.
        """
        start_event_definitions = {'messageEventDefinition', 'timerEventDefinition',
                                   'conditionalEventDefinition', 'escalationEventDefinition'}
        BPMNDiagramGraphImport.add_flownode_to_graph(diagram_graph, element, element_id)
        diagram_graph.node[element_id]["parallelMultiple"] = element.getAttribute("parallelMultiple") \
            if element.hasAttribute("parallelMultiple") else "false"
        BPMNDiagramGraphImport.add_event_definition_elements(diagram_graph, element,
                                                             element_id, start_event_definitions)

    @staticmethod
    def add_intermediate_catch_event_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN intermediate catch event.
        Intermediate catch event inherits attribute parallelMultiple from CatchEvent type
        and sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'intermediateCatchEvent' element,
        :param element_id: string with ID attribute value.
        """
        intermediate_catch_event_definitions = {'messageEventDefinition', 'signalEventDefinition',
                                                'conditionalEventDefinition', 'escalationEventDefinition'}
        BPMNDiagramGraphImport.add_flownode_to_graph(diagram_graph, element, element_id)
        diagram_graph.node[element_id]["parallelMultiple"] = element.getAttribute("parallelMultiple") \
            if element.hasAttribute("parallelMultiple") else "false"
        BPMNDiagramGraphImport.add_event_definition_elements(diagram_graph, element,
                                                             element_id, intermediate_catch_event_definitions)

    @staticmethod
    def add_end_event_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN end event.
        End event inherits sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'endEvent' element,
        :param element_id: string with ID attribute value.
        """
        end_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'escalationEventDefinition'}
        BPMNDiagramGraphImport.add_flownode_to_graph(diagram_graph, element, element_id)
        BPMNDiagramGraphImport.add_event_definition_elements(diagram_graph, element, element_id, end_event_definitions)

    @staticmethod
    def add_intermediate_throw_event_to_graph(diagram_graph, element, element_id):
        """
        Adds to graph the new element that represents BPMN intermediate throw event.
        Intermediate throw event inherits sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML 'intermediateThrowEvent' element,
        :param element_id: string with ID attribute value.
        """
        intermediate_throw_event_definitions = {'messageEventDefinition',
                                                'signalEventDefinition', 'escalationEventDefinition'}
        BPMNDiagramGraphImport.add_flownode_to_graph(diagram_graph, element, element_id)
        BPMNDiagramGraphImport.add_event_definition_elements(diagram_graph, element,
                                                             element_id, intermediate_throw_event_definitions)

    @staticmethod
    def add_edge_to_graph(diagram_graph, sequence_flows, flow):
        """
        Adds a new edge to graph and a record to sequence_flows dictionary.
        Input parameter is object of class xml.dom.Element.
        Edges are identified by pair of sourceRef and targetRef attributes of BPMNFlow element. We also
        provide a dictionary, that maps sequenceFlow ID attribute with its sourceRef and targetRef.
        Method adds basic attributes of sequenceFlow element to edge. Those elements are:
        - id - added as edge attribute, we assume that this is a required value,
        - name - optional attribute, empty string by default.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows:- sequence_flows - dictionary (associative list) that uses sequenceFlow ID
        attribute as key and tuple of (sourceRef, targetRef) parameters as value,
        :param flow: object representing a BPMN XML 'sequenceFlow' element.
        """
        flow_id = flow.getAttribute("id")
        source_ref = flow.getAttribute("sourceRef")
        target_ref = flow.getAttribute("targetRef")
        sequence_flows[flow_id] = (source_ref, target_ref)
        diagram_graph.add_edge(source_ref, target_ref)
        diagram_graph.edge[source_ref][target_ref]["id"] = flow.getAttribute("id")
        diagram_graph.edge[source_ref][target_ref]["name"] = flow.getAttribute("name") \
            if flow.hasAttribute("name") else ""

    @staticmethod
    def add_shape_di(diagram_graph, shape_element):
        """
        Adds Diagram Interchange information (information about rendering a diagram) to appropriate
        BPMN diagram element in graph node.
        We assume that those attributes are required for each BPMNShape:
        - width - width of BPMNShape,
        - height - height of BPMNShape,
        - x - first coordinate of BPMNShape,
        - y - second coordinate of BPMNShape.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param shape_element: object representing a BPMN XML 'BPMNShape' element.
        """
        element_id = shape_element.getAttribute("bpmnElement")
        bounds = shape_element.getElementsByTagNameNS("*", "Bounds")[0]
        diagram_graph.node[element_id]["width"] = bounds.getAttribute("width")
        diagram_graph.node[element_id]["height"] = bounds.getAttribute("height")
        diagram_graph.node[element_id]["x"] = bounds.getAttribute("x")
        diagram_graph.node[element_id]["y"] = bounds.getAttribute("y")

    @staticmethod
    def add_edge_di(diagram_graph, sequence_flows, edge_element):
        """
        Adds Diagram Interchange information (information about rendering a diagram) to appropriate
        BPMN sequence flow represented as graph edge.
        We assume that each BPMNEdge has a list of 'waypoint' elements. BPMN 2.0 XML Schema states,
        that each BPMNEdge must have at least two waypoints.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows:- sequence_flows - dictionary (associative list) that uses sequenceFlow ID
        attribute as key and tuple of (sourceRef, targetRef) parameters as value,
        :param edge_element: object representing a BPMN XML 'BPMNEdge' element.
        """
        flow_id = edge_element.getAttribute("bpmnElement")
        waypoints_xml = edge_element.getElementsByTagNameNS("*", "waypoint")
        length = len(waypoints_xml)
        waypoints = [None] * length
        for index in range(length):
            waypoint_tmp = (waypoints_xml[index].getAttribute("x"), waypoints_xml[index].getAttribute("y"))
            waypoints[index] = waypoint_tmp
        (source_ref, target_ref) = sequence_flows[flow_id]
        diagram_graph.edge[source_ref][target_ref]["waypoints"] = waypoints

    @staticmethod
    def load_diagram_from_xml(filepath, diagram_graph, sequence_flows,
                              process_attributes, diagram_attributes, plane_attributes):
        """
        Reads an XML file from given filepath and maps it into inner representation of BPMN diagram.
        Returns an instance of BPMNDiagramGraph class.

        :param filepath: string with output filepath,
        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows:- sequence_flows - dictionary (associative list) that uses sequenceFlow ID
        attribute as key and tuple of (sourceRef, targetRef) parameters as value,
        :param process_attributes: dictionary that holds attribute values for imported 'process' element,
        :param diagram_attributes: dictionary that holds attribute values for imported 'BPMNDiagram' element,
        :param plane_attributes: dictionary that holds attribute values for imported 'BPMNPlane' element.
        """
        document = BPMNDiagramGraphImport.read_xml_file(filepath)
        # We assume that there's only one process element
        process_element = document.getElementsByTagNameNS("*", "process")[0]
        # We assume that there's only one diagram element with one plane element
        diagram_element = document.getElementsByTagNameNS("*", "BPMNDiagram")[0]
        plane_element = diagram_element.getElementsByTagNameNS("*", "BPMNPlane")[0]

        BPMNDiagramGraphImport.add_process_attributes(process_attributes, process_element)
        BPMNDiagramGraphImport.add_diagram_and_plane_attributes(diagram_attributes, plane_attributes,
                                                                diagram_element, plane_element)

        for element in BPMNDiagramGraphImport.iterate_elements(process_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = BPMNDiagramGraphImport.remove_namespace_from_tag_name(element.tagName)
                if tag_name == "task":
                    BPMNDiagramGraphImport.add_task_to_graph(diagram_graph, element, element.getAttribute("id"))
                elif tag_name == "subProcess":
                    BPMNDiagramGraphImport.add_subprocess_to_graph(diagram_graph, element, element.getAttribute("id"))
                elif tag_name == "inclusiveGateway" or tag_name == "exclusiveGateway":
                    BPMNDiagramGraphImport.add_inclusive_or_exclusive_gateway_to_graph(diagram_graph, element,
                                                                                       element.getAttribute("id"))
                elif tag_name == "parallelGateway":
                    BPMNDiagramGraphImport.add_parallel_gateway_to_graph(diagram_graph, element,
                                                                         element.getAttribute("id"))
                elif tag_name == "eventBasedGateway":
                    BPMNDiagramGraphImport.add_event_based_gateway_to_graph(diagram_graph, element,
                                                                            element.getAttribute("id"))
                elif tag_name == "complexGateway":
                    BPMNDiagramGraphImport.add_complex_gateway_to_graph(diagram_graph, element,
                                                                        element.getAttribute("id"))
                elif tag_name == "startEvent":
                    BPMNDiagramGraphImport.add_start_event_to_graph(diagram_graph, element, element.getAttribute("id"))
                elif tag_name == "endEvent":
                    BPMNDiagramGraphImport.add_end_event_to_graph(diagram_graph, element, element.getAttribute("id"))
                elif tag_name == "intermediateCatchEvent":
                    BPMNDiagramGraphImport.add_intermediate_catch_event_to_graph(diagram_graph, element,
                                                                                 element.getAttribute("id"))
                elif tag_name == "intermediateThrowEvent":
                    BPMNDiagramGraphImport.add_intermediate_throw_event_to_graph(diagram_graph, element,
                                                                                 element.getAttribute("id"))

        for flow in BPMNDiagramGraphImport.iterate_elements(process_element):
            if flow.nodeType != flow.TEXT_NODE:
                tag_name = BPMNDiagramGraphImport.remove_namespace_from_tag_name(flow.tagName)
                if tag_name == "sequenceFlow":
                    BPMNDiagramGraphImport.add_edge_to_graph(diagram_graph, sequence_flows, flow)

        for element in BPMNDiagramGraphImport.iterate_elements(plane_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = BPMNDiagramGraphImport.remove_namespace_from_tag_name(element.tagName)
                if tag_name == "BPMNShape":
                    BPMNDiagramGraphImport.add_shape_di(diagram_graph, element)
                elif tag_name == "BPMNEdge":
                    BPMNDiagramGraphImport.add_edge_di(diagram_graph, sequence_flows, element)

    @staticmethod
    def read_xml_file(filepath):
        """
        Reads BPMN 2.0 XML file from given filepath and returns xml.dom.xminidom.Document object.

        :param filepath: filepath of source XML file.
        """
        dom_tree = minidom.parse(filepath)
        return dom_tree

    # Helper methods
    @staticmethod
    def remove_namespace_from_tag_name(tag_name):
        """
        Helper function, removes namespace annotation from tag name.

        :param tag_name: string with tag name.
        """
        return tag_name.split(':')[-1]

    @staticmethod
    def iterate_elements(parent):
        """
        Helper function that iterates over child Nodes/Elements of parent Node/Element.

        :param parent: object of Element class, representing parent element.
        """
        element = parent.firstChild
        while element is not None:
            yield element
            element = element.nextSibling
