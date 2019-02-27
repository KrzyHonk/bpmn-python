# coding=utf-8
"""
Package provides functionality for importing from BPMN 2.0 XML to graph representation
"""
from xml.dom import minidom

import bpmn_python.bpmn_import_utils as utils
import bpmn_python.bpmn_python_consts as consts


class BpmnDiagramGraphImport(object):
    """
    Class BPMNDiagramGraphImport provides methods for importing BPMN 2.0 XML file.
    As a utility class, it only contains static methods. This class is meant to be used from BPMNDiagramGraph class.
    """

    def __init__(self):
        pass

    @staticmethod
    def load_diagram_from_xml(filepath, bpmn_diagram):
        """
        Reads an XML file from given filepath and maps it into inner representation of BPMN diagram.
        Returns an instance of BPMNDiagramGraph class.

        :param filepath: string with output filepath,
        :param bpmn_diagram: an instance of BpmnDiagramGraph class.
        """
        diagram_graph = bpmn_diagram.diagram_graph
        sequence_flows = bpmn_diagram.sequence_flows
        process_elements_dict = bpmn_diagram.process_elements
        diagram_attributes = bpmn_diagram.diagram_attributes
        plane_attributes = bpmn_diagram.plane_attributes
        collaboration = bpmn_diagram.collaboration

        document = BpmnDiagramGraphImport.read_xml_file(filepath)
        # According to BPMN 2.0 XML Schema, there's only one 'BPMNDiagram' and 'BPMNPlane'
        diagram_element = document.getElementsByTagNameNS("*", "BPMNDiagram")[0]
        plane_element = diagram_element.getElementsByTagNameNS("*", "BPMNPlane")[0]
        BpmnDiagramGraphImport.import_diagram_and_plane_attributes(diagram_attributes, plane_attributes,
                                                                   diagram_element, plane_element)

        BpmnDiagramGraphImport.import_process_elements(document, diagram_graph, sequence_flows, process_elements_dict,
                                                       plane_element)

        collaboration_element_list = document.getElementsByTagNameNS("*", consts.Consts.collaboration)
        if collaboration_element_list is not None and len(collaboration_element_list) > 0:
            # Diagram has multiple pools and lanes
            collaboration_element = collaboration_element_list[0]
            BpmnDiagramGraphImport.import_collaboration_element(diagram_graph, collaboration_element, collaboration)

        if consts.Consts.message_flows in collaboration:
            message_flows = collaboration[consts.Consts.message_flows]
        else:
            message_flows = {}

        participants = []
        if consts.Consts.participants in collaboration:
            participants = collaboration[consts.Consts.participants]

        for element in utils.BpmnImportUtils.iterate_elements(plane_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                if tag_name == consts.Consts.bpmn_shape:
                    BpmnDiagramGraphImport.import_shape_di(participants, diagram_graph, element)
                elif tag_name == consts.Consts.bpmn_edge:
                    BpmnDiagramGraphImport.import_flow_di(diagram_graph, sequence_flows, message_flows, element)

    @staticmethod
    def import_collaboration_element(diagram_graph, collaboration_element, collaboration_dict):
        """
        Method that imports information from 'collaboration' element.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param collaboration_element: XML doument element,
        :param collaboration_dict: dictionary, that consist all information imported from 'collaboration' element.
            Includes three key-value pairs - 'id' which keeps ID of collaboration element, 'participants' that keeps
            information about 'participant' elements and 'message_flows' that keeps information about message flows.
        """
        collaboration_dict[consts.Consts.id] = collaboration_element.getAttribute(consts.Consts.id)
        collaboration_dict[consts.Consts.participants] = {}
        participants_dict = collaboration_dict[consts.Consts.participants]
        collaboration_dict[consts.Consts.message_flows] = {}
        message_flows_dict = collaboration_dict[consts.Consts.message_flows]

        for element in utils.BpmnImportUtils.iterate_elements(collaboration_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                if tag_name == consts.Consts.participant:
                    BpmnDiagramGraphImport.import_participant_element(diagram_graph, participants_dict, element)
                elif tag_name == consts.Consts.message_flow:
                    BpmnDiagramGraphImport.import_message_flow_to_graph(diagram_graph, message_flows_dict, element)

    @staticmethod
    def import_participant_element(diagram_graph, participants_dictionary, participant_element):
        """
        Adds 'participant' element to the collaboration dictionary.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param participants_dictionary: dictionary with participant element attributes. Key is participant ID, value
           is a dictionary of participant attributes,
        :param participant_element: object representing a BPMN XML 'participant' element.
        """
        participant_id = participant_element.getAttribute(consts.Consts.id)
        name = participant_element.getAttribute(consts.Consts.name)
        process_ref = participant_element.getAttribute(consts.Consts.process_ref)
        if participant_element.getAttribute(consts.Consts.process_ref) == '':
            diagram_graph.add_node(participant_id)
            diagram_graph.node[participant_id][consts.Consts.type] = consts.Consts.participant
            diagram_graph.node[participant_id][consts.Consts.process] = participant_id
        participants_dictionary[participant_id] = {consts.Consts.name: name, consts.Consts.process_ref: process_ref}

    @staticmethod
    def import_diagram_and_plane_attributes(diagram_attributes, plane_attributes, diagram_element, plane_element):
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
        diagram_attributes[consts.Consts.id] = diagram_element.getAttribute(consts.Consts.id)
        diagram_attributes[consts.Consts.name] = diagram_element.getAttribute(consts.Consts.name) \
            if diagram_element.hasAttribute(consts.Consts.name) else ""

        plane_attributes[consts.Consts.id] = plane_element.getAttribute(consts.Consts.id)
        plane_attributes[consts.Consts.bpmn_element] = plane_element.getAttribute(consts.Consts.bpmn_element)

    @staticmethod
    def import_process_elements(document, diagram_graph, sequence_flows, process_elements_dict, plane_element):
        """
        Method for importing all 'process' elements in diagram.

        :param document: XML document,
        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows: a list of sequence flows existing in diagram,
        :param process_elements_dict: dictionary that holds attribute values for imported 'process' elements. Key is
            an ID of process, value - a dictionary of process attributes,
        :param plane_element: object representing a BPMN XML 'plane' element.
        """
        for process_element in document.getElementsByTagNameNS("*", consts.Consts.process):
            BpmnDiagramGraphImport.import_process_element(process_elements_dict, process_element)

            process_id = process_element.getAttribute(consts.Consts.id)
            process_attributes = process_elements_dict[process_id]

            lane_set_list = process_element.getElementsByTagNameNS("*", consts.Consts.lane_set)
            if lane_set_list is not None and len(lane_set_list) > 0:
                # according to BPMN 2.0 XML Schema, there's at most one 'laneSet' element inside 'process'
                lane_set = lane_set_list[0]
                BpmnDiagramGraphImport.import_lane_set_element(process_attributes, lane_set, plane_element)

            for element in utils.BpmnImportUtils.iterate_elements(process_element):
                if element.nodeType != element.TEXT_NODE:
                    tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                    BpmnDiagramGraphImport.__import_element_by_tag_name(diagram_graph, sequence_flows, process_id,
                                                                        process_attributes, element, tag_name)

            for flow in utils.BpmnImportUtils.iterate_elements(process_element):
                if flow.nodeType != flow.TEXT_NODE:
                    tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(flow.tagName)
                    if tag_name == consts.Consts.sequence_flow:
                        BpmnDiagramGraphImport.import_sequence_flow_to_graph(diagram_graph, sequence_flows, process_id,
                                                                             flow)

    @staticmethod
    def __import_element_by_tag_name(diagram_graph, sequence_flows, process_id, process_attributes, element, tag_name):
        if tag_name == consts.Consts.task \
                or tag_name == consts.Consts.user_task \
                or tag_name == consts.Consts.service_task \
                or tag_name == consts.Consts.manual_task:
            BpmnDiagramGraphImport.import_task_to_graph(diagram_graph, process_id, process_attributes, element)
        elif tag_name == consts.Consts.subprocess:
            BpmnDiagramGraphImport.import_subprocess_to_graph(diagram_graph, sequence_flows, process_id,
                                                              process_attributes, element)
        elif tag_name == consts.Consts.data_object:
            BpmnDiagramGraphImport.import_data_object_to_graph(diagram_graph, process_id, process_attributes, element)
        elif tag_name == consts.Consts.inclusive_gateway or tag_name == consts.Consts.exclusive_gateway:
            BpmnDiagramGraphImport.import_incl_or_excl_gateway_to_graph(diagram_graph, process_id, process_attributes,
                                                                        element)
        elif tag_name == consts.Consts.parallel_gateway:
            BpmnDiagramGraphImport.import_parallel_gateway_to_graph(diagram_graph, process_id, process_attributes,
                                                                    element)
        elif tag_name == consts.Consts.event_based_gateway:
            BpmnDiagramGraphImport.import_event_based_gateway_to_graph(diagram_graph, process_id, process_attributes,
                                                                       element)
        elif tag_name == consts.Consts.complex_gateway:
            BpmnDiagramGraphImport.import_complex_gateway_to_graph(diagram_graph, process_id, process_attributes,
                                                                   element)
        elif tag_name == consts.Consts.start_event:
            BpmnDiagramGraphImport.import_start_event_to_graph(diagram_graph, process_id, process_attributes, element)
        elif tag_name == consts.Consts.end_event:
            BpmnDiagramGraphImport.import_end_event_to_graph(diagram_graph, process_id, process_attributes, element)
        elif tag_name == consts.Consts.intermediate_catch_event:
            BpmnDiagramGraphImport.import_intermediate_catch_event_to_graph(diagram_graph, process_id,
                                                                            process_attributes, element)
        elif tag_name == consts.Consts.intermediate_throw_event:
            BpmnDiagramGraphImport.import_intermediate_throw_event_to_graph(diagram_graph, process_id,
                                                                            process_attributes, element)
        elif tag_name == consts.Consts.boundary_event:
            BpmnDiagramGraphImport.import_boundary_event_to_graph(diagram_graph, process_id, process_attributes,
                                                                  element)

    @staticmethod
    def import_lane_set_element(process_attributes, lane_set_element, plane_element):
        """
        Method for importing 'laneSet' element from diagram file.

        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param lane_set_element: XML document element,
        :param plane_element: object representing a BPMN XML 'plane' element.
        """
        lane_set_id = lane_set_element.getAttribute(consts.Consts.id)
        lanes_attr = {}
        for element in utils.BpmnImportUtils.iterate_elements(lane_set_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                if tag_name == consts.Consts.lane:
                    lane = element
                    lane_id = lane.getAttribute(consts.Consts.id)
                    lane_attr = BpmnDiagramGraphImport.import_lane_element(lane, plane_element)
                    lanes_attr[lane_id] = lane_attr

        lane_set_attr = {consts.Consts.id: lane_set_id, consts.Consts.lanes: lanes_attr}
        process_attributes[consts.Consts.lane_set] = lane_set_attr

    @staticmethod
    def import_child_lane_set_element(child_lane_set_element, plane_element):
        """
        Method for importing 'childLaneSet' element from diagram file.

        :param child_lane_set_element: XML document element,
        :param plane_element: object representing a BPMN XML 'plane' element.
        """
        lane_set_id = child_lane_set_element.getAttribute(consts.Consts.id)
        lanes_attr = {}
        for element in utils.BpmnImportUtils.iterate_elements(child_lane_set_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                if tag_name == consts.Consts.lane:
                    lane = element
                    lane_id = lane.getAttribute(consts.Consts.id)
                    lane_attr = BpmnDiagramGraphImport.import_lane_element(lane, plane_element)
                    lanes_attr[lane_id] = lane_attr

        child_lane_set_attr = {consts.Consts.id: lane_set_id, consts.Consts.lanes: lanes_attr}
        return child_lane_set_attr

    @staticmethod
    def import_lane_element(lane_element, plane_element):
        """
        Method for importing 'laneSet' element from diagram file.

        :param lane_element: XML document element,
        :param plane_element: object representing a BPMN XML 'plane' element.
        """
        lane_id = lane_element.getAttribute(consts.Consts.id)
        lane_name = lane_element.getAttribute(consts.Consts.name)
        child_lane_set_attr = {}
        flow_node_refs = []
        for element in utils.BpmnImportUtils.iterate_elements(lane_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                if tag_name == consts.Consts.child_lane_set:
                    child_lane_set_attr = BpmnDiagramGraphImport.import_child_lane_set_element(element, plane_element)
                elif tag_name == consts.Consts.flow_node_ref:
                    flow_node_ref_id = element.firstChild.nodeValue
                    flow_node_refs.append(flow_node_ref_id)

        lane_attr = {consts.Consts.id: lane_id, consts.Consts.name: lane_name,
                     consts.Consts.child_lane_set: child_lane_set_attr,
                     consts.Consts.flow_node_refs: flow_node_refs}

        shape_element = None
        for element in utils.BpmnImportUtils.iterate_elements(plane_element):
            if element.nodeType != element.TEXT_NODE and element.getAttribute(consts.Consts.bpmn_element) == lane_id:
                shape_element = element
        if shape_element is not None:
            bounds = shape_element.getElementsByTagNameNS("*", "Bounds")[0]
            lane_attr[consts.Consts.is_horizontal] = shape_element.getAttribute(consts.Consts.is_horizontal)
            lane_attr[consts.Consts.width] = bounds.getAttribute(consts.Consts.width)
            lane_attr[consts.Consts.height] = bounds.getAttribute(consts.Consts.height)
            lane_attr[consts.Consts.x] = bounds.getAttribute(consts.Consts.x)
            lane_attr[consts.Consts.y] = bounds.getAttribute(consts.Consts.y)
        return lane_attr

    @staticmethod
    def import_process_element(process_elements_dict, process_element):
        """
        Adds attributes of BPMN process element to appropriate field process_attributes.
        Diagram inner representation contains following process attributes:

        - id - assumed to be required in XML file, even thought BPMN 2.0 schema doesn't say so,
        - isClosed - optional parameter, default value 'false',
        - isExecutable - optional parameter, default value 'false',
        - processType - optional parameter, default value 'None',
        - node_ids - list of flow nodes IDs, associated with given process.

        :param process_elements_dict: dictionary that holds attribute values for imported 'process' element. Key is
           process ID, value is a dictionary of attributes,
        :param process_element: object representing a BPMN XML 'process' element.
        """
        process_id = process_element.getAttribute(consts.Consts.id)
        process_element_attributes = {consts.Consts.id: process_element.getAttribute(consts.Consts.id),
                                      consts.Consts.name: process_element.getAttribute(consts.Consts.name)
                                      if process_element.hasAttribute(consts.Consts.name) else "",
                                      consts.Consts.is_closed: process_element.getAttribute(consts.Consts.is_closed)
                                      if process_element.hasAttribute(consts.Consts.is_closed) else "false",
                                      consts.Consts.is_executable: process_element.getAttribute(
                                          consts.Consts.is_executable)
                                      if process_element.hasAttribute(consts.Consts.is_executable) else "false",
                                      consts.Consts.process_type: process_element.getAttribute(
                                          consts.Consts.process_type)
                                      if process_element.hasAttribute(consts.Consts.process_type) else "None",
                                      consts.Consts.node_ids: []}
        process_elements_dict[process_id] = process_element_attributes

    @staticmethod
    def import_flow_node_to_graph(bpmn_graph, process_id, process_attributes, flow_node_element):
        """
        Adds a new node to graph.
        Input parameter is object of class xml.dom.Element.
        Nodes are identified by ID attribute of Element.
        Method adds basic attributes (shared by all BPMN elements) to node. Those elements are:

        - id - added as key value, we assume that this is a required value,
        - type - tagName of element, used to identify type of BPMN diagram element,
        - name - optional attribute, empty string by default.

        :param bpmn_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param flow_node_element: object representing a BPMN XML element corresponding to given flownode,
        """
        element_id = flow_node_element.getAttribute(consts.Consts.id)
        bpmn_graph.add_node(element_id)
        bpmn_graph.node[element_id][consts.Consts.id] = element_id
        bpmn_graph.node[element_id][consts.Consts.type] = \
            utils.BpmnImportUtils.remove_namespace_from_tag_name(flow_node_element.tagName)
        bpmn_graph.node[element_id][consts.Consts.node_name] = \
            flow_node_element.getAttribute(consts.Consts.name) \
                if flow_node_element.hasAttribute(consts.Consts.name) \
                else ""
        bpmn_graph.node[element_id][consts.Consts.process] = process_id
        process_attributes[consts.Consts.node_ids].append(element_id)

        # add incoming flow node list
        incoming_list = []
        for tmp_element in utils.BpmnImportUtils.iterate_elements(flow_node_element):
            if tmp_element.nodeType != tmp_element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(tmp_element.tagName)
                if tag_name == consts.Consts.incoming_flow:
                    incoming_value = tmp_element.firstChild.nodeValue
                    incoming_list.append(incoming_value)
        bpmn_graph.node[element_id][consts.Consts.incoming_flow] = incoming_list

        # add outgoing flow node list
        outgoing_list = []
        for tmp_element in utils.BpmnImportUtils.iterate_elements(flow_node_element):
            if tmp_element.nodeType != tmp_element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(tmp_element.tagName)
                if tag_name == consts.Consts.outgoing_flow:
                    outgoing_value = tmp_element.firstChild.nodeValue
                    outgoing_list.append(outgoing_value)
        bpmn_graph.node[element_id][consts.Consts.outgoing_flow] = outgoing_list

    @staticmethod
    def import_task_to_graph(diagram_graph, process_id, process_attributes, task_element):
        """
        Adds to graph the new element that represents BPMN task.
        In our representation tasks have only basic attributes and elements, inherited from Activity type,
        so this method only needs to call add_flownode_to_graph.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param task_element: object representing a BPMN XML 'task' element.
        """
        BpmnDiagramGraphImport.import_activity_to_graph(diagram_graph, process_id, process_attributes, task_element)

    @staticmethod
    def import_subprocess_to_graph(diagram_graph, sequence_flows, process_id, process_attributes, subprocess_element):
        """
        Adds to graph the new element that represents BPMN subprocess.
        In addition to attributes inherited from FlowNode type, SubProcess
        has additional attribute tiggeredByEvent (boolean type, default value - false).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows: a list of sequence flows existing in diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
           imported flow node,
        :param subprocess_element: object representing a BPMN XML 'subprocess' element
        """
        BpmnDiagramGraphImport.import_activity_to_graph(diagram_graph, process_id, process_attributes,
                                                        subprocess_element)

        subprocess_id = subprocess_element.getAttribute(consts.Consts.id)
        diagram_graph.node[subprocess_id][consts.Consts.triggered_by_event] = \
            subprocess_element.getAttribute(consts.Consts.triggered_by_event) \
                if subprocess_element.hasAttribute(consts.Consts.triggered_by_event) else "false"

        subprocess_attributes = diagram_graph.node[subprocess_id]
        subprocess_attributes[consts.Consts.node_ids] = []
        for element in utils.BpmnImportUtils.iterate_elements(subprocess_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                BpmnDiagramGraphImport.__import_element_by_tag_name(diagram_graph, sequence_flows, subprocess_id,
                                                                    subprocess_attributes, element, tag_name)

        for flow in utils.BpmnImportUtils.iterate_elements(subprocess_element):
            if flow.nodeType != flow.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(flow.tagName)
                if tag_name == consts.Consts.sequence_flow:
                    BpmnDiagramGraphImport.import_sequence_flow_to_graph(diagram_graph, sequence_flows, subprocess_id,
                                                                         flow)

    @staticmethod
    def import_data_object_to_graph(diagram_graph, process_id, process_attributes, data_object_element):
        """
        Adds to graph the new element that represents BPMN data object.
        Data object inherits attributes from FlowNode. In addition, an attribute 'isCollection' is added to the node.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param data_object_element: object representing a BPMN XML 'dataObject' element.
        """
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes,
                                                         data_object_element)
        data_object_id = data_object_element.getAttribute(consts.Consts.id)
        diagram_graph.node[data_object_id][consts.Consts.is_collection] = \
            data_object_element.getAttribute(consts.Consts.is_collection) \
                if data_object_element.hasAttribute(consts.Consts.is_collection) else "false"

    @staticmethod
    def import_activity_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Method that adds the new element that represents BPMN activity.
        Should not be used directly, only as a part of method, that imports an element which extends Activity element
        (task, subprocess etc.)

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
           imported flow node,
        :param element: object representing a BPMN XML element which extends 'activity'.
        """
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes, element)

        element_id = element.getAttribute(consts.Consts.id)
        diagram_graph.node[element_id][consts.Consts.default] = element.getAttribute(consts.Consts.default) \
            if element.hasAttribute(consts.Consts.default) else None

    @staticmethod
    def import_gateway_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN gateway.
        In addition to attributes inherited from FlowNode type, Gateway
        has additional attribute gatewayDirection (simple type, default value - Unspecified).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param element: object representing a BPMN XML element of Gateway type extension.
        """
        element_id = element.getAttribute(consts.Consts.id)
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes, element)
        diagram_graph.node[element_id][consts.Consts.gateway_direction] = \
            element.getAttribute(consts.Consts.gateway_direction) \
                if element.hasAttribute(consts.Consts.gateway_direction) else "Unspecified"

    @staticmethod
    def import_complex_gateway_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN complex gateway.
        In addition to attributes inherited from Gateway type, complex gateway
        has additional attribute default flow (default value - none).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param element: object representing a BPMN XML 'complexGateway' element.
        """
        element_id = element.getAttribute(consts.Consts.id)
        BpmnDiagramGraphImport.import_gateway_to_graph(diagram_graph, process_id, process_attributes, element)
        diagram_graph.node[element_id][consts.Consts.default] = element.getAttribute(consts.Consts.default) \
            if element.hasAttribute(consts.Consts.default) else None
        # TODO sequence of conditions
        # Can't get any working example of Complex gateway, so I'm not sure how exactly those conditions are kept

    @staticmethod
    def import_event_based_gateway_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN event based gateway.
        In addition to attributes inherited from Gateway type, event based gateway has additional
        attributes - instantiate (boolean type, default value - false) and eventGatewayType
        (custom type tEventBasedGatewayType, default value - Exclusive).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
           imported flow node,
        :param element: object representing a BPMN XML 'eventBasedGateway' element.
        """
        element_id = element.getAttribute(consts.Consts.id)
        BpmnDiagramGraphImport.import_gateway_to_graph(diagram_graph, process_id, process_attributes, element)
        diagram_graph.node[element_id][consts.Consts.instantiate] = element.getAttribute(consts.Consts.instantiate) \
            if element.hasAttribute(consts.Consts.instantiate) else "false"
        diagram_graph.node[element_id][consts.Consts.event_gateway_type] = \
            element.getAttribute(consts.Consts.event_gateway_type) \
                if element.hasAttribute(consts.Consts.event_gateway_type) else "Exclusive"

    @staticmethod
    def import_incl_or_excl_gateway_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN inclusive or eclusive gateway.
        In addition to attributes inherited from Gateway type, inclusive and exclusive gateway have additional
        attribute default flow (default value - none).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param element: object representing a BPMN XML 'inclusiveGateway' or 'exclusiveGateway' element.
        """
        element_id = element.getAttribute(consts.Consts.id)
        BpmnDiagramGraphImport.import_gateway_to_graph(diagram_graph, process_id, process_attributes, element)
        diagram_graph.node[element_id][consts.Consts.default] = element.getAttribute(consts.Consts.default) \
            if element.hasAttribute(consts.Consts.default) else None

    @staticmethod
    def import_parallel_gateway_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN parallel gateway.
        Parallel gateway doesn't have additional attributes. Separate method is used to improve code readability.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param element: object representing a BPMN XML 'parallelGateway'.
        """
        BpmnDiagramGraphImport.import_gateway_to_graph(diagram_graph, process_id, process_attributes, element)

    @staticmethod
    def import_event_definition_elements(diagram_graph, element, event_definitions):
        """
        Helper function, that adds event definition elements (defines special types of events) to corresponding events.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param element: object representing a BPMN XML event element,
        :param event_definitions: list of event definitions, that belongs to given event.
        """
        element_id = element.getAttribute(consts.Consts.id)
        event_def_list = []
        for definition_type in event_definitions:
            event_def_xml = element.getElementsByTagNameNS("*", definition_type)
            for index in range(len(event_def_xml)):
                # tuple - definition type, definition id
                event_def_tmp = {consts.Consts.id: event_def_xml[index].getAttribute(consts.Consts.id),
                                 consts.Consts.definition_type: definition_type}
                event_def_list.append(event_def_tmp)
        diagram_graph.node[element_id][consts.Consts.event_definitions] = event_def_list

    @staticmethod
    def import_start_event_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN start event.
        Start event inherits attribute parallelMultiple from CatchEvent type
        and sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
           imported flow node,
        :param element: object representing a BPMN XML 'startEvent' element.
        """
        element_id = element.getAttribute(consts.Consts.id)
        start_event_definitions = {'messageEventDefinition', 'timerEventDefinition', 'conditionalEventDefinition',
                                   'escalationEventDefinition', 'signalEventDefinition'}
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes, element)
        diagram_graph.node[element_id][consts.Consts.parallel_multiple] = \
            element.getAttribute(consts.Consts.parallel_multiple) \
                if element.hasAttribute(consts.Consts.parallel_multiple) else "false"
        diagram_graph.node[element_id][consts.Consts.is_interrupting] = \
            element.getAttribute(consts.Consts.is_interrupting) \
                if element.hasAttribute(consts.Consts.is_interrupting) else "true"
        BpmnDiagramGraphImport.import_event_definition_elements(diagram_graph, element, start_event_definitions)

    @staticmethod
    def import_intermediate_catch_event_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN intermediate catch event.
        Intermediate catch event inherits attribute parallelMultiple from CatchEvent type
        and sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param element: object representing a BPMN XML 'intermediateCatchEvent' element.
        """
        element_id = element.getAttribute(consts.Consts.id)
        intermediate_catch_event_definitions = {'messageEventDefinition', 'timerEventDefinition',
                                                'signalEventDefinition', 'conditionalEventDefinition',
                                                'escalationEventDefinition'}
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes, element)
        diagram_graph.node[element_id][consts.Consts.parallel_multiple] = \
            element.getAttribute(consts.Consts.parallel_multiple) \
                if element.hasAttribute(consts.Consts.parallel_multiple) else "false"
        BpmnDiagramGraphImport.import_event_definition_elements(diagram_graph, element,
                                                                intermediate_catch_event_definitions)

    @staticmethod
    def import_end_event_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN end event.
        End event inherits sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param element: object representing a BPMN XML 'endEvent' element.
        """
        end_event_definitions = {'messageEventDefinition', 'signalEventDefinition', 'escalationEventDefinition',
                                 'errorEventDefinition', 'compensateEventDefinition', 'terminateEventDefinition'}
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes, element)
        BpmnDiagramGraphImport.import_event_definition_elements(diagram_graph, element, end_event_definitions)

    @staticmethod
    def import_intermediate_throw_event_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN intermediate throw event.
        Intermediate throw event inherits sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
           imported flow node,
        :param element: object representing a BPMN XML 'intermediateThrowEvent' element.
        """
        intermediate_throw_event_definitions = {'messageEventDefinition', 'signalEventDefinition',
                                                'escalationEventDefinition', 'compensateEventDefinition'}
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes, element)
        BpmnDiagramGraphImport.import_event_definition_elements(diagram_graph, element,
                                                                intermediate_throw_event_definitions)

    @staticmethod
    def import_boundary_event_to_graph(diagram_graph, process_id, process_attributes, element):
        """
        Adds to graph the new element that represents BPMN boundary event.
        Boundary event inherits sequence of eventDefinitionRef from Event type.
        Separate methods for each event type are required since each of them has different variants
        (Message, Error, Signal etc.).

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param process_id: string object, representing an ID of process element,
        :param process_attributes: dictionary that holds attribute values of 'process' element, which is parent of
            imported flow node,
        :param element: object representing a BPMN XML 'endEvent' element.
        """
        element_id = element.getAttribute(consts.Consts.id)
        boundary_event_definitions = {'messageEventDefinition', 'timerEventDefinition', 'signalEventDefinition',
                                      'conditionalEventDefinition', 'escalationEventDefinition', 'errorEventDefinition'}
        BpmnDiagramGraphImport.import_flow_node_to_graph(diagram_graph, process_id, process_attributes, element)

        diagram_graph.node[element_id][consts.Consts.parallel_multiple] = \
            element.getAttribute(consts.Consts.parallel_multiple) \
                if element.hasAttribute(consts.Consts.parallel_multiple) else "false"
        diagram_graph.node[element_id][consts.Consts.cancel_activity] = \
            element.getAttribute(consts.Consts.cancel_activity) \
                if element.hasAttribute(consts.Consts.cancel_activity) else "true"
        diagram_graph.node[element_id][consts.Consts.attached_to_ref] = \
            element.getAttribute(consts.Consts.attached_to_ref)

        BpmnDiagramGraphImport.import_event_definition_elements(diagram_graph, element,
                                                                boundary_event_definitions)

    @staticmethod
    def import_sequence_flow_to_graph(diagram_graph, sequence_flows, process_id, flow_element):
        """
        Adds a new edge to graph and a record to sequence_flows dictionary.
        Input parameter is object of class xml.dom.Element.
        Edges are identified by pair of sourceRef and targetRef attributes of BPMNFlow element. We also
        provide a dictionary, that maps sequenceFlow ID attribute with its sourceRef and targetRef.
        Method adds basic attributes of sequenceFlow element to edge. Those elements are:

        - id - added as edge attribute, we assume that this is a required value,
        - name - optional attribute, empty string by default.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows: dictionary (associative list) of sequence flows existing in diagram.
            Key attribute is sequenceFlow ID, value is a dictionary consisting three key-value pairs: "name" (sequence
            flow name), "sourceRef" (ID of node, that is a flow source) and "targetRef" (ID of node, that is a flow target),
        :param process_id: string object, representing an ID of process element,
        :param flow_element: object representing a BPMN XML 'sequenceFlow' element.
        """
        flow_id = flow_element.getAttribute(consts.Consts.id)
        name = flow_element.getAttribute(consts.Consts.name) if flow_element.hasAttribute(consts.Consts.name) else ""
        source_ref = flow_element.getAttribute(consts.Consts.source_ref)
        target_ref = flow_element.getAttribute(consts.Consts.target_ref)
        sequence_flows[flow_id] = {consts.Consts.name: name, consts.Consts.source_ref: source_ref,
                                   consts.Consts.target_ref: target_ref}
        diagram_graph.add_edge(source_ref, target_ref)
        diagram_graph[source_ref][target_ref][consts.Consts.id] = flow_id
        diagram_graph[source_ref][target_ref][consts.Consts.process] = process_id
        diagram_graph[source_ref][target_ref][consts.Consts.name] = name
        diagram_graph[source_ref][target_ref][consts.Consts.source_ref] = source_ref
        diagram_graph[source_ref][target_ref][consts.Consts.target_ref] = target_ref
        for element in utils.BpmnImportUtils.iterate_elements(flow_element):
            if element.nodeType != element.TEXT_NODE:
                tag_name = utils.BpmnImportUtils.remove_namespace_from_tag_name(element.tagName)
                if tag_name == consts.Consts.condition_expression:
                    condition_expression = element.firstChild.nodeValue
                    diagram_graph[source_ref][target_ref][consts.Consts.condition_expression] = {
                        consts.Consts.id: element.getAttribute(consts.Consts.id),
                        consts.Consts.condition_expression: condition_expression
                    }

        '''
        # Add incoming / outgoing nodes to corresponding elements. May be redundant action since this information is
        added when processing nodes, but listing incoming / outgoing nodes under node element is optional - this way
        we can make sure this info will be imported.
        '''
        if consts.Consts.outgoing_flow not in diagram_graph.node[source_ref]:
            diagram_graph.node[source_ref][consts.Consts.outgoing_flow] = []
        outgoing_list = diagram_graph.node[source_ref][consts.Consts.outgoing_flow]
        if flow_id not in outgoing_list:
            outgoing_list.append(flow_id)

        if consts.Consts.incoming_flow not in diagram_graph.node[target_ref]:
            diagram_graph.node[target_ref][consts.Consts.incoming_flow] = []
        incoming_list = diagram_graph.node[target_ref][consts.Consts.incoming_flow]
        if flow_id not in incoming_list:
            incoming_list.append(flow_id)

    @staticmethod
    def import_message_flow_to_graph(diagram_graph, message_flows, flow_element):
        """
        Adds a new edge to graph and a record to message flows dictionary.
        Input parameter is object of class xml.dom.Element.
        Edges are identified by pair of sourceRef and targetRef attributes of BPMNFlow element. We also
        provide a dictionary, that maps messageFlow ID attribute with its sourceRef and targetRef.
        Method adds basic attributes of messageFlow element to edge. Those elements are:

        - id - added as edge attribute, we assume that this is a required value,
        - name - optional attribute, empty string by default.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param message_flows: dictionary (associative list) of message flows existing in diagram.
            Key attribute is messageFlow ID, value is a dictionary consisting three key-value pairs: "name" (message
            flow name), "sourceRef" (ID of node, that is a flow source) and "targetRef" (ID of node, that is a flow target),
        :param flow_element: object representing a BPMN XML 'messageFlow' element.
        """
        flow_id = flow_element.getAttribute(consts.Consts.id)
        name = flow_element.getAttribute(consts.Consts.name) if flow_element.hasAttribute(consts.Consts.name) else ""
        source_ref = flow_element.getAttribute(consts.Consts.source_ref)
        target_ref = flow_element.getAttribute(consts.Consts.target_ref)
        message_flows[flow_id] = {consts.Consts.id: flow_id, consts.Consts.name: name,
                                  consts.Consts.source_ref: source_ref,
                                  consts.Consts.target_ref: target_ref}
        diagram_graph.add_edge(source_ref, target_ref)
        diagram_graph[source_ref][target_ref][consts.Consts.id] = flow_id
        diagram_graph[source_ref][target_ref][consts.Consts.name] = name
        diagram_graph[source_ref][target_ref][consts.Consts.source_ref] = source_ref
        diagram_graph[source_ref][target_ref][consts.Consts.target_ref] = target_ref

        '''
        # Add incoming / outgoing nodes to corresponding elements. May be redundant action since this information is
        added when processing nodes, but listing incoming / outgoing nodes under node element is optional - this way
        we can make sure this info will be imported.
        '''
        if consts.Consts.outgoing_flow not in diagram_graph.node[source_ref]:
            diagram_graph.node[source_ref][consts.Consts.outgoing_flow] = []
        outgoing_list = diagram_graph.node[source_ref][consts.Consts.outgoing_flow]
        if flow_id not in outgoing_list:
            outgoing_list.append(flow_id)

        if consts.Consts.incoming_flow not in diagram_graph.node[target_ref]:
            diagram_graph.node[target_ref][consts.Consts.incoming_flow] = []
        incoming_list = diagram_graph.node[target_ref][consts.Consts.incoming_flow]
        if flow_id not in incoming_list:
            incoming_list.append(flow_id)

    @staticmethod
    def import_shape_di(participants_dict, diagram_graph, shape_element):
        """
        Adds Diagram Interchange information (information about rendering a diagram) to appropriate
        BPMN diagram element in graph node.
        We assume that those attributes are required for each BPMNShape:

        - width - width of BPMNShape,
        - height - height of BPMNShape,
        - x - first coordinate of BPMNShape,
        - y - second coordinate of BPMNShape.

        :param participants_dict: dictionary with 'participant' elements attributes,
        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param shape_element: object representing a BPMN XML 'BPMNShape' element.
        """
        element_id = shape_element.getAttribute(consts.Consts.bpmn_element)
        bounds = shape_element.getElementsByTagNameNS("*", "Bounds")[0]
        if diagram_graph.has_node(element_id):
            node = diagram_graph.node[element_id]
            node[consts.Consts.width] = bounds.getAttribute(consts.Consts.width)
            node[consts.Consts.height] = bounds.getAttribute(consts.Consts.height)

            if node[consts.Consts.type] == consts.Consts.subprocess:
                node[consts.Consts.is_expanded] = \
                    shape_element.getAttribute(consts.Consts.is_expanded) \
                        if shape_element.hasAttribute(consts.Consts.is_expanded) else "false"
            node[consts.Consts.x] = bounds.getAttribute(consts.Consts.x)
            node[consts.Consts.y] = bounds.getAttribute(consts.Consts.y)
        if element_id in participants_dict:
            # BPMNShape is either connected with FlowNode or Participant
            participant_attr = participants_dict[element_id]
            participant_attr[consts.Consts.is_horizontal] = shape_element.getAttribute(consts.Consts.is_horizontal)
            participant_attr[consts.Consts.width] = bounds.getAttribute(consts.Consts.width)
            participant_attr[consts.Consts.height] = bounds.getAttribute(consts.Consts.height)
            participant_attr[consts.Consts.x] = bounds.getAttribute(consts.Consts.x)
            participant_attr[consts.Consts.y] = bounds.getAttribute(consts.Consts.y)

    @staticmethod
    def import_flow_di(diagram_graph, sequence_flows, message_flows, flow_element):
        """
        Adds Diagram Interchange information (information about rendering a diagram) to appropriate
        BPMN sequence flow represented as graph edge.
        We assume that each BPMNEdge has a list of 'waypoint' elements. BPMN 2.0 XML Schema states,
        that each BPMNEdge must have at least two waypoints.

        :param diagram_graph: NetworkX graph representing a BPMN process diagram,
        :param sequence_flows: dictionary (associative list) of sequence flows existing in diagram.
            Key attribute is sequenceFlow ID, value is a dictionary consisting three key-value pairs: "name" (sequence
            flow name), "sourceRef" (ID of node, that is a flow source) and "targetRef" (ID of node, that is a flow target),
        :param message_flows: dictionary (associative list) of message flows existing in diagram.
            Key attribute is messageFlow ID, value is a dictionary consisting three key-value pairs: "name" (message
            flow name), "sourceRef" (ID of node, that is a flow source) and "targetRef" (ID of node, that is a flow target),
        :param flow_element: object representing a BPMN XML 'BPMNEdge' element.
        """
        flow_id = flow_element.getAttribute(consts.Consts.bpmn_element)
        waypoints_xml = flow_element.getElementsByTagNameNS("*", consts.Consts.waypoint)
        length = len(waypoints_xml)

        waypoints = [None] * length
        for index in range(length):
            waypoint_tmp = (waypoints_xml[index].getAttribute(consts.Consts.x),
                            waypoints_xml[index].getAttribute(consts.Consts.y))
            waypoints[index] = waypoint_tmp

        flow_data = None
        if flow_id in sequence_flows:
            flow_data = sequence_flows[flow_id]
        elif flow_id in message_flows:
            flow_data = message_flows[flow_id]

        if flow_data is not None:
            name = flow_data[consts.Consts.name]
            source_ref = flow_data[consts.Consts.source_ref]
            target_ref = flow_data[consts.Consts.target_ref]
            diagram_graph[source_ref][target_ref][consts.Consts.waypoints] = waypoints
            diagram_graph[source_ref][target_ref][consts.Consts.name] = name

    @staticmethod
    def read_xml_file(filepath):
        """
        Reads BPMN 2.0 XML file from given filepath and returns xml.dom.xminidom.Document object.

        :param filepath: filepath of source XML file.
        """
        dom_tree = minidom.parse(filepath)
        return dom_tree
