import sys
import pandas as pd
import numpy as np

from analysis_applicability import *
from analysis_overlap_tables import *

def calculate_overlap(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_muToksia, key_solvers, key_solverPair_key, key_solverPair_value):
    """
    Method to calculate the overlapping between the solvers, except the benchmark solver
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_solvers: string to access the rows of a specific solver
    
    Returns:
    - df_answers_tmp: DataFrame of the number of overlapping solved instances for each possible pair of solvers
    """

    # Get unique solver names
    unique_solvers = df_rawAnswered[key_solvers].unique()

    # Create an empty dictionary to store the results
    pair_counts = {}

    # Iterate over all unique pairs of solvers (solver_temp1, solver_temp2)
    for i, solver_temp1 in enumerate(unique_solvers):
        # filter out the benchmark solver
        if(solver_temp1 == key_muToksia): continue
        for solver_temp2 in unique_solvers[i+1:]:
            if(solver_temp2 == key_muToksia): continue
            # Filter the dataframe for rows where solver_name is either solver_temp1 or solver_temp2
            df_filtered = df_rawAnswered[df_rawAnswered[key_solvers].isin([solver_temp1, solver_temp2])]

            # prune data frame to contain only columns of interest
            df_pruned = df_filtered[[key_benchmarks, key_instance, key_solvers, key_answer]]
            df_pruned = df_pruned.groupby([key_benchmarks, key_instance, key_answer])

            # Count the number of rows in each group
            counts = df_pruned.size()

            # Filter out groups with only one row (no pairs)
            # The result is a Series where the index is the group and the value is the count of rows
            s_pairs = counts[counts == 2]

            # Count the row for each benchmark data set and sum the number up
            group_sizes = s_pairs.groupby(level=key_benchmarks).size()
            num_rowsInstanceBoth = group_sizes.sum()
            
            # Store the result in the dictionary
            pair_counts[(solver_temp1, solver_temp2)] = num_rowsInstanceBoth

    # Convert the result to a DataFrame for easier readability
    pair_counts_df = pd.DataFrame(list(pair_counts.items()), columns=[key_solverPair_key, key_solverPair_value])
    return pair_counts_df



def create_table_overlap(df_rawAnswered, key_answer, key_answerType, key_benchmarks, key_instance, key_muToksia, key_solvers, suffix_percentage, table_format):
    """
    Method to create a table showing the overlap of the applicability between each solver
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_answerType: string containing 'NO' or 'YES' to indicate which answers are to be processed
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_solvers: string to access the rows of a specific solver
    - suffix_percentage: string to concatenate after solver name to title the column of percentage values
    
    Returns:
    - df_answers_tmp: DataFrame showing the absolute and percentage overlap between the different solvers
    """

    key_solverPair_key = 'solver_pair'
    key_solverPair_value = 'pair_count'
    # filter to keep only rows with an answer similiar to the given answerType
    df_rawAnswered = df_rawAnswered[df_rawAnswered[key_answer] == key_answerType]
    # calculate the overlap
    df_overlap = calculate_overlap(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_muToksia, key_solvers, key_solverPair_key, key_solverPair_value)
    # count answers for each solver and each benchmark
    df_answers = count_answers(df_rawAnswered, key_answer, key_benchmarks, key_solvers)
    #df_answers = df_answers.xs(key_answerType, level=key_answer)
    # drop the answers of the benchmark solver
    df_answers = df_answers.drop(index=df_answers[df_answers.index.get_level_values(key_solvers) == key_muToksia].index)

    # sum up the number of answers over all benchmark datasets
    s_rowSumsAnswers = df_answers.sum(axis=1)
    s_rowSumsAnswers = s_rowSumsAnswers.groupby(key_solvers).first()


    #print(s_rowSumsAnswers)
    #print(" ")
    #print(" ")
    #print(df_overlap)  

    if(table_format == "INT"):
        return populate_tab_overlap_int(df_overlap, s_rowSumsAnswers, key_solverPair_key, key_solverPair_value)
    elif(table_format == "PCT"):
        return populate_tab_overlap_percentage(df_overlap, s_rowSumsAnswers, key_solverPair_key, key_solverPair_value)
    else:
        return populate_tab_overlap_string(df_overlap, s_rowSumsAnswers, key_solverPair_key, key_solverPair_value, suffix_percentage)