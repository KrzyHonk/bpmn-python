import matplotlib.pyplot as plt
import networkx as nx
import pydotplus
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.drawing.nx_pydot import write_dot

def visualize_diagram(bpmn_diagram):
    G=bpmn_diagram.diagram_graph
    pos = graphviz_layout(G)
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("task"), node_shape='s', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("subProcess"), node_shape='s', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("complexGateway"), node_shape='d', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("eventBasedGateway"), node_shape='o', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("inclusiveGateway"), node_shape='d', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("exclusiveGateway"), node_shape='d', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("parallelGateway"), node_shape='d', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("startEvent"), node_shape='o', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("intermediateCatchEvent"), node_shape='o', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("endEvent"), node_shape='o', node_color='white')
    nx.draw_networkx_nodes(G, pos, nodelist=bpmn_diagram.get_nodes_id_list_by_type("intermediateThrowEvent"), node_shape='o', node_color='white')

    node_labels = {}
    for node in G.nodes(data=True):
        node_labels[node[0]] = node[1].get("node_name")
    nx.draw_networkx_labels(G, pos, node_labels)

    nx.draw_networkx_edges(G, pos)

    edge_labels = {}
    for edge in G.edges(data=True):
        edge_labels[(edge[0],edge[1])] = edge[2].get("name")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.show()

def bpmn_diagram_to_dot_file(bpmn_diagram, file_name):
    G = bpmn_diagram.diagram_graph
    write_dot(G,file_name + ".dot")

def bpmn_diagram_to_png(bpmn_diagram, file_name):
    G = bpmn_diagram.diagram_graph
    graph = pydotplus.Dot()

    for node in G.nodes(data=True):

        if node[1].get("type") == "task":
            n = pydotplus.Node(name=node[0], shape="box", style="rounded", label=node[1].get("node_name"))
        elif node[1].get("type") == "exclusiveGateway":
            n = pydotplus.Node(name=node[0], shape="diamond", label=node[1].get("node_name"))
        else:
            n = pydotplus.Node(name=node[0], label=node[1].get("node_name"))
        graph.add_node(n)

    for edge in G.edges(data=True):
        e = pydotplus.Edge(src=edge[0], dst=edge[1], label=edge[2].get("name"))
        graph.add_edge(e)

    graph.write(file_name + ".png", format='png')