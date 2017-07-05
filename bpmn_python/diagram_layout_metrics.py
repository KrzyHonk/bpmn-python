# coding=utf-8
"""
Collection of different metrics used to compare diagram layout quality
"""
import copy
import bpmn_python.bpmn_python_consts as consts


def count_crossing_points(bpmn_graph):
    """

    :param bpmn_graph:
    :return:
    """
    flows = bpmn_graph.get_flows()
    segments = get_flows_segments(flows)

    crossing_point_num = 0
    while segments:
        segment_one = segments.pop()
        for segment_two in segments:
            if segments_common_points(segment_one, segment_two) is False and do_intersect(segment_one, segment_two):
                crossing_point_num += 1

    return crossing_point_num


def compute_determinant(p1, p2, p3):
    """

    :param p1:
    :param p2:
    :param p3:
    :return:
    """
    det = float(p1[0]) * float(p2[1]) + float(p2[0]) * float(p3[1]) + float(p3[0]) * float(p1[1])
    det -= float(p1[0]) * float(p3[1]) + float(p2[0]) * float(p1[1]) + float(p3[0]) * float(p2[1])
    return det


def check_integer_sign(value):
    """

    :param value:
    :return:
    """
    return value >= 0


def get_flows_segments(flows):
    """

    :param flows:
    """
    source_param_name = "source"
    target_param_name = "target"

    segments = []
    for flow in flows:
        waypoints = copy.deepcopy(flow[2][consts.Consts.waypoints])
        source = waypoints.pop(0)
        while len(waypoints) > 0:
            target = waypoints.pop(0)
            segments.append({source_param_name: {consts.Consts.x: float(source[0]), consts.Consts.y: float(source[1])},
                             target_param_name: {consts.Consts.x: float(target[0]), consts.Consts.y: float(target[1])}})
            source = target
    return segments


def segments_common_points(segment_one, segment_two):
    """

    :param segment_one:
    :param segment_two:
    :return:
    """
    source_param = "source"
    target_param = "target"
    return points_are_equal(segment_one[source_param], segment_two[source_param]) \
        or points_are_equal(segment_one[source_param], segment_two[target_param]) \
        or points_are_equal(segment_one[target_param], segment_two[source_param]) \
        or points_are_equal(segment_one[target_param], segment_two[target_param])


def points_are_equal(p1, p2):
    """

    :param p1:
    :param p2:
    :return:
    """
    return p1[consts.Consts.x] == p2[consts.Consts.x] and p1[consts.Consts.y] == p2[consts.Consts.y]


def do_intersect(segment_one, segment_two):
    """

    :param segment_one:
    :param segment_two:
    :return:
    """
    source_param = "source"
    target_param = "target"
    # Find the four orientations needed for general and special cases
    o1 = orientation(segment_one[source_param], segment_one[target_param], segment_two[source_param])
    o2 = orientation(segment_one[source_param], segment_one[target_param], segment_two[target_param])
    o3 = orientation(segment_two[source_param], segment_two[target_param], segment_one[source_param])
    o4 = orientation(segment_two[source_param], segment_two[target_param], segment_one[target_param])

    if o1 != o2 and o3 != o4:
        return True

    # Special Cases
    if o1 == 0 and lies_on_segment(segment_one[source_param], segment_one[target_param], segment_two[source_param]):
        return True

    if o2 == 0 and lies_on_segment(segment_one[source_param], segment_one[target_param], segment_two[target_param]):
        return True

    if o3 == 0 and lies_on_segment(segment_two[source_param], segment_two[target_param], segment_one[source_param]):
        return True

    if o4 == 0 and lies_on_segment(segment_two[source_param], segment_two[target_param], segment_one[target_param]):
        return True

    # Neither of special cases
    return False


def orientation(p1, p2, p3):
    """
    Finds orientation of three points p1, p2, p3.
    The function returns following values
    0 --> p1, p2 and p3 are collinear
    1 --> Clockwise
    2 --> Counterclockwise
    :param p1: tuple representing two dimensional point
    :param p2: tuple representing two dimensional point
    :param p3: tuple representing two dimensional point
    """
    val = (p2[consts.Consts.y] - p1[consts.Consts.y]) * (p3[consts.Consts.x] - p2[consts.Consts.x]) \
        - (p2[consts.Consts.x] - p1[consts.Consts.x]) * (p3[consts.Consts.y] - p2[consts.Consts.y])

    if val == 0:
        return 0  # collinear
    elif val > 0:
        return 1  # clockwise
    else:
        return 2  # counterclockwise


