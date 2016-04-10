import matplotlib.pyplot as plt
import networkx as nx


def visualize_diagram(diagram_graph):
    G=diagram_graph.diagram_graph
    pos=nx.spring_layout(G)
    nx.draw(G,pos,with_labels=True)
    plt.show()
