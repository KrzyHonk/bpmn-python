import xml.etree.cElementTree as eTree


class BPMNDiagramGraphExport:
    """
    Class BPMNDiagramGraphExport provides methods for exporting BPMNDiagramGraph into BPMN 2.0 XML file.
    As a utility class, it only contains static methods.
    This class is meant to be used from BPMNDiagramGraph class.
    """

    # String "constants" used in multiple places
    bpmndi_namespace = "bpmndi:"

    @staticmethod
    def export_task_info(node_params, output_element):
        """
        Adds Task node attributes to exported XML element

        :param node_params: dictionary with given task parameters,
        :param output_element: object representing BPMN XML 'task' element.
        """
        pass

    @staticmethod
    def export_subprocess_info(node_params, output_element):
        """
        Adds Subprocess node attributes to exported XML element

        :param node_params: dictionary with given subprocess parameters,
        :param output_element: object representing BPMN XML 'subprocess' element.
        """
        output_element.set("triggeredByEvent", node_params["triggeredByEvent"])

    # TODO sequence of conditions
    @staticmethod
    def export_complex_gateway_info(node_params, output_element):
        """
        Adds ComplexGateway node attributes to exported XML element

        :param node_params: dictionary with given complex gateway parameters,
        :param output_element: object representing BPMN XML 'complexGateway' element.
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])
        if node_params["default"] is not None:
            output_element.set("default", node_params["default"])

    @staticmethod
    def export_event_based_gateway_info(node_params, output_element):
        """
        Adds EventBasedGateway node attributes to exported XML element

        :param node_params: dictionary with given event based gateway parameters,
        :param output_element: object representing BPMN XML 'eventBasedGateway' element.
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])
        output_element.set("instantiate", node_params["instantiate"])
        output_element.set("eventGatewayType", node_params["eventGatewayType"])

    @staticmethod
    def export_inclusive_exclusive_gateway_info(node_params, output_element):
        """
        Adds InclusiveGateway or ExclusiveGateway node attributes to exported XML element

        :param node_params: dictionary with given inclusive or exclusive gateway parameters,
        :param output_element: object representing BPMN XML 'inclusiveGateway'/'exclusive' element.
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])
        if node_params["default"] is not None:
            output_element.set("default", node_params["default"])

    @staticmethod
    def export_parallel_gateway_info(node_params, output_element):
        """
        Adds Subprocess node attributes to exported XML element

        :param node_params: dictionary with given parallel gateway parameters,
        :param output_element: object representing BPMN XML 'parallelGateway' element.
        """
        output_element.set("gatewayDirection", node_params["gatewayDirection"])

    @staticmethod
    def export_catch_event_info(node_params, output_element):
        """
        Adds StartEvent or IntermediateCatchEvent attributes to exported XML element

        :param node_params: dictionary with given intermediate catch event parameters,
        :param output_element: object representing BPMN XML 'intermediateCatchEvent' element.
        """
        output_element.set("parallelMultiple", node_params["parallelMultiple"])
        definitions = node_params["event_definitions"]
        for definition in definitions:
            definition_type = definition[0]
            definition_id = definition[1]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set("id", definition_id)

    @staticmethod
    def export_throw_event_info(node_params, output_element):
        """
        Adds EndEvent or IntermediateThrowingEvent attributes to exported XML element

        :param node_params: dictionary with given intermediate throw event parameters,
        :param output_element: object representing BPMN XML 'intermediateThrowEvent' element.
        """
        definitions = node_params["event_definitions"]
        for definition in definitions:
            definition_type = definition[0]
            definition_id = definition[1]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set("id", definition_id)

    @staticmethod
    def create_root_process_output(process_attributes):
        """
        Creates root element ('definitions') and 'process' element for exported BPMN XML file.
        Returns a tuple (root, process).

        :param process_attributes: dictionary that holds attribute values for imported 'process' element.
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
        process.set("id", process_attributes["id"])
        process.set("isClosed", process_attributes["isClosed"])
        process.set("isExecutable", process_attributes["isExecutable"])
        process.set("processType", process_attributes["processType"])

        return root, process

    @staticmethod
    def create_diagram_plane_output(root, diagram_attributes, plane_attributes):
        """
        Creates 'diagram' and 'plane' elements for exported BPMN XML file.
        Returns a tuple (diagram, plane).

        :param root: object of Element class, representing a BPMN XML root element ('definitions'),
        :param diagram_attributes: dictionary that holds attribute values for imported 'BPMNDiagram' element,
        :param plane_attributes: dictionary that holds attribute values for imported 'BPMNPlane' element.
        """
        diagram = eTree.SubElement(root, BPMNDiagramGraphExport.bpmndi_namespace + "BPMNDiagram")
        diagram.set("id", diagram_attributes["id"])
        diagram.set("name", diagram_attributes["name"])

        plane = eTree.SubElement(diagram, BPMNDiagramGraphExport.bpmndi_namespace + "BPMNPlane")
        plane.set("id", plane_attributes["id"])
        plane.set("bpmnElement", plane_attributes["bpmnElement"])

        return diagram, plane

    @staticmethod
    def export_node_process_data(process_id, params, process):
        """
        Creates a new XML element (depends on node type) for given node parameters and adds it to 'process' element.

        :param process_id: string representing ID of given flow node,
        :param params: dictionary with node parameters,
        :param process: object of Element class, representing BPMN XML 'process' element (root for nodes).
        """
        node_type = params["type"]
        output_element = eTree.SubElement(process, node_type)
        output_element.set("id", process_id)
        output_element.set("name", params["name"])

        for incoming in params["incoming"]:
            incoming_element = eTree.SubElement(output_element, "incoming")
            incoming_element.text = incoming
        for outgoing in params["outgoing"]:
            outgoing_element = eTree.SubElement(output_element, "outgoing")
            outgoing_element.text = outgoing

        if node_type == "task":
            BPMNDiagramGraphExport.export_task_info(params, output_element)
        elif node_type == "subProcess":
            BPMNDiagramGraphExport.export_subprocess_info(params, output_element)
        elif node_type == "complexGateway":
            BPMNDiagramGraphExport.export_complex_gateway_info(params, output_element)
        elif node_type == "eventBasedGateway":
            BPMNDiagramGraphExport.export_event_based_gateway_info(params, output_element)
        elif node_type == "inclusiveGateway" or node_type == "exclusiveGateway":
            BPMNDiagramGraphExport.export_inclusive_exclusive_gateway_info(params, output_element)
        elif node_type == "parallelGateway":
            BPMNDiagramGraphExport.export_parallel_gateway_info(params, output_element)
        elif node_type == "startEvent" or node_type == "intermediateCatchEvent":
            BPMNDiagramGraphExport.export_catch_event_info(params, output_element)
        elif node_type == "endEvent" or node_type == "intermediateThrowEvent":
            BPMNDiagramGraphExport.export_throw_event_info(params, output_element)

    @staticmethod
    def export_node_di_data(node_id, params, plane):
        """
        Creates a new BPMNShape XML element for given node parameters and adds it to 'plane' element.

        :param node_id: string representing ID of given flow node,
        :param params: dictionary with node parameters,
        :param plane: object of Element class, representing BPMN XML 'BPMNPlane' element (root for node DI data).
        """
        output_element_di = eTree.SubElement(plane, BPMNDiagramGraphExport.bpmndi_namespace + "BPMNShape")
        output_element_di.set("id", node_id + "_gui")
        output_element_di.set("bpmnElement", node_id)
        bounds = eTree.SubElement(output_element_di, "omgdc:Bounds")
        bounds.set("width", params["width"])
        bounds.set("height", params["height"])
        bounds.set("x", params["x"])
        bounds.set("y", params["y"])

    @staticmethod
    def export_edge_process_data(params, process, source_ref, target_ref):
        """
        Creates a new SequenceFlow XML element for given edge parameters and adds it to 'process' element.

        :param params: dictionary with edge parameters,
        :param process: object of Element class, representing BPMN XML 'process' element (root for sequence flows),
        :param source_ref: string representing ID of source node,
        :param target_ref: string representing ID of taget node.
        """
        output_flow = eTree.SubElement(process, "sequenceFlow")
        output_flow.set("id", params["id"])
        output_flow.set("name", params["name"])
        output_flow.set("sourceRef", source_ref)
        output_flow.set("targetRef", target_ref)

    @staticmethod
    def export_edge_di_data(params, plane):
        """
        Creates a new BPMNEdge XML element for given edge parameters and adds it to 'plane' element.

        :param params: dictionary with edge parameters,
        :param plane: object of Element class, representing BPMN XML 'BPMNPlane' element (root for edge DI data).
        """
        output_flow_edge = eTree.SubElement(plane, BPMNDiagramGraphExport.bpmndi_namespace + "BPMNEdge")
        output_flow_edge.set("id", params["id"] + "_gui")
        output_flow_edge.set("bpmnElement", params["id"])
        waypoints = params["waypoints"]
        for waypoint in waypoints:
            waypoint_element = eTree.SubElement(output_flow_edge, "omgdi:waypoint")
            waypoint_element.set("x", waypoint[0])
            waypoint_element.set("y", waypoint[1])

    @staticmethod
    def export_xml_file(output_path, diagram_graph, sequence_flows,
                        process_attributes, diagram_attributes, plane_attributes):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (with Diagram Interchange data).

        :param output_path: string representing output pathfile,
        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows:- sequence_flows - dictionary (associative list) that uses sequenceFlow ID
        attribute as key and tuple of (sourceRef, targetRef) parameters as value,
        :param process_attributes: dictionary that holds attribute values for imported 'process' element,
        :param diagram_attributes: dictionary that holds attribute values for imported 'BPMNDiagram' element,
        :param plane_attributes: dictionary that holds attribute values for imported 'BPMNPlane' element.
        """
        [root, process] = BPMNDiagramGraphExport.create_root_process_output(process_attributes)
        [_, plane] = BPMNDiagramGraphExport.create_diagram_plane_output(root, diagram_attributes,
                                                                        plane_attributes)

        # for each node in graph add correct type of element, its attributes and BPMNShape element
        nodes = diagram_graph.nodes(data=True)
        for node in nodes:
            node_id = node[0]
            params = node[1]
            BPMNDiagramGraphExport.export_node_process_data(node_id, params, process)
            BPMNDiagramGraphExport.export_node_di_data(node_id, params, plane)

        # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
        edges = diagram_graph.edges(data=True)
        for flow in edges:
            params = flow[2]
            (source_ref, target_ref) = sequence_flows[params["id"]]
            BPMNDiagramGraphExport.export_edge_process_data(params, process, source_ref, target_ref)
            BPMNDiagramGraphExport.export_edge_di_data(params, plane)

        BPMNDiagramGraphExport.indent(root)
        tree = eTree.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)

    @staticmethod
    def export_xml_file_no_di(output_path, diagram_graph, sequence_flows,
                              process_attributes):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (without Diagram Interchange data).

        :param output_path: string representing output pathfile,
        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows:- sequence_flows - dictionary (associative list) that uses sequenceFlow ID
        attribute as key and tuple of (sourceRef, targetRef) parameters as value,
        :param process_attributes: dictionary that holds attribute values for imported 'process' element.
        """
        [root, process] = BPMNDiagramGraphExport.create_root_process_output(process_attributes)

        # for each node in graph add correct type of element, its attributes and BPMNShape element
        nodes = diagram_graph.nodes(data=True)
        for node in nodes:
            node_id = node[0]
            params = node[1]
            BPMNDiagramGraphExport.export_node_process_data(node_id, params, process)

        # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
        edges = diagram_graph.edges(data=True)
        for flow in edges:
            params = flow[2]
            (source_ref, target_ref) = sequence_flows[params["id"]]
            BPMNDiagramGraphExport.export_edge_process_data(params, process, source_ref, target_ref)

        BPMNDiagramGraphExport.indent(root)
        tree = eTree.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)

    # Helper methods
    @staticmethod
    def indent(elem, level=0):
        """
        Helper function, adds indentation to XML output.

        :param elem: object of Element class, representing element to which method adds intendation,
        :param level: current level of intendation.
        """
        i = "\n" + level * "  "
        j = "\n" + (level - 1) * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                BPMNDiagramGraphExport.indent(subelem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem
