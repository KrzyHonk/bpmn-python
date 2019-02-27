# coding=utf-8
"""
Package used to unify the different constant values used in entire project
"""


class Consts(object):
    """
    Class used to unify the different constant values used in entire project
    """
    # BPMN 2.0 element attribute names
    id = "id"
    name = "name"
    # Flow nodes cannot use "name" parameter in dictionary, due to the errors with PyDot
    node_name = "node_name"
    gateway_direction = "gatewayDirection"
    default = "default"
    instantiate = "instantiate"
    event_gateway_type = "eventGatewayType"
    source_ref = "sourceRef"
    target_ref = "targetRef"
    triggered_by_event = "triggeredByEvent"
    parallel_multiple = "parallelMultiple"
    cancel_activity = "cancelActivity"
    attached_to_ref = "attachedToRef"
    is_interrupting = "isInterrupting"
    is_closed = "isClosed"
    is_executable = "isExecutable"
    is_expanded = "isExpanded"
    is_horizontal = "isHorizontal"
    is_collection = "isCollection"
    process_type = "processType"
    sequence_flow = "sequenceFlow"
    condition_expression = "conditionExpression"
    message_flow = "messageFlow"
    message_flows = "messageFlows"

    # CSV literals
    csv_order = "Order"
    csv_activity = "Activity"
    csv_condition = "Condition"
    csv_who = "Who"
    csv_subprocess = "Subprocess"
    csv_terminated = "Terminated"

    # BPMN 2.0 diagram interchange element attribute names
    bpmn_element = "bpmnElement"
    height = "height"
    width = "width"
    x = "x"
    y = "y"

    # BPMN 2.0 element names
    definitions = "definitions"
    collaboration = "collaboration"
    participant = "participant"
    participants = "participants"
    process = "process"
    process_ref = "processRef"
    lane = "lane"
    lanes = "lanes"
    lane_set = "laneSet"
    child_lane_set = "childLaneSet"
    flow_node_ref = "flowNodeRef"
    flow_node_refs = "flowNodeRefs"
    task = "task"
    user_task = "userTask"
    service_task = "serviceTask"
    manual_task = "manualTask"
    subprocess = "subProcess"
    data_object = "dataObject"
    complex_gateway = "complexGateway"
    event_based_gateway = "eventBasedGateway"
    inclusive_gateway = "inclusiveGateway"
    exclusive_gateway = "exclusiveGateway"
    parallel_gateway = "parallelGateway"
    start_event = "startEvent"
    intermediate_catch_event = "intermediateCatchEvent"
    end_event = "endEvent"
    intermediate_throw_event = "intermediateThrowEvent"
    boundary_event = "boundaryEvent"

    # BPMN 2.0 diagram interchange element names
    bpmn_shape = "BPMNShape"
    bpmn_edge = "BPMNEdge"

    # BPMN 2.0 child element names
    incoming_flow = "incoming"
    incoming_flow_list = "incoming_flow_list"
    outgoing_flow = "outgoing"
    outgoing_flow_list = "outgoing_flow_list"
    waypoint = "waypoint"
    waypoints = "waypoints"

    # Additional parameter names
    type = "type"
    event_definitions = "event_definitions"
    node_ids = "node_ids"
    definition_type = "definition_type"

    grid_column_width = 2
