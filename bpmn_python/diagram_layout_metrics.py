# coding=utf-8
"""
Collection of different metrics used to compare diagram layout quality
"""
import copy


def count_crossing_points(bpmn_graph):
    """

    :param bpmn_graph:
    :return:
    """
    flows = bpmn_graph.get_flows()
    segments = get_flows_segments(flows)

    crossing_point_num = 0
    while (segments):
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
        waypoints = copy.deepcopy(flow[2]["waypoints"])
        source = waypoints.pop(0)
        while len(waypoints) > 0:
            target = waypoints.pop(0)
            segments.append({source_param_name: {"x": float(source[0]), "y": float(source[1])},
                             target_param_name: {"x": float(target[0]), "y": float(target[1])}})
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
    return p1['x'] == p2['x'] and p1['y'] == p2['y']


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
    val = (p2['y'] - p1['y']) * (p3['x'] - p2['x']) - (p2['x'] - p1['x']) * (p3['y'] - p2['y'])

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
    return min(p1['x'], p2['x']) <= p3['x'] <= max(p1['x'], p2['x']) \
           and min(p1['y'], p2['y']) <= p3['y'] <= max(p1['y'], p2['y'])


def min_int(v1, v2):
    """

    :param v1:
    :param v2:
    :return:
    """
    if v1 < v2:
        return v1
    else:
        return v2


def max(v1, v2):
    """

    :param v1:
    :param v2:
    :return:
    """
    if v1 >= v2:
        return v1
    else:
        return v2


def count_segments(bpmn_graph):
    """

    :param bpmn_graph:
    """
    flows = bpmn_graph.get_flows()
    segments = get_flows_segments(flows)
    return len(segments)


def compute_longest_path(bpmn_path):
    """

    :param bpmn_path:
    """
    pass
