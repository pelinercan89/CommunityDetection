import my_globals, dataset_generator, reader, algorithm_executer, plotter, directory_manager
  
def main():         
    # Select a dataset
    # Test on synthetic networks
    # dataset_generator.create_test_set(5, 15, 3, 5, 0.8, 3, 2)  
    my_globals.select_dataset_type(my_globals.DatasetType.LFR_BENCHMARK)   
    # Test on real networks
    # my_globals.select_dataset_type(my_globals.DatasetType.GROUND_TRUTH)
    # Test on datasets without ground truth
    # my_globals.select_dataset_type(my_globals.DatasetType.WITHOUT_GROUND_TRUTH)
    
    # get the dataset
    datasets = reader.read_datasets()    

    # Select algorithms
    algorithm_keys_to_select = ["my", "ego_networks"] 
    # my_globals.select_algorithms(algorithm_keys_to_select)
    my_globals.select_all_algorithms()
    
    # Clean directory    
    directory_manager.clean_output_directory()
    # Create directory for results    
    directory_manager.create_directories()
    
    # Run algorşthm on datasets
    results = algorithm_executer.run_algorithms_on_datasets(datasets)
    
    # Plot graphs (Only call if the graphs are of a size that can be visually examined)
    plotter.plot_graphs(datasets, results)
    
    # Plot bar charts
    plotter.plot_data(results, datasets)
    
main()
