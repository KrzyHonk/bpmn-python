# coding=utf-8
"""
Package with BPMNDiagramGraph - graph representation of BPMN diagram
"""
import copy

import bpmn_python.bpmn_python_consts as consts
import bpmn_python.grid_cell_class as cell_class


def generate_layout(bpmn_graph):
    """
    :param bpmn_graph: an instance of BPMNDiagramGraph class.
    """
    classification = generate_elements_clasification(bpmn_graph)
    (sorted_nodes_with_classification, backward_flows) = topological_sort(bpmn_graph, classification[0])
    grid = grid_layout(bpmn_graph, sorted_nodes_with_classification)
    set_coordinates_for_nodes(bpmn_graph, grid)
    set_flows_waypoints(bpmn_graph)


def generate_elements_clasification(bpmn_graph):
    """
    :param bpmn_graph:
    :return:
    """
    nodes_classification = []
    node_param_name = "node"
    flow_param_name = "flow"
    classification_param_name = "classification"

    classification_element = "Element"
    classification_join = "Join"
    classification_split = "Split"
    classification_start_event = "Start Event"
    classification_end_event = "End Event"

    task_list = bpmn_graph.get_nodes(consts.Consts.task)
    for element in task_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    subprocess_list = bpmn_graph.get_nodes(consts.Consts.subprocess)
    for element in subprocess_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    complex_gateway_list = bpmn_graph.get_nodes(consts.Consts.complex_gateway)
    for element in complex_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    event_based_gateway_list = bpmn_graph.get_nodes(consts.Consts.event_based_gateway)
    for element in event_based_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    inclusive_gateway_list = bpmn_graph.get_nodes(consts.Consts.inclusive_gateway)
    for element in inclusive_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    exclusive_gateway_list = bpmn_graph.get_nodes(consts.Consts.exclusive_gateway)
    for element in exclusive_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    parallel_gateway_list = bpmn_graph.get_nodes(consts.Consts.parallel_gateway)
    for element in parallel_gateway_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    start_event_list = bpmn_graph.get_nodes(consts.Consts.start_event)
    for element in start_event_list:
        tmp = [classification_element, classification_start_event]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    intermediate_catch_event_list = bpmn_graph.get_nodes(consts.Consts.intermediate_catch_event)
    for element in intermediate_catch_event_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    end_event_list = bpmn_graph.get_nodes(consts.Consts.end_event)
    for element in end_event_list:
        tmp = [classification_element, classification_end_event]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    intermediate_throw_event_list = bpmn_graph.get_nodes(consts.Consts.intermediate_throw_event)
    for element in intermediate_throw_event_list:
        tmp = [classification_element]
        if len(element[1][consts.Consts.incoming_flow]) >= 2:
            tmp.append(classification_join)
        if len(element[1][consts.Consts.outgoing_flow]) >= 2:
            tmp.append(classification_split)
        nodes_classification += [{node_param_name: element, classification_param_name: tmp}]

    flows_classification = []
    flows_list = bpmn_graph.get_flows()
    for flow in flows_list:
        flows_classification += [{flow_param_name: flow, classification_param_name: ["Flow"]}]

    return nodes_classification, flows_classification


