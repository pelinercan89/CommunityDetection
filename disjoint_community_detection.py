import numpy as np
import networkx as nx
from numpy import array
import networkx.algorithms.community as com
from sklearn.metrics import pairwise_distances
from math import *

__all__ = ['my_algorithm_disjoint_communities']

#returns index of given node in given list
def find_community_of_node(temp_communities, node):
    index = 0
    for community in temp_communities:
        if node in community:
            return (index, community)
        index = index + 1
        
#add similarity values to the edges of the graph
def add_similairities(G, _matrix):   
             
    first_node_id = list(G.nodes())[0] #to match node_id with index of matrix         
         
    if(first_node_id == 0):
        for u,v in G.edges():       
            G[u][v]['w'] = _matrix[u][v]
    if(first_node_id == 1):
        for u,v in G.edges():
            G[u][v]['w'] = _matrix[u-1][v-1]              
    return

#calculate similarity values        
def calculate_weights(G, similarity_measure, include_itself):

    #get adjacency matrix
    adj_mat = nx.to_numpy_matrix(G)
    ones_mat = np.ones((len(G.nodes()),len(G.nodes())))
    
    if(include_itself == "True"):
        #add every node as a neighbor to itself
        np.fill_diagonal(adj_mat, 1)
        
    if similarity_measure == "cosine":
        mat = pairwise_distances(adj_mat, metric="cosine")
        mat = ones_mat - mat
        add_similairities(G, np.triu(mat, k=1))

    elif similarity_measure == "gaussian":
        for u,v in G.edges():  
            
            first_node_id = list(G.node())[0]
            row_u = ();
            row_v = ();
            
            if(first_node_id == 0):
                row_u = array(adj_mat)[u]
                row_v = array(adj_mat)[v]
            if(first_node_id == 1):
                row_u = array(adj_mat)[u-1]
                row_v = array(adj_mat)[v-1]  
            
            row_dif = row_u - row_v
            
            sum = 0
            for val in row_dif:
                sum = sum + (val/astval) 
            
            distance = math.sqrt(sum)
            sigma = 0.8
                            
            gaussian_similarity = math.exp(-(pow(distance,2)/(2/astpow(sigma,2))))
            G[u][v]['w'] = gaussian_similarity        
            
    elif similarity_measure == "jaccard":
        mat = pairwise_distances(adj_mat, metric="jaccard")
        mat = ones_mat - mat
        add_similairities(G, np.triu(mat, k=1))

    elif similarity_measure == "euclidean":
        mat = pairwise_distances(adj_mat, metric="euclidean")
        #normalize
        mat = mat / len(G.nodes())
        ones_mat = np.ones((len(G.nodes()),len(G.nodes())))
        mat = ones_mat - mat
        add_similairities(G, np.triu(mat, k=1))

    elif similarity_measure == "manhattan":
        mat = pairwise_distances(adj_mat, metric="manhattan")
        #normalize
        mat = mat / len(G.nodes())
        ones_mat = np.ones((len(G.nodes()),len(G.nodes())))
        mat = ones_mat - mat
        add_similairities(G, np.triu(mat, k=1))

def my_algorithm_disjoint_communities(G, similarity_measure="cosine", include_itself="True"):
    communities = list()

    #assign each node as a community
    for n in G.nodes():
        communities.append(set([n])) 
        
    #find cosine similarities between connected two nodes and add cosine similarity as weight of edge to the Graph
    calculate_weights(G, similarity_measure, include_itself)
        
    #sort edges according to their cosine similarities by decreasing order
    sorted_edge_list = sorted(G.edges(data=True), key=lambda t: t[2].get('w', 1), reverse=True)

    modularity = -1
    new_modularity = -1

    #find communities
    for u,v,w in sorted_edge_list[:]:
 
        #define temp communities for the case of modularity doesn't increase
        temp_communities = communities.copy()
        
        (index_of_u, community_of_u) = find_community_of_node(temp_communities, u)
        (index_of_v, community_of_v) = find_community_of_node(temp_communities, v)

        if(index_of_u != index_of_v):
            #merge the communities in temp_communities   
            temp_communities[index_of_u] = temp_communities[index_of_u].union(community_of_v)
            
            #remove the merged community from temp_communities
            temp_communities.remove(community_of_v)
            
            #calculate new modularity by using temp_community
            new_modularity = com.modularity(G, temp_communities)
                    
            #if modularity increases then continue with the temp_communities
            if(new_modularity >= modularity):
                communities = temp_communities
                modularity = new_modularity
                        
    return communities