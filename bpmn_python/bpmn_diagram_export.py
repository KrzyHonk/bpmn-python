# coding=utf-8
"""
Package provides functionality for exporting graph representation to BPMN 2.0 XML
"""
import errno
import os
import xml.etree.cElementTree as eTree

import bpmn_python.bpmn_python_consts as consts


class BpmnDiagramGraphExport(object):
    """
    Class BPMNDiagramGraphExport provides methods for exporting BPMNDiagramGraph into BPMN 2.0 XML file.
    As a utility class, it only contains static methods.
    This class is meant to be used from BPMNDiagramGraph class.
    """

    def __init__(self):
        pass

    # String "constants" used in multiple places
    bpmndi_namespace = "bpmndi:"

    @staticmethod
    def export_task_info(node_params, output_element):
        """
        Adds Task node attributes to exported XML element

        :param node_params: dictionary with given task parameters,
        :param output_element: object representing BPMN XML 'task' element.
        """
        if consts.Consts.default in node_params and node_params[consts.Consts.default] is not None:
            output_element.set(consts.Consts.default, node_params[consts.Consts.default])

    @staticmethod
    def export_subprocess_info(bpmn_diagram, subprocess_params, output_element):
        """
        Adds Subprocess node attributes to exported XML element

        :param bpmn_diagram: BPMNDiagramGraph class instantion representing a BPMN process diagram,
        :param subprocess_params: dictionary with given subprocess parameters,
        :param output_element: object representing BPMN XML 'subprocess' element.
        """
        output_element.set(consts.Consts.triggered_by_event, subprocess_params[consts.Consts.triggered_by_event])
        if consts.Consts.default in subprocess_params and subprocess_params[consts.Consts.default] is not None:
            output_element.set(consts.Consts.default, subprocess_params[consts.Consts.default])

        # for each node in graph add correct type of element, its attributes and BPMNShape element
        subprocess_id = subprocess_params[consts.Consts.id]
        nodes = bpmn_diagram.get_nodes_list_by_process_id(subprocess_id)
        for node in nodes:
            node_id = node[0]
            params = node[1]
            BpmnDiagramGraphExport.export_node_data(bpmn_diagram, node_id, params, output_element)

        # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
        flows = bpmn_diagram.get_flows_list_by_process_id(subprocess_id)
        for flow in flows:
            params = flow[2]
            BpmnDiagramGraphExport.export_flow_process_data(params, output_element)

    @staticmethod
    def export_data_object_info(bpmn_diagram, data_object_params, output_element):
        """
        Adds DataObject node attributes to exported XML element

        :param bpmn_diagram: BPMNDiagramGraph class instantion representing a BPMN process diagram,
        :param data_object_params: dictionary with given subprocess parameters,
        :param output_element: object representing BPMN XML 'subprocess' element.
        """
        output_element.set(consts.Consts.is_collection, data_object_params[consts.Consts.is_collection])

    # TODO Complex gateway not fully supported
    #  need to find out how sequence of conditions is represented in BPMN 2.0 XML
    @staticmethod
    def export_complex_gateway_info(node_params, output_element):
        """
        Adds ComplexGateway node attributes to exported XML element

        :param node_params: dictionary with given complex gateway parameters,
        :param output_element: object representing BPMN XML 'complexGateway' element.
        """
        output_element.set(consts.Consts.gateway_direction, node_params[consts.Consts.gateway_direction])
        if consts.Consts.default in node_params and node_params[consts.Consts.default] is not None:
            output_element.set(consts.Consts.default, node_params[consts.Consts.default])

    @staticmethod
    def export_event_based_gateway_info(node_params, output_element):
        """
        Adds EventBasedGateway node attributes to exported XML element

        :param node_params: dictionary with given event based gateway parameters,
        :param output_element: object representing BPMN XML 'eventBasedGateway' element.
        """
        output_element.set(consts.Consts.gateway_direction, node_params[consts.Consts.gateway_direction])
        output_element.set(consts.Consts.instantiate, node_params[consts.Consts.instantiate])
        output_element.set(consts.Consts.event_gateway_type, node_params[consts.Consts.event_gateway_type])

    @staticmethod
    def export_inclusive_exclusive_gateway_info(node_params, output_element):
        """
        Adds InclusiveGateway or ExclusiveGateway node attributes to exported XML element

        :param node_params: dictionary with given inclusive or exclusive gateway parameters,
        :param output_element: object representing BPMN XML 'inclusiveGateway'/'exclusive' element.
        """
        output_element.set(consts.Consts.gateway_direction, node_params[consts.Consts.gateway_direction])
        if consts.Consts.default in node_params and node_params[consts.Consts.default] is not None:
            output_element.set(consts.Consts.default, node_params[consts.Consts.default])

    @staticmethod
    def export_parallel_gateway_info(node_params, output_element):
        """
        Adds parallel gateway node attributes to exported XML element

        :param node_params: dictionary with given parallel gateway parameters,
        :param output_element: object representing BPMN XML 'parallelGateway' element.
        """
        output_element.set(consts.Consts.gateway_direction, node_params[consts.Consts.gateway_direction])

    @staticmethod
    def export_catch_event_info(node_params, output_element):
        """
        Adds IntermediateCatchEvent attributes to exported XML element

        :param node_params: dictionary with given intermediate catch event parameters,
        :param output_element: object representing BPMN XML 'intermediateCatchEvent' element.
        """
        output_element.set(consts.Consts.parallel_multiple, node_params[consts.Consts.parallel_multiple])
        definitions = node_params[consts.Consts.event_definitions]
        for definition in definitions:
            definition_id = definition[consts.Consts.id]
            definition_type = definition[consts.Consts.definition_type]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set(consts.Consts.id, definition_id)

    @staticmethod
    def export_start_event_info(node_params, output_element):
        """
        Adds StartEvent attributes to exported XML element

        :param node_params: dictionary with given intermediate catch event parameters,
        :param output_element: object representing BPMN XML 'intermediateCatchEvent' element.
        """
        output_element.set(consts.Consts.parallel_multiple, node_params.get(consts.Consts.parallel_multiple))
        output_element.set(consts.Consts.is_interrupting, node_params.get(consts.Consts.is_interrupting))
        definitions = node_params.get(consts.Consts.event_definitions)
        for definition in definitions:
            definition_id = definition[consts.Consts.id]
            definition_type = definition[consts.Consts.definition_type]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set(consts.Consts.id, definition_id)

    @staticmethod
    def export_throw_event_info(node_params, output_element):
        """
        Adds EndEvent or IntermediateThrowingEvent attributes to exported XML element

        :param node_params: dictionary with given intermediate throw event parameters,
        :param output_element: object representing BPMN XML 'intermediateThrowEvent' element.
        """
        definitions = node_params[consts.Consts.event_definitions]
        for definition in definitions:
            definition_id = definition[consts.Consts.id]
            definition_type = definition[consts.Consts.definition_type]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set(consts.Consts.id, definition_id)

    @staticmethod
    def export_boundary_event_info(node_params, output_element):
        """
        Adds IntermediateCatchEvent attributes to exported XML element

        :param node_params: dictionary with given intermediate catch event parameters,
        :param output_element: object representing BPMN XML 'intermediateCatchEvent' element.
        """
        output_element.set(consts.Consts.parallel_multiple, node_params[consts.Consts.parallel_multiple])
        output_element.set(consts.Consts.cancel_activity, node_params[consts.Consts.cancel_activity])
        output_element.set(consts.Consts.attached_to_ref, node_params[consts.Consts.attached_to_ref])
        definitions = node_params[consts.Consts.event_definitions]
        for definition in definitions:
            definition_id = definition[consts.Consts.id]
            definition_type = definition[consts.Consts.definition_type]
            output_definition = eTree.SubElement(output_element, definition_type)
            if definition_id != "":
                output_definition.set(consts.Consts.id, definition_id)

    @staticmethod
    def export_definitions_element():
        """
        Creates root element ('definitions') for exported BPMN XML file.

        :return: definitions XML element.
        """
        root = eTree.Element(consts.Consts.definitions)
        root.set("xmlns", "http://www.omg.org/spec/BPMN/20100524/MODEL")
        root.set("xmlns:bpmndi", "http://www.omg.org/spec/BPMN/20100524/DI")
        root.set("xmlns:omgdc", "http://www.omg.org/spec/DD/20100524/DC")
        root.set("xmlns:omgdi", "http://www.omg.org/spec/DD/20100524/DI")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("targetNamespace", "http://www.signavio.com/bpmn20")
        root.set("typeLanguage", "http://www.w3.org/2001/XMLSchema")
        root.set("expressionLanguage", "http://www.w3.org/1999/XPath")
        root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")

        return root

    @staticmethod
    def export_process_element(definitions, process_id, process_attributes_dictionary):
        """
        Creates process element for exported BPMN XML file.

        :param process_id: string object. ID of exported process element,
        :param definitions: an XML element ('definitions'), root element of BPMN 2.0 document
        :param process_attributes_dictionary: dictionary that holds attribute values of 'process' element
        :return: process XML element
        """
        process = eTree.SubElement(definitions, consts.Consts.process)
        process.set(consts.Consts.id, process_id)
        process.set(consts.Consts.is_closed, process_attributes_dictionary[consts.Consts.is_closed])
        process.set(consts.Consts.is_executable, process_attributes_dictionary[consts.Consts.is_executable])
        process.set(consts.Consts.process_type, process_attributes_dictionary[consts.Consts.process_type])

        return process

    @staticmethod
    def export_lane_set(process, lane_set, plane_element):
        """
        Creates 'laneSet' element for exported BPMN XML file.

        :param process: an XML element ('process'), from exported BPMN 2.0 document,
        :param lane_set: dictionary with exported 'laneSet' element attributes and child elements,
        :param plane_element: XML object, representing 'plane' element of exported BPMN 2.0 XML.
        """
        lane_set_xml = eTree.SubElement(process, consts.Consts.lane_set)
        for key, value in lane_set[consts.Consts.lanes].items():
            BpmnDiagramGraphExport.export_lane(lane_set_xml, key, value, plane_element)

    @staticmethod
    def export_child_lane_set(parent_xml_element, child_lane_set, plane_element):
        """
        Creates 'childLaneSet' element for exported BPMN XML file.

        :param parent_xml_element: an XML element, parent of exported 'childLaneSet' element,
        :param child_lane_set: dictionary with exported 'childLaneSet' element attributes and child elements,
        :param plane_element: XML object, representing 'plane' element of exported BPMN 2.0 XML.
        """
        lane_set_xml = eTree.SubElement(parent_xml_element, consts.Consts.lane_set)
        for key, value in child_lane_set[consts.Consts.lanes].items():
            BpmnDiagramGraphExport.export_lane(lane_set_xml, key, value, plane_element)

    @staticmethod
    def export_lane(parent_xml_element, lane_id, lane_attr, plane_element):
        """
        Creates 'lane' element for exported BPMN XML file.

        :param parent_xml_element: an XML element, parent of exported 'lane' element,
        :param lane_id: string object. ID of exported lane element,
        :param lane_attr: dictionary with lane element attributes,
        :param plane_element: XML object, representing 'plane' element of exported BPMN 2.0 XML.
        """
        lane_xml = eTree.SubElement(parent_xml_element, consts.Consts.lane)
        lane_xml.set(consts.Consts.id, lane_id)
        lane_xml.set(consts.Consts.name, lane_attr[consts.Consts.name])
        if consts.Consts.child_lane_set in lane_attr and len(lane_attr[consts.Consts.child_lane_set]):
            child_lane_set = lane_attr[consts.Consts.child_lane_set]
            BpmnDiagramGraphExport.export_child_lane_set(lane_xml, child_lane_set, plane_element)
        if consts.Consts.flow_node_refs in lane_attr and len(lane_attr[consts.Consts.flow_node_refs]):
            for flow_node_ref_id in lane_attr[consts.Consts.flow_node_refs]:
                flow_node_ref_xml = eTree.SubElement(lane_xml, consts.Consts.flow_node_ref)
                flow_node_ref_xml.text = flow_node_ref_id

        output_element_di = eTree.SubElement(plane_element, BpmnDiagramGraphExport.bpmndi_namespace +
                                             consts.Consts.bpmn_shape)
        output_element_di.set(consts.Consts.id, lane_id + "_gui")

        output_element_di.set(consts.Consts.bpmn_element, lane_id)
        output_element_di.set(consts.Consts.is_horizontal, lane_attr[consts.Consts.is_horizontal])
        bounds = eTree.SubElement(output_element_di, "omgdc:Bounds")
        bounds.set(consts.Consts.width, lane_attr[consts.Consts.width])
        bounds.set(consts.Consts.height, lane_attr[consts.Consts.height])
        bounds.set(consts.Consts.x, lane_attr[consts.Consts.x])
        bounds.set(consts.Consts.y, lane_attr[consts.Consts.y])

    @staticmethod
    def export_diagram_plane_elements(root, diagram_attributes, plane_attributes):
        """
        Creates 'diagram' and 'plane' elements for exported BPMN XML file.
        Returns a tuple (diagram, plane).

        :param root: object of Element class, representing a BPMN XML root element ('definitions'),
        :param diagram_attributes: dictionary that holds attribute values for imported 'BPMNDiagram' element,
        :param plane_attributes: dictionary that holds attribute values for imported 'BPMNPlane' element.
        """
        diagram = eTree.SubElement(root, BpmnDiagramGraphExport.bpmndi_namespace + "BPMNDiagram")
        diagram.set(consts.Consts.id, diagram_attributes[consts.Consts.id])
        diagram.set(consts.Consts.name, diagram_attributes[consts.Consts.name])

        plane = eTree.SubElement(diagram, BpmnDiagramGraphExport.bpmndi_namespace + "BPMNPlane")
        plane.set(consts.Consts.id, plane_attributes[consts.Consts.id])
        plane.set(consts.Consts.bpmn_element, plane_attributes[consts.Consts.bpmn_element])

        return diagram, plane

    @staticmethod
    def export_node_data(bpmn_diagram, process_id, params, process):
        """
        Creates a new XML element (depends on node type) for given node parameters and adds it to 'process' element.

        :param bpmn_diagram: BPMNDiagramGraph class instantion representing a BPMN process diagram,
        :param process_id: string representing ID of given flow node,
        :param params: dictionary with node parameters,
        :param process: object of Element class, representing BPMN XML 'process' element (root for nodes).
        """
        node_type = params[consts.Consts.type]
        output_element = eTree.SubElement(process, node_type)
        output_element.set(consts.Consts.id, process_id)
        output_element.set(consts.Consts.name, params[consts.Consts.node_name])

        for incoming in params[consts.Consts.incoming_flow]:
            incoming_element = eTree.SubElement(output_element, consts.Consts.incoming_flow)
            incoming_element.text = incoming
        for outgoing in params[consts.Consts.outgoing_flow]:
            outgoing_element = eTree.SubElement(output_element, consts.Consts.outgoing_flow)
            outgoing_element.text = outgoing

        if node_type == consts.Consts.task \
                or node_type == consts.Consts.user_task \
                or node_type == consts.Consts.service_task \
                or node_type == consts.Consts.manual_task:
            BpmnDiagramGraphExport.export_task_info(params, output_element)
        elif node_type == consts.Consts.subprocess:
            BpmnDiagramGraphExport.export_subprocess_info(bpmn_diagram, params, output_element)
        elif node_type == consts.Consts.data_object:
            BpmnDiagramGraphExport.export_data_object_info(bpmn_diagram, params, output_element)
        elif node_type == consts.Consts.complex_gateway:
            BpmnDiagramGraphExport.export_complex_gateway_info(params, output_element)
        elif node_type == consts.Consts.event_based_gateway:
            BpmnDiagramGraphExport.export_event_based_gateway_info(params, output_element)
        elif node_type == consts.Consts.inclusive_gateway or node_type == consts.Consts.exclusive_gateway:
            BpmnDiagramGraphExport.export_inclusive_exclusive_gateway_info(params, output_element)
        elif node_type == consts.Consts.parallel_gateway:
            BpmnDiagramGraphExport.export_parallel_gateway_info(params, output_element)
        elif node_type == consts.Consts.start_event:
            BpmnDiagramGraphExport.export_start_event_info(params, output_element)
        elif node_type == consts.Consts.intermediate_catch_event:
            BpmnDiagramGraphExport.export_catch_event_info(params, output_element)
        elif node_type == consts.Consts.end_event or node_type == consts.Consts.intermediate_throw_event:
            BpmnDiagramGraphExport.export_throw_event_info(params, output_element)
        elif node_type == consts.Consts.boundary_event:
            BpmnDiagramGraphExport.export_boundary_event_info(params, output_element)

    @staticmethod
    def export_node_di_data(node_id, params, plane):
        """
        Creates a new BPMNShape XML element for given node parameters and adds it to 'plane' element.

        :param node_id: string representing ID of given flow node,
        :param params: dictionary with node parameters,
        :param plane: object of Element class, representing BPMN XML 'BPMNPlane' element (root for node DI data).
        """
        output_element_di = eTree.SubElement(plane, BpmnDiagramGraphExport.bpmndi_namespace + consts.Consts.bpmn_shape)
        output_element_di.set(consts.Consts.id, node_id + "_gui")

        output_element_di.set(consts.Consts.bpmn_element, node_id)
        bounds = eTree.SubElement(output_element_di, "omgdc:Bounds")
        bounds.set(consts.Consts.width, params[consts.Consts.width])
        bounds.set(consts.Consts.height, params[consts.Consts.height])
        bounds.set(consts.Consts.x, params[consts.Consts.x])
        bounds.set(consts.Consts.y, params[consts.Consts.y])
        if params[consts.Consts.type] == consts.Consts.subprocess:
            output_element_di.set(consts.Consts.is_expanded, params[consts.Consts.is_expanded])

    @staticmethod
    def export_flow_process_data(params, process):
        """
        Creates a new SequenceFlow XML element for given edge parameters and adds it to 'process' element.

        :param params: dictionary with edge parameters,
        :param process: object of Element class, representing BPMN XML 'process' element (root for sequence flows)
        """
        output_flow = eTree.SubElement(process, consts.Consts.sequence_flow)
        output_flow.set(consts.Consts.id, params[consts.Consts.id])
        output_flow.set(consts.Consts.name, params[consts.Consts.name])
        output_flow.set(consts.Consts.source_ref, params[consts.Consts.source_ref])
        output_flow.set(consts.Consts.target_ref, params[consts.Consts.target_ref])
        if consts.Consts.condition_expression in params:
            condition_expression_params = params[consts.Consts.condition_expression]
            condition_expression = eTree.SubElement(output_flow, consts.Consts.condition_expression)
            condition_expression.set(consts.Consts.id, condition_expression_params[consts.Consts.id])
            condition_expression.set(consts.Consts.id, condition_expression_params[consts.Consts.id])
            condition_expression.text = condition_expression_params[consts.Consts.condition_expression]
            output_flow.set(consts.Consts.name, condition_expression_params[consts.Consts.condition_expression])

    @staticmethod
    def export_flow_di_data(params, plane):
        """
        Creates a new BPMNEdge XML element for given edge parameters and adds it to 'plane' element.

        :param params: dictionary with edge parameters,
        :param plane: object of Element class, representing BPMN XML 'BPMNPlane' element (root for edge DI data).
        """
        output_flow = eTree.SubElement(plane, BpmnDiagramGraphExport.bpmndi_namespace + consts.Consts.bpmn_edge)
        output_flow.set(consts.Consts.id, params[consts.Consts.id] + "_gui")
        output_flow.set(consts.Consts.bpmn_element, params[consts.Consts.id])
        waypoints = params[consts.Consts.waypoints]
        for waypoint in waypoints:
            waypoint_element = eTree.SubElement(output_flow, "omgdi:waypoint")
            waypoint_element.set(consts.Consts.x, waypoint[0])
            waypoint_element.set(consts.Consts.y, waypoint[1])

    @staticmethod
    def export_xml_file(directory, filename, bpmn_diagram):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (with Diagram Interchange data).

        :param directory: string representing output directory,
        :param filename: string representing output file name,
        :param bpmn_diagram: BPMNDiagramGraph class instantion representing a BPMN process diagram.
        """
        diagram_attributes = bpmn_diagram.diagram_attributes
        plane_attributes = bpmn_diagram.plane_attributes
        collaboration = bpmn_diagram.collaboration
        process_elements_dict = bpmn_diagram.process_elements
        definitions = BpmnDiagramGraphExport.export_definitions_element()

        [_, plane] = BpmnDiagramGraphExport.export_diagram_plane_elements(definitions, diagram_attributes,
                                                                          plane_attributes)

        if collaboration is not None and len(collaboration) > 0:
            message_flows = collaboration[consts.Consts.message_flows]
            participants = collaboration[consts.Consts.participants]
            collaboration_xml = eTree.SubElement(definitions, consts.Consts.collaboration)
            collaboration_xml.set(consts.Consts.id, collaboration[consts.Consts.id])

            for message_flow_id, message_flow_attr in message_flows.items():
                message_flow = eTree.SubElement(collaboration_xml, consts.Consts.message_flow)
                message_flow.set(consts.Consts.id, message_flow_id)
                message_flow.set(consts.Consts.name, message_flow_attr[consts.Consts.name])
                message_flow.set(consts.Consts.source_ref, message_flow_attr[consts.Consts.source_ref])
                message_flow.set(consts.Consts.target_ref, message_flow_attr[consts.Consts.target_ref])

                message_flow_params = bpmn_diagram.get_flow_by_id(message_flow_id)[2]
                output_flow = eTree.SubElement(plane, BpmnDiagramGraphExport.bpmndi_namespace + consts.Consts.bpmn_edge)
                output_flow.set(consts.Consts.id, message_flow_id + "_gui")
                output_flow.set(consts.Consts.bpmn_element, message_flow_id)
                waypoints = message_flow_params[consts.Consts.waypoints]
                for waypoint in waypoints:
                    waypoint_element = eTree.SubElement(output_flow, "omgdi:waypoint")
                    waypoint_element.set(consts.Consts.x, waypoint[0])
                    waypoint_element.set(consts.Consts.y, waypoint[1])

            for participant_id, participant_attr in participants.items():
                participant = eTree.SubElement(collaboration_xml, consts.Consts.participant)
                participant.set(consts.Consts.id, participant_id)
                participant.set(consts.Consts.name, participant_attr[consts.Consts.name])
                participant.set(consts.Consts.process_ref, participant_attr[consts.Consts.process_ref])

                output_element_di = eTree.SubElement(plane, BpmnDiagramGraphExport.bpmndi_namespace +
                                                     consts.Consts.bpmn_shape)
                output_element_di.set(consts.Consts.id, participant_id + "_gui")
                output_element_di.set(consts.Consts.bpmn_element, participant_id)
                output_element_di.set(consts.Consts.is_horizontal, participant_attr[consts.Consts.is_horizontal])
                bounds = eTree.SubElement(output_element_di, "omgdc:Bounds")
                bounds.set(consts.Consts.width, participant_attr[consts.Consts.width])
                bounds.set(consts.Consts.height, participant_attr[consts.Consts.height])
                bounds.set(consts.Consts.x, participant_attr[consts.Consts.x])
                bounds.set(consts.Consts.y, participant_attr[consts.Consts.y])

        for process_id in process_elements_dict:
            process_element_attr = process_elements_dict[process_id]
            process = BpmnDiagramGraphExport.export_process_element(definitions, process_id, process_element_attr)
            if consts.Consts.lane_set in process_element_attr:
                BpmnDiagramGraphExport.export_lane_set(process, process_element_attr[consts.Consts.lane_set], plane)

            # for each node in graph add correct type of element, its attributes and BPMNShape element
            nodes = bpmn_diagram.get_nodes_list_by_process_id(process_id)
            for node in nodes:
                node_id = node[0]
                params = node[1]
                BpmnDiagramGraphExport.export_node_data(bpmn_diagram, node_id, params, process)
                # BpmnDiagramGraphExport.export_node_di_data(node_id, params, plane)

            # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
            flows = bpmn_diagram.get_flows_list_by_process_id(process_id)
            for flow in flows:
                params = flow[2]
                BpmnDiagramGraphExport.export_flow_process_data(params, process)
                # BpmnDiagramGraphExport.export_flow_di_data(params, plane)

        # Export DI data
        nodes = bpmn_diagram.get_nodes()
        for node in nodes:
            node_id = node[0]
            params = node[1]
            BpmnDiagramGraphExport.export_node_di_data(node_id, params, plane)

        flows = bpmn_diagram.get_flows()
        for flow in flows:
            params = flow[2]
            BpmnDiagramGraphExport.export_flow_di_data(params, plane)

        BpmnDiagramGraphExport.indent(definitions)
        tree = eTree.ElementTree(definitions)
        try:
            os.makedirs(directory)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        tree.write(directory + filename, encoding='utf-8', xml_declaration=True)

    @staticmethod
    def export_xml_file_no_di(directory, filename, bpmn_diagram):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (without Diagram Interchange data).

        :param directory: string representing output directory,
        :param filename: string representing output file name,
        :param bpmn_diagram: BPMNDiagramGraph class instance representing a BPMN process diagram.
        """
        diagram_graph = bpmn_diagram.diagram_graph
        process_elements_dict = bpmn_diagram.process_elements
        definitions = BpmnDiagramGraphExport.export_definitions_element()

        for process_id in process_elements_dict:
            process_element_attr = process_elements_dict[process_id]
            process = BpmnDiagramGraphExport.export_process_element(definitions, process_id, process_element_attr)

            # for each node in graph add correct type of element, its attributes and BPMNShape element
            nodes = diagram_graph.nodes(data=True)
            for node in nodes:
                node_id = node[0]
                params = node[1]
                BpmnDiagramGraphExport.export_node_data(bpmn_diagram, node_id, params, process)

            # for each edge in graph add sequence flow element, its attributes and BPMNEdge element
            flows = diagram_graph.edges(data=True)
            for flow in flows:
                params = flow[2]
                BpmnDiagramGraphExport.export_flow_process_data(params, process)

        BpmnDiagramGraphExport.indent(definitions)
        tree = eTree.ElementTree(definitions)
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
