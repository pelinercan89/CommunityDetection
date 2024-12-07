import math

__all__ = ['my_algorithm_overlapping_communities']
     
def select_community_using_my_metric(communities, communities_of_node, neighbors_of_node):
    metric = -1
    return_index = 0
    for index in communities_of_node:
        new_metric = len(communities[index].intersection(neighbors_of_node))
        
        # print("new_metric ", new_metric)
        if new_metric > metric:
            return_index = index
            metric = new_metric
    return (metric, return_index)

def calculate_weights(G):   
    for u,v in G.edges():                    
        uNeighbors = frozenset(G.neighbors(u)).union({u})
        vNeighbors = frozenset(G.neighbors(v)).union({v})
        commonNeighbors = uNeighbors.intersection(vNeighbors)
        
        G[u][v]['w'] = len(commonNeighbors) / (math.sqrt(len(uNeighbors) * len(vNeighbors)))

def find_all_communities_of_node(communities, node):
    community_list = list()
    index = 0
    for community in communities:
        if node in community:
            community_list.append(index)
        index = index + 1
    return community_list



def my_algorithm_overlapping_communities(G):
    communities = list()
        
    #assign each node as a community
    for n in G.nodes():
        communities.append(set([n])) 
                                
    #find cosine similarities between connected two nodes and add cosine similarity as weight of edge to the Graph
    calculate_weights(G)
        
    #sort edges according to their cosine similarities by decreasing order
    sorted_edge_list = sorted(G.edges(data=True), key=lambda t: t[2].get('w', -1), reverse=True)    
    
    # print("sorted_edge_list ", sorted_edge_list)

    #find communities
    for u,v,w in sorted_edge_list[:]:

        # print("u ", u, "v ", v)
    
        if u == v:
          continue
          
        if ({u} in communities) and ({v} in communities):
            communities.remove({u})
            communities.remove({v})
            communities.append({u,v})
            continue
        
        # define temp communities for the case of modularity doesn’t increase        
        communities_of_node_1 = find_all_communities_of_node(communities, u) 
        communities_of_node_2 = find_all_communities_of_node(communities, v)

        if len( set(communities_of_node_1).intersection(set(communities_of_node_2)) ) == 0:        
            
            (metric_1, index_1) = select_community_using_my_metric(communities, communities_of_node_1, set(G.neighbors(v)))
            (metric_2, index_2) = select_community_using_my_metric(communities, communities_of_node_2, set(G.neighbors(u)))
            
            
            if metric_1 > metric_2:
                communities[index_1] = communities[index_1].union({v}) 
                if {v} in communities:
                    communities.remove({v})
            elif metric_2 > metric_1:
                communities[index_2] = communities[index_2].union({u})
                if {u} in communities:
                    communities.remove({u}) 
            else:
                if G.degree(u) < G.degree(v):
                    communities[index_2] = communities[index_2].union({u})
                    if {u} in communities:
                        communities.remove({u}) 
                else:
                    communities[index_1] = communities[index_1].union({v}) 
                    if {v} in communities:
                        communities.remove({v})
   

        # print("communities ", communities)
    #merge some overlapping communities
    sorted_communities = sorted(communities, key=len, reverse=True)
    index1 = 1
      
    # print("sorted communities ", sorted_communities)
    while index1 < len(sorted_communities):
        index2 = index1 - 1
        while index2 >= 0:
            #(1/2.5)
            if len(set(sorted_communities[index1]).intersection(set(sorted_communities[index2]))) > (1/2)*len(sorted_communities[index1]):
                sorted_communities[index1] = set(sorted_communities[index1]).union(set(sorted_communities[index2]))
                sorted_communities.remove(sorted_communities[index2])
                index1 = index1 - 1 
            elif len(sorted_communities[index1]) == 2 and len(set(sorted_communities[index1]).intersection(set(sorted_communities[index2]))) == (1/2)*len(sorted_communities[index1]):   
                sorted_communities[index1] = set(sorted_communities[index1]).union(set(sorted_communities[index2]))
                sorted_communities.remove(sorted_communities[index2])
                index1 = index1 - 1
            index2 = index2 - 1
        index1 = index1 + 1
    
    return sorted_communities