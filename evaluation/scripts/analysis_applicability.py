import sys

import pandas as pd

# Method to create a table counting the answers of a given type for each solver
def create_table_number_answers(df_answers, dfrow_solution, dfrow_total_instances, key_answer, key_answerType, key_mutoksia, key_number_instances, key_percentage, key_solution):
    """
    Processes the answers, calculates percentages, and returns the updated DataFrame.
    
    Parameters:
    - df_answers: DataFrame containing the answers for each solver and benchmark
    - dfrow_solution: Row containing the number of NO-solutions
    - dfrow_total_instances: Row containing the total number of instances
    - key_answer: string to access the answer column
    - key_answerType: string containing 'NO' or 'YES' to indicate which answers are to be processed
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_number_instances: string to access the row of the total number of instances per benchmark dataset
    - key_percentage: string used as title for the new column to create
    - key_solution: string to access the row of answers from the solutions
    
    Returns:
    - df_answers_tmp: DataFrame with the number of answers for each solver, the total instances, and the percentages of answers found of the solver compared to the solution
    """
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