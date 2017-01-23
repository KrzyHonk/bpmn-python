# coding=utf-8
"""
Package with BPMNDiagramGraph - graph representation of BPMN diagram
"""
import uuid

import networkx as nx

import bpmn_diagram_exception as bpmn_exception
import bpmn_python.bpmn_diagram_export as bpmn_export
import bpmn_python.bpmn_diagram_import as bpmn_import
import bpmn_python.bpmn_process_csv_export as bpmn_csv_export


class BpmnDiagramGraph:
    """
    Class BPMNDiagramGraph implements simple inner representation of BPMN 2.0 diagram,
    based on NetworkX graph implementation

    Fields:
    - diagram_graph - networkx.Graph object, stores elements of BPMN diagram as nodes. Each edge of graph represents
    sequenceFlow element. Edges are identified by IDs of nodes connected by edge. IDs are passed as edge parameters,
    - sequence_flows - dictionary (associative list) of sequence flows existing in diagram.
    Key attribute is sequenceFlow ID, value is a dictionary consisting three key-value pairs: "name" (sequence flow
    name), "sourceRef" (ID of node, that is a flow source) and "targetRef" (ID of node, that is a flow target),
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

    def load_diagram_from_xml(self, filepath):
        """
        Reads an XML file from given filepath and maps it into inner representation of BPMN diagram.
        Returns an instance of BPMNDiagramGraph class.

        :param filepath: string with output filepath.
        """

        bpmn_import.BpmnDiagramGraphImport.load_diagram_from_xml(filepath, self.diagram_graph,
                                                                 self.sequence_flows, self.process_attributes,
                                                                 self.diagram_attributes, self.plane_attributes)

    def export_xml_file(self, directory, filename):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (with Diagram Interchange data).

        :param directory: strings representing output directory,
        :param filename: string representing output file name.
        """
        bpmn_export.BpmnDiagramGraphExport.export_xml_file(directory, filename, self, self.process_attributes,
                                                           self.diagram_attributes, self.plane_attributes)

    def export_xml_file_no_di(self, directory, filename):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (without Diagram Interchange data).

        :param directory: strings representing output directory,
        :param filename: string representing output file name.
        """
        bpmn_export.BpmnDiagramGraphExport.export_xml_file_no_di(directory, filename, self.diagram_graph,
                                                                 self.process_attributes)

    def export_csv_file(self, directory, filename):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (with Diagram Interchange data).

        :param directory: strings representing output directory,
        :param filename: string representing output file name.
        """
        bpmn_csv_export.BpmnDiagramGraphCsvExport.export_process_to_csv(self, directory, filename)

    # Querying methods
    def get_nodes(self, node_type=""):
        """
        Gets all nodes of requested type. If no type is provided by user, all nodes in BPMN diagram graph are returned.
        Returns a dictionary, where key is an ID of node, value is a dictionary of all node attributes.

        :param node_type: string with valid BPMN XML tag name (e.g. 'task', 'sequenceFlow').
        """
        tmp_nodes = self.diagram_graph.nodes(True)
        if node_type == "":
            return tmp_nodes
        else:
            nodes = []
            for node in tmp_nodes:
                if node[1]["type"] == node_type:
                    nodes.append(node)
            return nodes

    def get_node_by_id(self, node_id):
        """
        Gets a node with requested ID.
        Returns a tuple, where first value is node ID, second - a dictionary of all node attributes.

        :param node_id: string with ID of node.
        """
        tmp_nodes = self.diagram_graph.nodes(data=True)
        for node in tmp_nodes:
            if node[0] == node_id:
                return node

    def get_nodes_id_list_by_type(self, node_type):
        """
        Get a list of node's id by requested type.
        Returns a list of ids

        :param node_type: string with valid BPMN XML tag name (e.g. 'task', 'sequenceFlow').
        """
        tmp_nodes = self.diagram_graph.nodes(data=True)
        id_list = []
        for node in tmp_nodes:
            if node[1]["type"] == node_type:
                id_list.append(node[0])
        return id_list

    def get_flows(self):
        """
        Gets all graph edges (process flows).
        Returns a two-dimensional dictionary, where keys are IDs of nodes connected by edge and
        values are a dictionary of all edge attributes.
        """
        return self.diagram_graph.edges(data=True)

    def get_flow_by_id(self, flow_id):
        """
        Gets an edge (flow) with requested ID.
        Returns a tuple, where first value is node ID, second - a dictionary of all node attributes.

        :param flow_id: string with edge ID.
        """
        tmp_flows = self.diagram_graph.edges(data=True)
        for flow in tmp_flows:
            if flow[2]["id"] == flow_id:
                return flow

    # Diagram creating methods
    def create_new_diagram_graph(self, process_is_closed=False, process_is_executable=False,
                                 process_type="None", diagram_name=""):
        """
        Initializes a new BPMN diagram and sets up a basic process, diagram and plane attributes.
        Accepts a user-defined values for following attributes:
        (Process element)
        - isClosed - default value false,
        - isExecutable - default value false,
        - processType - default value None.
        (Diagram element)
        - name - default value empty string.

        :param process_is_closed: boolean type. Represents a user-defined value of 'process' element
        attribute 'isClosed'. Default value false,
        :param process_is_executable: boolean type. Represents a user-defined value of 'process' element
        attribute 'isExecutable'. Default value false,
        :param process_type: string type. Represents a user-defined value of 'process' element
        attribute 'procesType'. Default value "None",
        :param diagram_name: string type. Represents a user-defined value of 'BPMNDiagram' element
        attribute 'name'. Default value - empty string.
        """
        self.__init__()
        process_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        diagram_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        plane_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
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

        :param node_type: string object. Represents type of BPMN node passed to method,
        :param node_id: string object. ID of given node,
        :param node_name: string object. Node name.
        """
        self.diagram_graph.add_node(node_id)
        self.diagram_graph.node[node_id]["type"] = node_type
        self.diagram_graph.node[node_id]["node_name"] = node_name
        self.diagram_graph.node[node_id]["incoming"] = []
        self.diagram_graph.node[node_id]["outgoing"] = []

        # Adding some dummy constant values
        self.diagram_graph.node[node_id]["width"] = "100"
        self.diagram_graph.node[node_id]["height"] = "100"
        self.diagram_graph.node[node_id]["x"] = "100"
        self.diagram_graph.node[node_id]["y"] = "100"
        return node_id, self.diagram_graph.node[node_id]

    def add_task_to_diagram(self, task_name=""):
        """
        Adds a Task element to BPMN diagram.
        User-defined attributes:
        - name
        Returns a tuple, where first value is task ID, second a reference to created object.

        :param task_name: string object. Name of task.
        """
        task_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("task", task_id, task_name)
        return task_id, self.diagram_graph.node[task_id]

    def add_subprocess_to_diagram(self, subprocess_name, is_expanded=False, triggered_by_event=False):
        """
        Adds a SubProcess element to BPMN diagram.
        User-defined attributes:
        - name
        - triggered_by_event
        Returns a tuple, where first value is subProcess ID, second a reference to created object.

        :param subprocess_name: string object. Name of subprocess,
        :param is_expanded: boolean value for attribute "isExpanded". Default value false,
        :param triggered_by_event: boolean value for attribute "triggeredByEvent". Default value false.
        """
        subprocess_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("subProcess", subprocess_id, subprocess_name)
        self.diagram_graph.node[subprocess_id]["isExpanded"] = "true" if is_expanded else "false"
        self.diagram_graph.node[subprocess_id]["triggeredByEvent"] = "true" if triggered_by_event else "false"
        return subprocess_id, self.diagram_graph.node[subprocess_id]

    def add_start_event_to_diagram(self, start_event_name="", start_event_definition=None, parallel_multiple=False,
                                   is_interrupting=True):
        """
        Adds a StartEvent element to BPMN diagram.
        User-defined attributes:
        - name
        - parallel_multiple
        - is_interrupting
        - event definition (creates a special type of start event). Supported event definitions -
        'message': 'messageEventDefinition', 'timer': 'timerEventDefinition', 'signal': 'signalEventDefinition',
        'conditional': 'conditionalEventDefinition', 'escalation': 'escalationEventDefinition'.

        :param start_event_name: string object. Name of start event,
        :param start_event_definition: list of event definitions. By default - empty,
        :param parallel_multiple: boolean value for attribute "parallelMultiple",
        :param is_interrupting: boolean value for attribute "isInterrupting.
        :return a tuple, where first value is startEvent ID, second a reference to created object.
        """
        start_event_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("startEvent", start_event_id, start_event_name)
        self.diagram_graph.node[start_event_id]["parallelMultiple"] = "true" if parallel_multiple else "false"
        self.diagram_graph.node[start_event_id]["isInterrupting"] = "true" if is_interrupting else "false"
        start_event_definitions = {"message": "messageEventDefinition", "timer": "timerEventDefinition",
                                   "conditional": "conditionalEventDefinition", "signal": "signalEventDefinition",
                                   "escalation": "escalationEventDefinition"}
        event_def_list = []
        if start_event_definition == "message":
            event_def_list.append(self.add_event_definition_element("message", start_event_definitions))
        elif start_event_definition == "timer":
            event_def_list.append(self.add_event_definition_element("timer", start_event_definitions))
        elif start_event_definition == "conditional":
            event_def_list.append(self.add_event_definition_element("conditional", start_event_definitions))
        elif start_event_definition == "signal":
            event_def_list.append(self.add_event_definition_element("signal", start_event_definitions))
        elif start_event_definition == "escalation":
            event_def_list.append(self.add_event_definition_element("escalation", start_event_definitions))

        self.diagram_graph.node[start_event_id]["event_definitions"] = event_def_list
        return start_event_id, self.diagram_graph.node[start_event_id]

    def add_end_event_to_diagram(self, end_event_name="", end_event_definition=None):
        """
        Adds an EndEvent element to BPMN diagram.
        User-defined attributes:
        - name
        - event definition (creates a special type of end event). Supported event definitions -
        'terminate': 'terminateEventDefinition', 'signal': 'signalEventDefinition', 'error': 'errorEventDefinition',
        'escalation': 'escalationEventDefinition', 'message': 'messageEventDefinition',
        'compensate': 'compensateEventDefinition'.

        :param end_event_name: string object. Name of end event,
        :param end_event_definition: list of event definitions. By default - empty.
        :return a tuple, where first value is endEvent ID, second a reference to created object.
        """
        end_event_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("endEvent", end_event_id, end_event_name)
        end_event_definitions = {"terminate": "terminateEventDefinition", "escalation": "escalationEventDefinition",
                                 "message": "messageEventDefinition", "compensate": "compensateEventDefinition",
                                 "signal": "signalEventDefinition", "error": "errorEventDefinition"}
        event_def_list = []
        if end_event_definition == "terminate":
            event_def_list.append(self.add_event_definition_element("terminate", end_event_definitions))
        elif end_event_definition == "escalation":
            event_def_list.append(self.add_event_definition_element("escalation", end_event_definitions))
        elif end_event_definition == "message":
            event_def_list.append(self.add_event_definition_element("message", end_event_definitions))
        elif end_event_definition == "compensate":
            event_def_list.append(self.add_event_definition_element("compensate", end_event_definitions))
        elif end_event_definition == "signal":
            event_def_list.append(self.add_event_definition_element("signal", end_event_definitions))
        elif end_event_definition == "error":
            event_def_list.append(self.add_event_definition_element("error", end_event_definitions))

        self.diagram_graph.node[end_event_id]["event_definitions"] = event_def_list
        return end_event_id, self.diagram_graph.node[end_event_id]

    def add_event_definition_element(self, event_type, event_definitions):
        """
        Helper function, that creates event definition element (special type of event) from given parameters.

        :param event_type: string object. Short name of required event definition,
        :param event_definitions: dictionary of event definitions. Key is a short name of event definition,
        value is a full name of event definition, as defined in BPMN 2.0 XML Schema.
        """
        event_def_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        event_def = (event_definitions[event_type], event_def_id)
        return event_def

    def add_exclusive_gateway_to_diagram(self, gateway_name="", gateway_direction="Unspecified", default=None):
        """
        Adds an exclusiveGateway element to BPMN diagram.
        User-defined attributes:
        - name
        - gatewayDirection
        - default
        Returns a tuple, where first value is exculusiveGateway ID, second a reference to created object.

        :param gateway_name: string object. Name of exclusive gateway,
        :param gateway_direction: string object. Accepted values - "Unspecified", "Converging", "Diverging", "Mixed".
        Default value - "Unspecified". If passed value is not one of the allowed values, it is changed to "Unspecified"
        :param default: string object. ID of flow node, target of gateway default path. Default value - None.
        """
        exclusive_gateway_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("exclusiveGateway", exclusive_gateway_id, gateway_name)
        if not (gateway_direction in ("Unspecified", "Converging", "Diverging", "Mixed")):
            raise bpmn_exception.BpmnPythonError("Invalid value passed as gatewayDirection parameter. Value passed: "
                                                 + gateway_direction)
        self.diagram_graph.node[exclusive_gateway_id]["gatewayDirection"] = gateway_direction
        self.diagram_graph.node[exclusive_gateway_id]["default"] = default
        return exclusive_gateway_id, self.diagram_graph.node[exclusive_gateway_id]

    def add_inclusive_gateway_to_diagram(self, gateway_name="", gateway_direction="Unspecified", default=None):
        """
        Adds an inclusiveGateway element to BPMN diagram.
        User-defined attributes:
        - name
        - gatewayDirection
        - default
        Returns a tuple, where first value is inclusiveGateway ID, second a reference to created object.

        :param gateway_name: string object. Name of inclusive gateway,
        :param gateway_direction: string object. Accepted values - "Unspecified", "Converging", "Diverging", "Mixed".
        Default value - "Unspecified",
        :param default: string object. ID of flow node, target of gateway default path. Default value - None.
        """
        inclusive_gateway_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("inclusiveGateway", inclusive_gateway_id, gateway_name)
        self.diagram_graph.node[inclusive_gateway_id]["gatewayDirection"] = gateway_direction
        self.diagram_graph.node[inclusive_gateway_id]["default"] = default
        return inclusive_gateway_id, self.diagram_graph.node[inclusive_gateway_id]

    def add_parallel_gateway_to_diagram(self, gateway_name="", gateway_direction="Unspecified"):
        """
        Adds an parallelGateway element to BPMN diagram.
        User-defined attributes:
        - name
        - gatewayDirection
        Returns a tuple, where first value is parallelGateway ID, second a reference to created object.

        :param gateway_name: string object. Name of inclusive gateway,
        :param gateway_direction: string object. Accepted values - "Unspecified", "Converging", "Diverging", "Mixed".
        Default value - "Unspecified".
        """
        parallel_gateway_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("parallelGateway", parallel_gateway_id, gateway_name)
        self.diagram_graph.node[parallel_gateway_id]["gatewayDirection"] = gateway_direction
        return parallel_gateway_id, self.diagram_graph.node[parallel_gateway_id]

    def add_sequence_flow_to_diagram(self, source_ref_id, target_ref_id, sequence_flow_name=""):
        """
        Adds a SequenceFlow element to BPMN diagram.
        Requires that user passes a sourceRef and targetRef as parameters.
        User-defined attributes:
        - name
        Returns a tuple, where first value is sequenceFlow ID, second a reference to created object.

        :param source_ref_id: string object. ID of source node,
        :param target_ref_id: string object. ID of target node,
        :param sequence_flow_name: string object. Name of sequence flow.
        """
        sequence_flow_id = BpmnDiagramGraph.id_prefix + str(uuid.uuid4())
        self.sequence_flows[sequence_flow_id] = {"name": sequence_flow_name, "sourceRef": source_ref_id,
                                                 "targetRef": target_ref_id}
        self.diagram_graph.add_edge(source_ref_id, target_ref_id)
        flow = self.diagram_graph.edge[source_ref_id][target_ref_id]
        flow["id"] = sequence_flow_id
        flow["name"] = sequence_flow_name
        flow["source_id"] = source_ref_id
        flow["target_id"] = target_ref_id
        source_node = self.diagram_graph.node[source_ref_id]
        target_node = self.diagram_graph.node[target_ref_id]
        flow["waypoints"] = \
            [(source_node["x"], source_node["y"]),
             (target_node["x"], target_node["y"])]

        # add target node (target_ref_id) as outgoing node from source node (source_ref_id)
        source_node["outgoing"].append(sequence_flow_id)

        # add source node (source_ref_id) as incoming node to target node (target_ref_id)
        target_node["incoming"].append(sequence_flow_id)
        return sequence_flow_id, flow

    def get_nodes_positions(self):
        """
        Getter method for nodes positions.
        :return: A dictionary with nodes as keys and positions as values
        """
        nodes = self.get_nodes()
        output = {}
        for node in nodes:
            output[node[0]] = (float(node[1]["x"]), float(node[1]["y"]))
        return output
