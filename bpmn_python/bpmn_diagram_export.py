# coding=utf-8
"""
Package provides functionality for exporting graph representation to BPMN 2.0 XML
"""
import errno
import os
import xml.etree.cElementTree as eTree


class BpmnDiagramGraphExport:
    """
    Class BPMNDiagramGraphExport provides methods for exporting BPMNDiagramGraph into BPMN 2.0 XML file.
    As a utility class, it only contains static methods.
    This class is meant to be used from BPMNDiagramGraph class.
    """

    def __init__(self):
        pass

    # String "constants" used in multiple places
    bpmndi_namespace = "bpmndi:"
    gateway_direction_param_name = "gatewayDirection"
    id_param_name = "id"
    waypoints_param_name = "waypoints"
    bpmn_element_param_name = "bpmnElement"
    default_param_name = "default"

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

    # TODO Complex gateway not fully supported
    #  need to find out how sequence of conditions is represented in BPMN 2.0 XML
    @staticmethod
    def export_complex_gateway_info(node_params, output_element):
        """
        Adds ComplexGateway node attributes to exported XML element

        :param node_params: dictionary with given complex gateway parameters,
        :param output_element: object representing BPMN XML 'complexGateway' element.
        """
        output_element.set(BpmnDiagramGraphExport.gateway_direction_param_name,
                           node_params[BpmnDiagramGraphExport.gateway_direction_param_name])
        if node_params[BpmnDiagramGraphExport.default_param_name] is not None:
            output_element.set(BpmnDiagramGraphExport.default_param_name,
                               node_params[BpmnDiagramGraphExport.default_param_name])

    @staticmethod
    def export_event_based_gateway_info(node_params, output_element):
        """
        Adds EventBasedGateway node attributes to exported XML element

        :param node_params: dictionary with given event based gateway parameters,
        :param output_element: object representing BPMN XML 'eventBasedGateway' element.
        """
        output_element.set(BpmnDiagramGraphExport.gateway_direction_param_name,
                           node_params[BpmnDiagramGraphExport.gateway_direction_param_name])
        output_element.set("instantiate", node_params["instantiate"])
        output_element.set("eventGatewayType", node_params["eventGatewayType"])

    @staticmethod
    def export_inclusive_exclusive_gateway_info(node_params, output_element):
        """
        Adds InclusiveGateway or ExclusiveGateway node attributes to exported XML element

        :param node_params: dictionary with given inclusive or exclusive gateway parameters,
        :param output_element: object representing BPMN XML 'inclusiveGateway'/'exclusive' element.
        """
        output_element.set(BpmnDiagramGraphExport.gateway_direction_param_name,
                           node_params[BpmnDiagramGraphExport.gateway_direction_param_name])
        if node_params[BpmnDiagramGraphExport.default_param_name] is not None:
            output_element.set(BpmnDiagramGraphExport.default_param_name,
                               node_params[BpmnDiagramGraphExport.default_param_name])

    @staticmethod
    def export_parallel_gateway_info(node_params, output_element):
        """
        Adds Subprocess node attributes to exported XML element

        :param node_params: dictionary with given parallel gateway parameters,
        :param output_element: object representing BPMN XML 'parallelGateway' element.
        """
        output_element.set(BpmnDiagramGraphExport.gateway_direction_param_name,
                           node_params[BpmnDiagramGraphExport.gateway_direction_param_name])

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
                output_definition.set(BpmnDiagramGraphExport.id_param_name, definition_id)

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
                output_definition.set(BpmnDiagramGraphExport.id_param_name, definition_id)

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
        process.set(BpmnDiagramGraphExport.id_param_name, process_attributes[BpmnDiagramGraphExport.id_param_name])
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
        diagram = eTree.SubElement(root, BpmnDiagramGraphExport.bpmndi_namespace + "BPMNDiagram")
        diagram.set(BpmnDiagramGraphExport.id_param_name, diagram_attributes[BpmnDiagramGraphExport.id_param_name])
        diagram.set("name", diagram_attributes["name"])

        plane = eTree.SubElement(diagram, BpmnDiagramGraphExport.bpmndi_namespace + "BPMNPlane")
        plane.set(BpmnDiagramGraphExport.id_param_name, plane_attributes[BpmnDiagramGraphExport.id_param_name])
        plane.set(BpmnDiagramGraphExport.bpmn_element_param_name,
                  plane_attributes[BpmnDiagramGraphExport.bpmn_element_param_name])

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
        output_element.set(BpmnDiagramGraphExport.id_param_name, process_id)
        output_element.set("name", params["node_name"])

        for incoming in params["incoming"]:
            incoming_element = eTree.SubElement(output_element, "incoming")
            incoming_element.text = incoming
        for outgoing in params["outgoing"]:
            outgoing_element = eTree.SubElement(output_element, "outgoing")
            outgoing_element.text = outgoing

        if node_type == "task":
            BpmnDiagramGraphExport.export_task_info(params, output_element)
        elif node_type == "subProcess":
            BpmnDiagramGraphExport.export_subprocess_info(params, output_element)
        elif node_type == "complexGateway":
            BpmnDiagramGraphExport.export_complex_gateway_info(params, output_element)
        elif node_type == "eventBasedGateway":
            BpmnDiagramGraphExport.export_event_based_gateway_info(params, output_element)
        elif node_type == "inclusiveGateway" or node_type == "exclusiveGateway":
            BpmnDiagramGraphExport.export_inclusive_exclusive_gateway_info(params, output_element)
        elif node_type == "parallelGateway":
            BpmnDiagramGraphExport.export_parallel_gateway_info(params, output_element)
        elif node_type == "startEvent" or node_type == "intermediateCatchEvent":
            BpmnDiagramGraphExport.export_catch_event_info(params, output_element)
        elif node_type == "endEvent" or node_type == "intermediateThrowEvent":
            BpmnDiagramGraphExport.export_throw_event_info(params, output_element)

    @staticmethod
    def export_node_di_data(node_id, params, plane):
        """
        Creates a new BPMNShape XML element for given node parameters and adds it to 'plane' element.

        :param node_id: string representing ID of given flow node,
        :param params: dictionary with node parameters,
        :param plane: object of Element class, representing BPMN XML 'BPMNPlane' element (root for node DI data).
        """
        output_element_di = eTree.SubElement(plane, BpmnDiagramGraphExport.bpmndi_namespace + "BPMNShape")
        output_element_di.set(BpmnDiagramGraphExport.id_param_name, node_id + "_gui")

        output_element_di.set(BpmnDiagramGraphExport.bpmn_element_param_name, node_id)
        bounds = eTree.SubElement(output_element_di, "omgdc:Bounds")
        bounds.set("width", params["width"])
        bounds.set("height", params["height"])
        bounds.set("x", params["x"])
        bounds.set("y", params["y"])
        if params["type"] == "subProcess":
            output_element_di.set("isExpanded", params["isExpanded"])

    @staticmethod
    def export_flow_process_data(params, process):
        """
        Creates a new SequenceFlow XML element for given edge parameters and adds it to 'process' element.

        :param params: dictionary with edge parameters,
        :param process: object of Element class, representing BPMN XML 'process' element (root for sequence flows)
        """
        output_flow = eTree.SubElement(process, "sequenceFlow")
        output_flow.set(BpmnDiagramGraphExport.id_param_name, params[BpmnDiagramGraphExport.id_param_name])
        output_flow.set("name", params["name"])
        output_flow.set("sourceRef", params["source_id"])
        output_flow.set("targetRef", params["target_id"])

    @staticmethod
    def export_flow_di_data(params, plane):
        """
        Creates a new BPMNEdge XML element for given edge parameters and adds it to 'plane' element.

        :param params: dictionary with edge parameters,
        :param plane: object of Element class, representing BPMN XML 'BPMNPlane' element (root for edge DI data).
        """
        output_flow = eTree.SubElement(plane, BpmnDiagramGraphExport.bpmndi_namespace + "BPMNEdge")
        output_flow.set(BpmnDiagramGraphExport.id_param_name, params[BpmnDiagramGraphExport.id_param_name] + "_gui")
        output_flow.set(BpmnDiagramGraphExport.bpmn_element_param_name, params[BpmnDiagramGraphExport.id_param_name])
        waypoints = params[BpmnDiagramGraphExport.waypoints_param_name]
        for waypoint in waypoints:
            waypoint_element = eTree.SubElement(output_flow, "omgdi:waypoint")
            waypoint_element.set("x", waypoint[0])
            waypoint_element.set("y", waypoint[1])

    @staticmethod
    def export_xml_file(directory, filename, bpmn_graph, process_attributes, diagram_attributes, plane_attributes):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (with Diagram Interchange data).

        :param directory: string representing output directory,
        :param filename: string representing output file name,
        :param bpmn_graph: BPMNDiagramGraph class instantion representing a BPMN process diagram,
        :param process_attributes: dictionary that holds attribute values for imported 'process' element,
        :param diagram_attributes: dictionary that holds attribute values for imported 'BPMNDiagram' element,
        :param plane_attributes: dictionary that holds attribute values for imported 'BPMNPlane' element.
        """
        [root, process] = BpmnDiagramGraphExport.create_root_process_output(process_attributes)
        [_, plane] = BpmnDiagramGraphExport.create_diagram_plane_output(root, diagram_attributes, plane_attributes)
        graph = bpmn_graph.diagram_graph

        # for each node in graph add correct type of element, its attributes and BPMNShape element
        nodes = graph.nodes(data=True)
        for node in nodes:
            node_id = node[0]
            params = node[1]
            BpmnDiagramGraphExport.export_node_process_data(node_id, params, process)
            BpmnDiagramGraphExport.export_node_di_data(node_id, params, plane)

        # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
        flows = graph.edges(data=True)
        for flow in flows:
            params = flow[2]
            BpmnDiagramGraphExport.export_flow_process_data(params, process)
            BpmnDiagramGraphExport.export_flow_di_data(params, plane)

        BpmnDiagramGraphExport.indent(root)
        tree = eTree.ElementTree(root)
        try:
            os.makedirs(directory)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        tree.write(directory + filename, encoding='utf-8', xml_declaration=True)

    @staticmethod
    def export_xml_file_no_di(directory, filename, graph, process_attributes):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (without Diagram Interchange data).

        :param directory: string representing output directory,
        :param filename: string representing output file name,
        :param graph: NetworkX graph representing a BPMN process diagram,
        :param process_attributes: dictionary that holds attribute values for imported 'process' element.
        """
        [root, process] = BpmnDiagramGraphExport.create_root_process_output(process_attributes)

        # for each node in graph add correct type of element, its attributes and BPMNShape element
        nodes = graph.nodes(data=True)
        for node in nodes:
            node_id = node[0]
            params = node[1]
            BpmnDiagramGraphExport.export_node_process_data(node_id, params, process)

        # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
        flows = graph.edges(data=True)
        for flow in flows:
            params = flow[2]
            BpmnDiagramGraphExport.export_flow_process_data(params, process)

        BpmnDiagramGraphExport.indent(root)
        tree = eTree.ElementTree(root)
        try:
            os.makedirs(directory)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        tree.write(directory + filename, encoding='utf-8', xml_declaration=True)

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
                BpmnDiagramGraphExport.indent(subelem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem
