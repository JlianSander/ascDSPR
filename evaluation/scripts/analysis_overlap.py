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
    - DataFrame of the number of overlapping solved instances for each possible pair of solvers
    """

    # Get unique solver names
    unique_solvers = df_rawAnswered[key_solvers].unique()

    # Create an empty dictionary to store the results
    pair_counts = {}

    # Iterate over all unique pairs of solvers (solver_temp1, solver_temp2)
    for i, solver_temp1 in enumerate(unique_solvers):
        for solver_temp2 in unique_solvers[i+1:]:
            if(solver_temp2 == key_muToksia): continue

            # filter to keep only rows of instances solved by both solvers
            df_intersection = filter_intersection_pair(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_solvers, solver_temp1 , solver_temp2)  

            # filter to keep only rows solved by solver 1
            df_intersection = df_intersection[df_intersection[key_solvers] == solver_temp1]

            # Count the row for each benchmark data set and sum the number up
            group_sizes = df_intersection.groupby(key_benchmarks).size()
            num_rowsInstanceBoth = group_sizes.sum()
            
            # Store the result in the dictionary
            pair_counts[(solver_temp1, solver_temp2)] = num_rowsInstanceBoth

    # Convert the result to a DataFrame for easier readability
    pair_counts_df = pd.DataFrame(list(pair_counts.items()), columns=[key_solverPair_key, key_solverPair_value])
    return pair_counts_df


#---------------------------------------------------------------------------------------------------------------------------


def create_table_overlap(df_rawAnswered, key_answer, key_answerType, key_benchmarks, key_instance, key_muToksia, key_solvers, num_digits_pct, suffix_percentage, table_format):
    """
    Method to create a table showing the overlap of the applicability between each solver
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_answerType: string containing 'NO' or 'YES' to indicate which answers are to be processed
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_solvers: string to access the rows of a specific solver
    - num_digits_pct: number of digits for the percentage value
    - suffix_percentage: string to concatenate after solver name to title the column of percentage values
    
    Returns:
    - DataFrame showing the absolute and percentage overlap between the different solvers
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
    # # drop the answers of the benchmark solver
    # df_answers = df_answers.drop(index=df_answers[df_answers.index.get_level_values(key_solvers) == key_muToksia].index)

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
        return populate_tab_overlap_formatted(df_overlap, s_rowSumsAnswers, key_solverPair_key, key_solverPair_value, num_digits_pct, suffix_percentage)