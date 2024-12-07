import time
import my_globals
import modularities
import numpy as np
import overlapping_community_detection as my
import disjoint_community_detection as my_dis
import networkx as nx
import copy

from cdlib import algorithms, evaluation, NodeClustering

# Initialize result object
result = my_globals.Result()

# Define algorithm functions
algorithm_functions = {
    "core_expansion": algorithms.core_expansion,
    "ego_networks": algorithms.ego_networks,
    "lpanni": algorithms.lpanni,
    "percomvc": algorithms.percomvc,
    "girvan_newman": lambda nxG: algorithms.girvan_newman(nxG, 1),
    "greedy_modularity": algorithms.greedy_modularity,
    "louvain": algorithms.louvain,
    "k_clique": lambda nxG: algorithms.kclique(nxG, 3),
    "fluid_communities": lambda nxG: algorithms.async_fluid(nxG, k=4),
    "walktrap": algorithms.walktrap,
    "label_propagation": algorithms.label_propagation,
    "my_overlapping": my.my_algorithm_overlapping_communities,
    "my_disjoint": my_dis.my_algorithm_disjoint_communities
}

# Run algorithms and return a list of communities
def run_algorithm(nxG, algorithm_name, real_communities=None):
    
    if algorithm_name == "my":
        start_time = time.perf_counter()
        predicted_communities = my.my_algorithm_overlapping_communities(nxG)
        end_time = time.perf_counter()
        predicted_clusters = NodeClustering(predicted_communities, graph=None)
    else:
        start_time = time.perf_counter()
        predicted_clusters = algorithm_functions[algorithm_name](nxG)
        end_time = time.perf_counter()
        predicted_communities = list(map(set, set(map(frozenset, predicted_clusters.communities))))

    # Set communities
    result.predicted_communities = predicted_communities

    # Set time
    result.runtime = round((end_time - start_time), 4)

    # Set number of communities
    result.number_of_communities = len(predicted_communities)
        
    #girvan newman modularity works with nonoverlapping communities
    # result.modularity = round(modularities.modularity(nxG, predicted_communities), 2)
      
    # Set Shen modularity
    result.shen_modularity = round(modularities.shen_modularity(nxG, predicted_communities), 2)
    if np.isnan(result.shen_modularity):
        result.shen_modularity = 0.0

    # Set my modularity
    result.my_modularity = round(modularities.my_modularity(nxG, predicted_clusters), 2)

    # Set MGH NMI and F-score
    if real_communities:
        real_clusters = NodeClustering(real_communities, graph=None)
        result.real_clusters = real_clusters
        result.mgh_nmi = round(evaluation.overlapping_normalized_mutual_information_MGH(real_clusters, predicted_clusters).score, 2)
        result.f_score = round(evaluation.nf1(real_clusters, predicted_clusters).score, 2) if len(predicted_communities) > 0 else 0.0
                  
        #performance
        # print("performance ", nx.community.quality.performance(nxG, predicted_communities))
        
    return result

def run_algorithms_on_datasets(datasets):
    results = {}
    my_globals.print_header()
    
    for dataset in datasets:
        for algo_name in my_globals.SELECTED_ALGORITHMS.keys():
            result = copy.deepcopy(run_algorithm(dataset.nx_graph, algo_name, dataset.real_communities))
            result.set_dataset(dataset)
            result.algorithm_name = algo_name
            
            results[(dataset.name, algo_name)] = result   
            result.print_result()
    return results