import numpy as np
import networkx.algorithms.community as nx_comm


def modularity(graph, communities):
    return nx_comm.modularity(graph, communities)


def shen_modularity(graph, communities):
    # find belonging degrees of each node for each community
    belongingMatrix = np.zeros((graph.number_of_nodes(), len(communities)))

    for communityNo, community in enumerate(communities):
        belongingMatrix[[int(n) for n in community], communityNo] = 1

    belongingMatrix = belongingMatrix / belongingMatrix.sum(1, keepdims=True)

    modularity = 0.0
    m = 2 * len(graph.edges())

    for c in range(0, len(communities)):

        for nd1 in graph.nodes:
            for nd2 in graph.nodes:
                sigma = int(graph.has_edge(nd1, nd2))
                suv = belongingMatrix[nd1][c] * belongingMatrix[nd2][c]
                modularity += suv * \
                    (sigma - (graph.degree(nd1)*graph.degree(nd2)/m))

    return modularity / m


def my_modularity(graph, communities):
    if len(communities.communities) == 1:
        return 0

    communities = communities.to_node_community_map()

    edge_list = graph.edges()
    m = len(edge_list)

    in_edge = 0
    out_edge = 0

    for (u, v) in edge_list:
        if len(set(communities[v]).intersection(set(communities[u]))) > 0:
            in_edge = in_edge + 1
        else:
            out_edge = out_edge + 1

    my_modularity_score = (m + in_edge - out_edge)/(2*m)

    return my_modularity_score
