import sys
import pandas as pd

def create_table_overlap(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_solvers, suffix_absolute, suffix_percentage):
    """
    Method to create a table showing the overlap of the applicability between each solver
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_solvers: string to access the rows of a specific solver
    - suffix_absolute: string to concatenate after solver name to title the column of absolute values
    - suffix_percentage: string to concatenate after solver name to title the column of percentage values
    
    Returns:
    - df_answers_tmp: DataFrame showing the absolute and percentage overlap between the different solvers
    """

    # Get unique solver names
    unique_solvers = df_rawAnswered[key_solvers].unique()

    # Create an empty dictionary to store the results
    pair_counts = {}

    # Iterate over all unique pairs of solvers (solver_temp1, solver_temp2)
    for i, solver_temp1 in enumerate(unique_solvers):
        for solver_temp2 in unique_solvers[i+1:]:
            # Filter the dataframe for rows where solver_name is either solver_temp1 or solver_temp2
            df_filtered = df_rawAnswered[df_rawAnswered[key_solvers].isin([solver_temp1, solver_temp2])]

            # prune data frame to contain only columns of interest
            df_pruned = df_filtered[[key_benchmarks, key_instance, key_solvers, key_answer]]
            df_pruned = df_pruned.groupby(['benchmark_name', 'instance', 'answer'])

            # Count the number of rows in each group
            counts = df_pruned.size()

            # Filter out groups with only one row (no pairs)
            # The result is a Series where the index is the group and the value is the count of rows
            s_pairs = counts[counts == 2]

            # Count the row for each benchmark data set and sum the number up
            group_sizes = s_pairs.groupby(level='benchmark_name').size()
            num_rowsInstanceBoth = group_sizes.sum()
            
            # Store the result in the dictionary
            pair_counts[(solver_temp1, solver_temp2)] = num_rowsInstanceBoth

    # Convert the result to a DataFrame for easier readability
    pair_counts_df = pd.DataFrame(list(pair_counts.items()), columns=['solver_pair', 'pair_count'])

    # Display the results
    print(pair_counts_df)#DEBUG