def topological_sort(bpmn_graph, nodes_with_classification):
    """
    :return:
    """
    node_param_name = "node"
    classification_param_name = "classification"

    tmp_nodes_with_classification = copy.deepcopy(nodes_with_classification)
    sorted_nodes_with_classification = []
    no_incoming_flow_nodes = []
    backward_flows = []

    while tmp_nodes_with_classification:
        for node_with_classification in tmp_nodes_with_classification:
            incoming_list = node_with_classification[node_param_name][1][consts.Consts.incoming_flow]
            if len(incoming_list) == 0:
                no_incoming_flow_nodes.append(node_with_classification)
        if len(no_incoming_flow_nodes) > 0:
            while len(no_incoming_flow_nodes) > 0:
                node_with_classification = no_incoming_flow_nodes.pop()
                tmp_nodes_with_classification.remove(node_with_classification)
                sorted_nodes_with_classification \
                    .append(next(tmp_node for tmp_node in nodes_with_classification
                                 if tmp_node[node_param_name][0] == node_with_classification[node_param_name][0]))

                outgoing_list = list(node_with_classification[node_param_name][1][consts.Consts.outgoing_flow])
                tmp_outgoing_list = list(outgoing_list)

                for flow_id in tmp_outgoing_list:
                    '''
                    - Remove the outgoing flow for source flow node (the one without incoming flows)
                    - Get the target node
                    - Remove the incoming flow for target flow node
                    '''
                    outgoing_list.remove(flow_id)
                    node_with_classification[node_param_name][1][consts.Consts.outgoing_flow].remove(flow_id)

                    flow = bpmn_graph.get_flow_by_id(flow_id)
                    target_id = flow[2][consts.Consts.target_ref]
                    target = next(tmp_node[node_param_name]
                                  for tmp_node in tmp_nodes_with_classification
                                  if tmp_node[node_param_name][0] == target_id)
                    target[1][consts.Consts.incoming_flow].remove(flow_id)
        else:
            for node_with_classification in tmp_nodes_with_classification:
                if "Join" in node_with_classification[classification_param_name]:
                    incoming_list = list(node_with_classification[node_param_name][1][consts.Consts.incoming_flow])
                    tmp_incoming_list = list(incoming_list)
                    for flow_id in tmp_incoming_list:
                        incoming_list.remove(flow_id)

                        flow = bpmn_graph.get_flow_by_id(flow_id)

                        source_id = flow[2][consts.Consts.source_ref]
                        source = next(tmp_node[node_param_name]
                                      for tmp_node in tmp_nodes_with_classification
                                      if tmp_node[node_param_name][0] == source_id)
                        source[1][consts.Consts.outgoing_flow].remove(flow_id)

                        target_id = flow[2][consts.Consts.target_ref]
                        target = next(tmp_node[node_param_name]
                                      for tmp_node in tmp_nodes_with_classification
                                      if tmp_node[node_param_name][0] == target_id)
                        target[1][consts.Consts.incoming_flow].remove(flow_id)
                        backward_flows.append(flow)
    return sorted_nodes_with_classification, backward_flows


def grid_layout(bpmn_graph, sorted_nodes_with_classification):
    """

    :param sorted_nodes_with_classification:
    :param bpmn_graph:
    :return:
    """
    tmp_nodes_with_classification = list(sorted_nodes_with_classification)

    last_row = 1
    last_col = 1
    grid = []
    while tmp_nodes_with_classification:
        node_with_classification = tmp_nodes_with_classification.pop(0)
        (grid, last_row, last_col) = place_element_in_grid(node_with_classification, grid, last_row, last_col,
                                                           bpmn_graph, tmp_nodes_with_classification)
    return grid


