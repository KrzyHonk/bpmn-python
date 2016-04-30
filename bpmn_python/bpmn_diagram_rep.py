import networkx as nx
import uuid
import bpmn_python.bpmn_diagram_import as bpmn_import
import bpmn_python.bpmn_diagram_export as bpmn_export


class BPMNDiagramGraph:
    """
    Class BPMNDiagramGraph implements simple inner representation of BPMN 2.0 diagram,
    based on NetworkX graph implementation

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

    def load_diagram_from_xml(self, filepath):
        """
        Reads an XML file from given filepath and maps it into inner representation of BPMN diagram.
        Returns an instance of BPMNDiagramGraph class.

        :param filepath: string with output filepath.
        """

        bpmn_import.BPMNDiagramGraphImport.load_diagram_from_xml(filepath, self.diagram_graph,
                                                                 self.sequence_flows, self.process_attributes,
                                                                 self.diagram_attributes, self.plane_attributes)

    def export_xml_file(self, output_path):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (with Diagram Interchange data).

        :param output_path: string representing output pathfile.
        """
        bpmn_export.BPMNDiagramGraphExport.export_xml_file(output_path, self.diagram_graph, self.sequence_flows,
                                                           self.process_attributes, self.diagram_attributes,
                                                           self.plane_attributes)

    def export_xml_file_no_di(self, output_path):
        """
        Exports diagram inner graph to BPMN 2.0 XML file (without Diagram Interchange data).

        :param output_path: string representing output pathfile.
        """
        bpmn_export.BPMNDiagramGraphExport.export_xml_file_no_di(output_path, self.diagram_graph,
                                                                 self.sequence_flows, self.process_attributes)

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
            if node[1]["id"] == node_id:
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

    def get_edges(self):
        """
        Gets all graph edges.
        Returns a two-dimensional dictionary, where keys are IDs of nodes connected by edge,
        value is a dictionary of all edge attributes.
        """
        return self.diagram_graph.edges(data=True)

    def get_edge_by_id(self, edge_id):
        """
        Gets an edge with requested ID.
        Returns a tuple, where first value is node ID, second - a dictionary of all node attributes.

        :param edge_id: string with edge ID.
        """
        tmp_edges = self.diagram_graph.edges(data=True)
        for edge in tmp_edges:
            if edge[2]["id"] == edge_id:
                return edge

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

        :param node_type: string object. Represents type of BPMN node passed to method,
        :param node_id: string object. ID of given node,
        :param node_name: string object. Node name.
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

    def add_task_to_diagram(self, task_name=""):
        """
        Adds a Task element to BPMN diagram.
        User-defined attributes:
        - name
        Returns a tuple, where first value is task ID, second a reference to created object.

        :param task_name: string object. Name of task.
        """
        task_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("task", task_id, task_name)
        return task_id, self.diagram_graph.node[task_id]

    # TODO add isExpanded?
    def add_subprocess_to_diagram(self, subprocess_name, triggered_by_event=False):
        """
        Adds a SubProcess element to BPMN diagram.
        User-defined attributes:
        - name
        - triggered_by_event
        Returns a tuple, where first value is subProcess ID, second a reference to created object.

        :param subprocess_name: string object. Name of subprocess,
        :param triggered_by_event: boolean value for attribute "triggeredByEvent". Default value false.
        """
        subprocess_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("subProcess", subprocess_id, subprocess_name)
        self.diagram_graph.node[subprocess_id]["triggeredByEvent"] = "true" if triggered_by_event else "false"
        return subprocess_id, self.diagram_graph.node[subprocess_id]

    def add_start_event_to_diagram(self, start_event_name="", start_event_definition=None, parallel_multiple=False):
        """
        Adds a StartEvent element to BPMN diagram.
        User-defined attributes:
        - name
        - parallel_multiple
        Returns a tuple, where first value is startEvent ID, second a reference to created object.

        :param start_event_name: string object. Name of start event,
        :param start_event_definition: list of event definitions. By default - empty,
        :param parallel_multiple: boolean value for attribute "parallelMultiple".
        """
        start_event_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("startEvent", start_event_id, start_event_name)
        self.diagram_graph.node[start_event_id]["parallelMultiple"] = "true" if parallel_multiple else "false"
        # TODO Add event definition
        self.diagram_graph.node[start_event_id]["event_definitions"] = []
        return start_event_id, self.diagram_graph.node[start_event_id]

    def add_end_event_to_diagram(self, end_event_name="", end_event_definition=None):
        """
        Adds an EndEvent element to BPMN diagram.
        User-defined attributes:
        - name
        Returns a tuple, where first value is endEvent ID, second a reference to created object.

        :param end_event_name: string object. Name of end event,
        :param end_event_definition: list of event definitions. By default - empty.
        """
        end_event_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.add_flow_node_to_diagram("endEvent", end_event_id, end_event_name)
        # TODO Add event definition
        self.diagram_graph.node[end_event_id]["event_definitions"] = []
        return end_event_id, self.diagram_graph.node[end_event_id]

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
        sequence_flow_id = BPMNDiagramGraph.id_prefix + str(uuid.uuid4())
        self.sequence_flows[sequence_flow_id] = (source_ref_id, target_ref_id)
        self.diagram_graph.add_edge(source_ref_id, target_ref_id)
        self.diagram_graph.edge[source_ref_id][target_ref_id]["id"] = sequence_flow_id
        self.diagram_graph.edge[source_ref_id][target_ref_id]["name"] = sequence_flow_name
        self.diagram_graph.edge[source_ref_id][target_ref_id]["waypoints"] = \
            [(self.diagram_graph.node[source_ref_id]["x"], self.diagram_graph.node[source_ref_id]["y"]),
             (self.diagram_graph.node[target_ref_id]["x"], self.diagram_graph.node[target_ref_id]["y"])]

        # add target node (target_ref_id) as outgoing node from source node (source_ref_id)
        self.diagram_graph.node[source_ref_id]["outgoing"].append(target_ref_id)

        # add source node (source_ref_id) as incoming node to target node (target_ref_id)
        self.diagram_graph.node[target_ref_id]["incoming"].append(source_ref_id)
        return sequence_flow_id, self.diagram_graph.edge[source_ref_id][target_ref_id]
