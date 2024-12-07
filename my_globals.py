import networkx as nx
import igraph as ig
from enum import Enum

# Define all algorithms and selected algorithms
ALL_ALGORITHMS = {
    "ego_networks": "Ego Networks",
    "lpanni": "LPANNI",
    "core_expansion": "Core Expansion",
    "my": "Proposed"
}
SELECTED_ALGORITHMS = {}
SELECTED_DATASET_TYPE = None
MAXIMUM_GRAPH_SIZE = 200

class Dataset:
    def __init__(self):
        self.name = ""
        self.directory = ""
        self.nx_graph = nx.Graph()
        self.ig_graph = ig.Graph()
        self.layout = ig.Layout()
        self.real_communities = []            
        
class Result:
    def __init__(self):
        self.dataset_name = ""
        self.ig_graph = ig.Graph()
        self.layout = ig.Layout()
        self.real_communities = []
        self.algorithm_name = ""
        self.predicted_communities = []
        self.number_of_communities = 0
        self.runtime = 0.0
        self.shen_modularity = 0.0
        self.my_modularity = 0.0
        self.mgh_nmi = 0.0
        self.f_score = 0.0
        self.modularity = 0.0

    def __copy__(self):
        return Result()

    def set_dataset(self, dataset):
        self.dataset_name = dataset.name
        self.ig_graph = dataset.ig_graph
        self.layout = dataset.layout
        self.real_communities = dataset.real_communities

    def print_result(self):
        print(f"{self.dataset_name:<15}{self.algorithm_name:<17}{self.number_of_communities:<24}{self.runtime:<10}{self.shen_modularity:<18}{self.my_modularity:<16}{self.mgh_nmi:<10}{self.f_score:<10}{self.modularity:<10}")

def print_header():
    print("dataset_name   algorithm_name   number_of_communities   runtime   shen_modularity   my_modularity   mgh_nmi   f_score   modularity")

def select_algorithms(algorithm_keys): 
    for key in algorithm_keys: 
        if key in ALL_ALGORITHMS: 
            SELECTED_ALGORITHMS[key] = ALL_ALGORITHMS[key] 
        else:
            print(f"Algorithm key '{key}' not found in ALL_ALGORITHMS")
            
def select_all_algorithms():
    global SELECTED_ALGORITHMS
    SELECTED_ALGORITHMS = ALL_ALGORITHMS.copy()
    
class DatasetType(Enum):
    GROUND_TRUTH = "GroundTruth"
    WITHOUT_GROUND_TRUTH = "WithoutGroundTruth"
    LFR_BENCHMARK = "LFRbenchmark"

dataset_type_to_string = {
    DatasetType.GROUND_TRUTH: "GroundTruth",
    DatasetType.WITHOUT_GROUND_TRUTH: "WithoutGroundTruth",
    DatasetType.LFR_BENCHMARK: "LFRbenchmark"
}

def select_dataset_type(dataset_type):
    global SELECTED_DATASET_TYPE
    SELECTED_DATASET_TYPE = dataset_type

def get_selected_dataset_type():
    return dataset_type_to_string[SELECTED_DATASET_TYPE]
