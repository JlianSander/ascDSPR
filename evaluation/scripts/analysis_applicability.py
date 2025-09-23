import sys
import pandas as pd

def count_answers(df_rawAnswered, key_answer, key_benchmarks, key_solvers):
    """
    Method to count the answers of each solver for each benchmark dataset
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_solvers: string to access the rows of a specific solver
    
    Returns:
    - DataFrame with the number of answers for each solver for each benchmark dataset
    """

    df_rawSolvBench = df_rawAnswered.groupby([key_solvers,key_benchmarks])
    df_answers = df_rawSolvBench[key_answer].value_counts().unstack(level=1)
    df_answers.index = df_answers.index.droplevel(key_answer)
    df_answers = df_answers.fillna(0).astype('int')
    return df_answers


#---------------------------------------------------------------------------------------------------------------------------


def create_table_number_answers(df_rawAnswered, dfrow_solution, key_answer, key_benchmarks, key_mutoksia, key_solution, key_solvers, title_percentage, title_total):
    """
    Method to create a table counting the answers of a given type for each solver
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - dfrow_solution: Row containing the number of NO-solutions
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_number_instances: string to access the row of the total number of instances per benchmark dataset
    - key_solution: string to access the row of answers from the solutions
    - key_solvers: string to access the rows of a specific solver
    - title_percentage: string used as title for the new column to create
    - title_total: string used as title for the new column to create
    
    Returns:
    - DataFrame with the number of answers for each solver, the total instances, and the percentages of answers found of the solver compared to the solution
    """

    # count answers for each solver and each benchmark
    df_answers_tmp = count_answers(df_rawAnswered, key_answer, key_benchmarks, key_solvers)
    
    # Reorder position of rows so that 'mu-toksia' is at the top
    dfrow_mu = df_answers_tmp.loc[[key_mutoksia]]
    df_answers_tmp = df_answers_tmp.drop(key_mutoksia)
    df_answers_tmp = pd.concat([df_answers_tmp, dfrow_mu])
    
    # Add row for total number of instances and row of the solutions to the dataframe
    df_answers_tmp = pd.concat([df_answers_tmp, dfrow_solution])
    df_answers_tmp = df_answers_tmp.fillna(0).astype('int')
    
    
    # Calculate the sum of the 'solution' row 
    solution_sum = df_answers_tmp.loc[key_solution].sum()
    
    # Add an empty column 'percentage'
    df_answers_tmp[title_total] = None
    df_answers_tmp[title_percentage] = None
    
    # Calculate the percentage for each row
    for index in df_answers_tmp.index:
        row_sum = df_answers_tmp.loc[index].sum()
        df_answers_tmp.loc[index, title_total] = row_sum
        percentage = (row_sum / solution_sum) * 100
        df_answers_tmp.loc[index, title_percentage] = percentage.round(0).astype('int').__str__() + "%"
    
    return df_answers_tmp 