def lies_on_segment(p1, p2, p3):
    """

    :param p1:
    :param p2:
    :param p3:
    :return:
    """
    return min(p1[consts.Consts.x], p2[consts.Consts.x]) <= p3[consts.Consts.x] \
        <= max(p1[consts.Consts.x], p2[consts.Consts.x])\
        and min(p1[consts.Consts.y],  p2[consts.Consts.y]) <= p3[consts.Consts.y] \
        <= max(p1[consts.Consts.y], p2[consts.Consts.y])


def count_segments(bpmn_graph):
    """

    :param bpmn_graph:
    """
    flows = bpmn_graph.get_flows()
    segments = get_flows_segments(flows)
    return len(segments)


def compute_longest_path(bpmn_graph):
    """

    :param bpmn_graph:
    """
    incoming_flows_list_param_name = "incoming"

    nodes = copy.deepcopy(bpmn_graph.get_nodes())
    no_incoming_flow_nodes = []
    for node in nodes:
        incoming_list = node[1][incoming_flows_list_param_name]
        if len(incoming_list) == 0:
            no_incoming_flow_nodes.append(node)

    longest_path = []
    for node in no_incoming_flow_nodes:
        (output_path, output_path_len) = find_longest_path([], node, bpmn_graph)
        if output_path_len > len(longest_path):
            longest_path = output_path
    return longest_path, len(longest_path)


def find_longest_path(previous_nodes, node, bpmn_graph):
    """

    :param previous_nodes:
    :param node:
    :param bpmn_graph:
    :return:
    """
    outgoing_flows_list_param_name = "outgoing"
    outgoing_flows_list = node[1][outgoing_flows_list_param_name]
    longest_path = []

    if len(outgoing_flows_list) == 0:
        tmp_previous_nodes = copy.deepcopy(previous_nodes)
        tmp_previous_nodes.append(node)
        return tmp_previous_nodes, len(tmp_previous_nodes)
    else:
        tmp_previous_nodes = copy.deepcopy(previous_nodes)
        tmp_previous_nodes.append(node)
        for outgoing_flow_id in outgoing_flows_list:
            flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.target_ref])
            if outgoing_node not in previous_nodes:
                (output_path, output_path_len) = find_longest_path(tmp_previous_nodes, outgoing_node, bpmn_graph)
                if output_path_len > len(longest_path):
                    longest_path = output_path
        return longest_path, len(longest_path)


def compute_longest_path_tasks(bpmn_graph):
    """

    :param bpmn_graph:
    """
    incoming_flows_list_param_name = "incoming"

    nodes = copy.deepcopy(bpmn_graph.get_nodes())
    no_incoming_flow_nodes = []
    for node in nodes:
        incoming_list = node[1][incoming_flows_list_param_name]
        if len(incoming_list) == 0:
            no_incoming_flow_nodes.append(node)

    longest_path = []
    for node in no_incoming_flow_nodes:
        (all_nodes, qualified_nodes) = find_longest_path_tasks([], [], node, bpmn_graph)
        if len(qualified_nodes) > len(longest_path):
            longest_path = qualified_nodes
    return longest_path, len(longest_path)


def find_longest_path_tasks(path, qualified_nodes, node, bpmn_graph):
    """

    :param path:
    :param qualified_nodes:
    :param node:
    :param bpmn_graph:
    :return:
    """
    node_names = {"task", "subProcess"}
    outgoing_flows_list = node[1][consts.Consts.outgoing_flow]

    if len(outgoing_flows_list) == 0:
        tmp_path = copy.deepcopy(path)
        tmp_path.append(node)
        tmp_qualified_nodes = copy.deepcopy(qualified_nodes)
        if node[1][consts.Consts.type] in node_names:
            tmp_qualified_nodes.append(node)
        return tmp_path, tmp_qualified_nodes
    else:
        longest_qualified_nodes = []
        longest_path = copy.deepcopy(path)
        longest_path.append(node)
        for outgoing_flow_id in outgoing_flows_list:
            flow = bpmn_graph.get_flow_by_id(outgoing_flow_id)
            outgoing_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.target_ref])
            tmp_path = copy.deepcopy(path)
            tmp_path.append(node)
            tmp_qualified_nodes = copy.deepcopy(qualified_nodes)
            if node[1]["type"] in node_names:
                tmp_qualified_nodes.append(node)

            if outgoing_node not in path:
                (path_all_nodes, path_qualified_nodes) = find_longest_path_tasks(tmp_path, tmp_qualified_nodes,
                                                                                 outgoing_node, bpmn_graph)
                if len(path_qualified_nodes) > len(longest_qualified_nodes):
                    longest_qualified_nodes = path_qualified_nodes
                    longest_path = path_all_nodes
            else:
                if len(tmp_qualified_nodes) > len(longest_qualified_nodes):
                    longest_qualified_nodes = tmp_qualified_nodes
                    longest_path = tmp_path
        return longest_path, longest_qualified_nodes
