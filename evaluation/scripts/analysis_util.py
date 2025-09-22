import sys
import pandas as pd

"""
    Based on work of Lars Bengel, published as: 
    Lars Bengel, Julian Sander, and Matthias Thimm. A reduct-based approach to skeptical
    preferred reasoning in abstract argumentation. In Proceedings of the 22th International 
    Conference on Principles of Knowledge Representation and Reasoning, KR 2025, 2025.
"""

#---------------------------------------------------------------------------------------------------------------------------


def filter_by_answer(df_rawAnswered, key_answer, key_answerType):
    """
    Method to filter the given data frame to those rows with the given answerType as answer
    Parameters:
    - df_input: data frame with a column 'answer'
    - key_answer: string to access the answer column
    - key_answerType: string containing 'NO' or 'YES' to indicate which answers are to be processed
    
    Returns:
    - Data frame containing only those rows with the given answerType as answer
    """

    # filter to keep only rows with an answer similiar to the given answerType
    return df_rawAnswered[df_rawAnswered[key_answer] == key_answerType]

#---------------------------------------------------------------------------------------------------------------------------

def filter_intersection(df_input, key_benchmarks, key_instance, key_solvers):
    """
    Method to filter the given data frame to those rows which instance has been solved by all solvers
    Parameters:
    - df_input: data frame with columns 'key_solvers','key_benchmarks','key_instance'
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_solvers: string to access the rows of a specific solver
    
    Returns:
    - Data frame containing only those rows which instance has been solved by all solvers
    """

    # Create a set of unique pairs of ('benchmark_name', 'instance') for each 'solver_name'
    s_solvedInstances = df_input.groupby(key_solvers).apply(lambda x: set(zip(x[key_benchmarks], x[key_instance])))
    # get the list of solvers
    solvers = df_input[key_solvers].unique().tolist()

    # check for each row if the created pair of the row is contained in the dictionairies of all solvers
    def check_row(row):
        benchmark_instance_pair = (row[key_benchmarks], row[key_instance])
        for solver in solvers:
            if(benchmark_instance_pair not in s_solvedInstances[solver]):
                return False
        return True

    # Apply the filter function
    df_input.apply(check_row, axis=1)
    filtered_df = df_input[df_input.apply(check_row, axis=1)]
    return filtered_df

#---------------------------------------------------------------------------------------------------------------------------

def print_full(df_input):
    """
    Method to print all rows of the given data frame
    Parameters:
    - df_input: a nonempty data frame
    
    Returns:
    void
    """

    pd.set_option('display.max_rows', len(df_input))
    print(df_input)
    pd.reset_option('display.max_rows')

#---------------------------------------------------------------------------------------------------------------------------

# Function to replace 'asc_0x' with '\Sc{x}' for both index and columns
def replace_asc_labels(df, prefix_replacement):
    # Update index (row labels)
    df.index = df.index.to_series().replace(r'asc_0(\d)', rf'\\{prefix_replacement}{{\1}}', regex=True)
    df.index = df.index.to_series().replace(r'asc_(\d+)', rf'\\{prefix_replacement}{{\1}}', regex=True)
    
    # Update column names
    df.columns = df.columns.to_series().replace(r'asc_0(\d)', rf'\\{prefix_replacement}{{\1}}', regex=True)
    df.columns = df.columns.to_series().replace(r'asc_(\d+)', rf'\\{prefix_replacement}{{\1}}', regex=True)
    
    return df