def place_element_in_grid(node_with_classification, grid, last_row, last_col, bpmn_graph, nodes_with_classification,
                          enforced_row_num=None):
    """

    :param node_with_classification:
    :param grid:
    :param last_row:
    :param last_col:
    :param bpmn_graph:
    :param nodes_with_classification:
    :param enforced_row_num:
    :return:
    """
    node_param_name = "node"
    classification_param_name = "classification"

    node_id = node_with_classification[node_param_name][0]
    incoming_flows = node_with_classification[node_param_name][1][consts.Consts.incoming_flow]
    outgoing_flows = node_with_classification[node_param_name][1][consts.Consts.outgoing_flow]

    if len(incoming_flows) == 0:
        # if node has no incoming flow, put it in new row
        current_element_row = last_row
        current_element_col = last_col
        if enforced_row_num:
            insert_into_grid(grid, enforced_row_num, current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row, current_element_col, node_id)
        last_row += 1
    elif "Join" not in node_with_classification[classification_param_name]:
        # if node is not a Join, put it right from its predecessor (element should only have one predecessor)
        flow_id = incoming_flows[0]
        flow = bpmn_graph.get_flow_by_id(flow_id)
        predecessor_id = flow[2][consts.Consts.source_ref]
        predecessor_cell = next(grid_cell for grid_cell in grid if grid_cell.node_id == predecessor_id)
        # insert into cell right from predecessor - no need to insert new column or row
        current_element_row = predecessor_cell.row
        current_element_col = predecessor_cell.col + 1
        if enforced_row_num:
            insert_into_grid(grid, enforced_row_num, current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row, current_element_col, node_id)
    # TODO consider rule for split/join node
    else:
        # find the rightmost predecessor - put into next column
        # if last_split was passed, use row number from it, otherwise compute mean from predecessors
        predecessors_id_list = []
        for flow_id in incoming_flows:
            flow = bpmn_graph.get_flow_by_id(flow_id)
            predecessors_id_list.append(flow[2][consts.Consts.source_ref])

        max_col_num = 0
        row_num_sum = 0
        # TODO try to implement corresponding split finding
        for grid_cell in grid:
            if grid_cell.node_id in predecessors_id_list:
                row_num_sum += grid_cell.row
                if grid_cell.col > max_col_num:
                    max_col_num = grid_cell.col
        current_element_row = row_num_sum // len(predecessors_id_list)
        current_element_col = max_col_num + 1
        if enforced_row_num:
            insert_into_grid(grid, enforced_row_num, current_element_col, node_id)
        else:
            insert_into_grid(grid, current_element_row, current_element_col, node_id)

    if "Split" in node_with_classification[classification_param_name]:
        successors_id_list = []
        for flow_id in outgoing_flows:
            flow = bpmn_graph.get_flow_by_id(flow_id)
            successors_id_list.append(flow[2][consts.Consts.target_ref])
        num_of_successors = len(successors_id_list)
        if num_of_successors % 2 != 0:
            # if number of successors is even, put one half over the split, second half below
            # proceed with first half
            centre = (num_of_successors // 2)
            for index in range(0, centre):
                # place element above split
                successor_node = next(successor_node for successor_node in nodes_with_classification
                                      if successor_node[node_param_name][0] == successors_id_list[index])
                (grid, last_row, last_col) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                   bpmn_graph, current_element_row + 1)
            successor_node = next(successor_node for successor_node in nodes_with_classification
                                  if successor_node[node_param_name][0] == successors_id_list[centre + 1])
            (grid, last_row, last_col) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                               bpmn_graph, current_element_row + 1)
            for index in range(centre + 2, num_of_successors):
                # place element below split
                successor_node = next(successor_node for successor_node in nodes_with_classification
                                      if successor_node[node_param_name][0] == successors_id_list[index])
                (grid, last_row, last_col) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                   bpmn_graph, current_element_row - 1)
        else:
            centre = (num_of_successors // 2)
            for index in range(0, centre):
                # place element above split
                successor_node = next(successor_node for successor_node in nodes_with_classification
                                      if successor_node[node_param_name][0] == successors_id_list[index])
                (grid, last_row, last_col) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                   bpmn_graph, current_element_row + 1)
            for index in range(centre + 1, num_of_successors):
                # place element below split
                successor_node = next(successor_node for successor_node in nodes_with_classification
                                      if successor_node[node_param_name][0] == successors_id_list[index])
                (grid, last_row, last_col) = place_element_in_grid(successor_node, grid, last_row, last_col,
                                                                   bpmn_graph, current_element_row - 1)
    return grid, last_row, last_col


def insert_into_grid(grid, row, col, node_id):
    """

    :param grid:
    :param row:
    :param col:
    :param node_id:
    """
    if row <= 0:
        row = 1
    occupied_cell = None
    try:
        occupied_cell = next(grid_cell for grid_cell in grid if grid_cell.row == row and grid_cell.col == col)
    except StopIteration:
        pass
    # if cell is already occupied, insert new row
    if occupied_cell:
        for grid_cell in grid:
            if grid_cell.row >= row:
                grid_cell.row += 1
    grid.append(cell_class.GridCell(row, col, node_id))


def set_coordinates_for_nodes(bpmn_graph, grid):
    """

    :param bpmn_graph:
    :param grid:
    """

    nodes = bpmn_graph.get_nodes()
    for node in nodes:
        cell = next(grid_cell for grid_cell in grid if grid_cell.node_id == node[0])
        node[1][consts.Consts.x] = str(cell.col * 150 + 50)
        node[1][consts.Consts.y] = str(cell.row * 100 + 50)


def set_flows_waypoints(bpmn_graph):
    """

    :param bpmn_graph:
    """
    # TODO hardcoded node center, better compute it with x,y coordinates and height/width
    # TODO get rid of string cast
    flows = bpmn_graph.get_flows()
    for flow in flows:
        source_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.source_ref])
        target_node = bpmn_graph.get_node_by_id(flow[2][consts.Consts.target_ref])
        flow[2][consts.Consts.waypoints] = [(str(int(source_node[1][consts.Consts.x]) + 50),
                                             str(int(source_node[1][consts.Consts.y]) + 50)),
                                            (str(int(target_node[1][consts.Consts.x]) + 50),
                                             str(int(target_node[1][consts.Consts.y]) + 50))]
