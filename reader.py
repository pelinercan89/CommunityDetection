import os
import networkx as nx
import igraph as ig
import my_globals, directory_manager

from networkx import convert_node_labels_to_integers

# Read a graph from a file and return both NetworkX and iGraph representations.
def read_graph(file_name):
    file_type = file_name.split(".")[1]

    if file_type == "gml":
        nxG = read_gml_graph(file_name)
    elif file_type in ["edgelist", "dat"]:
        nxG = read_edgelist_dat_graph(file_name, file_type)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    nxG = convert_node_labels_to_integers(nxG, first_label=0, ordering='default', label_attribute=None)
    igG = ig.Graph.from_networkx(nxG)

    return nxG, igG

# Read a GML graph file and return a NetworkX graph.
def read_gml_graph(file_name):
    return nx.read_gml(file_name, label="id")

# Read an edgelist or dat graph file and return a NetworkX graph.
def read_edgelist_dat_graph(file_name, file_type):
    nxG_edgelist = nx.read_edgelist(file_name, nodetype=int, data=(('weight', int),))
    nxG_edgelist = nx.relabel_nodes(nxG_edgelist, nx.get_node_attributes(nxG_edgelist, "id"))

    nxG = nx.Graph()
    nxG.add_nodes_from(range(len(nxG_edgelist.nodes())))
    nxG.add_edges_from(nxG_edgelist.edges())

    return nxG

# Read a graph from a file and return both NetworkX and iGraph representations along with the layout.
def read_graph_and_layout(directory):
    nx_graph, ig_graph = read_graph(directory)
    layout = ig_graph.layout("kk")
    return nx_graph, ig_graph, layout

# Read communities from a file.
def read_communities(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return eval(lines[0])

def read_datasets():
    directory = f"{directory_manager.PROJECT_DIRECTORY}/Data/{my_globals.dataset_type_to_string[my_globals.SELECTED_DATASET_TYPE]}"
    datasets = []
    
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
                    
            if file_name.endswith(".edgelist") or file_name.endswith(".gml"):
                dataset = my_globals.Dataset()
                dataset.directory = file_path
                dataset.name, _ = os.path.splitext(file_name)
                dataset.nx_graph, dataset.ig_graph, dataset.layout = read_graph_and_layout(dataset.directory) 
                          
                # Check if original communities file exists and read it                
                communities_file_path = os.path.splitext(file_path)[0] + ".dat"
                if os.path.exists(communities_file_path):
                    dataset.real_communities = read_communities(communities_file_path)

                datasets.append(dataset)
            
    return datasets


