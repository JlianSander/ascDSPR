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
    # filter to keep only rows with an answer similiar to the given answerType
    return df_rawAnswered[df_rawAnswered[key_answer] == key_answerType]

#---------------------------------------------------------------------------------------------------------------------------

def filter_dataframe(df_input: pd.DataFrame, key_benchmarks, key_task, benchmark: str, problem: str):
    df_filtered = df_input[df_input[key_task] == problem]
    df_filtered = df_filtered[df_filtered[key_benchmarks] == benchmark]
    return df_filtered

#---------------------------------------------------------------------------------------------------------------------------

def filter_intersection(df_input, key_benchmarks, key_instance, key_solvers):
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

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')