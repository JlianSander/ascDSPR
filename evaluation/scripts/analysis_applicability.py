import sys

import pandas as pd

# Method to create a table counting the answers of a given type for each solver
def create_table_number_answers(df_rawAnswered, dfrow_solution, dfrow_total_instances, key_answer, key_answerType, key_benchmarks, key_mutoksia, key_number_instances, key_percentage, key_solution, key_solvers):
    """
    Processes the answers, calculates percentages, and returns the updated DataFrame.
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - dfrow_solution: Row containing the number of NO-solutions
    - dfrow_total_instances: Row containing the total number of instances
    - key_answer: string to access the answer column
    - key_answerType: string containing 'NO' or 'YES' to indicate which answers are to be processed
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_number_instances: string to access the row of the total number of instances per benchmark dataset
    - key_percentage: string used as title for the new column to create
    - key_solution: string to access the row of answers from the solutions
    - key_solvers: string to access the rows of a specific solver
    
    Returns:
    - df_answers_tmp: DataFrame with the number of answers for each solver, the total instances, and the percentages of answers found of the solver compared to the solution
    """

    # count answers for each solver and each benchmark
    df_rawSolvBench = df_rawAnswered.groupby([key_solvers,key_benchmarks])
    df_answers = df_rawSolvBench[key_answer].value_counts().unstack(level=1)
    df_answers = df_answers.fillna(0).astype('int')

    # Filter out only those rows with answer {key_answerType}
    df_answers_tmp = df_answers.xs(key_answerType, level=key_answer)
    
    # Reorder position of rows so that 'mu-toksia' is at the top
    dfrow_mu = df_answers_tmp.loc[[key_mutoksia]]
    df_answers_tmp = df_answers_tmp.drop(key_mutoksia)
    df_answers_tmp = pd.concat([dfrow_mu, df_answers_tmp])
    
    # Add row for total number of instances and row of the solutions to the dataframe
    df_answers_tmp = pd.concat([dfrow_solution, df_answers_tmp])
    df_answers_tmp = pd.concat([dfrow_total_instances, df_answers_tmp])
    
    # Calculate the sum of the 'solution' row 
    solution_sum = df_answers_tmp.loc[key_solution].sum()
    
    # Add an empty column 'percentage'
    df_answers_tmp[key_percentage] = None
    
    # Calculate the percentage for each row (except 'solution')
    for index in df_answers_tmp.index:
        if index != key_number_instances:
            row_sum = df_answers_tmp.loc[index].sum()
            percentage = (row_sum / solution_sum) * 100
            df_answers_tmp.loc[index, key_percentage] = percentage
    
    return df_answers_tmp 