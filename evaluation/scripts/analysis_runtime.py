import sys
import pandas as pd
import numpy as np

"""
    Based on work of Lars Bengel, published as: 
    Lars Bengel, Julian Sander, and Matthias Thimm. A reduct-based approach to skeptical
    preferred reasoning in abstract argumentation. In Proceedings of the 22th International 
    Conference on Principles of Knowledge Representation and Reasoning, KR 2025, 2025.
"""

def filter_dataframe(df_input: pd.DataFrame, key_benchmarks, key_task, benchmark: str, problem: str):
    df_filtered = df_input[df_input[key_task] == problem]
    df_filtered = df_filtered[df_filtered[key_benchmarks] == benchmark]
    return df_filtered

def restructure_dataframe(df_input: pd.DataFrame, key_solvers, key_runtime):
    solvers = df_input[key_solvers].unique().tolist()
    df_structured = pd.DataFrame()
    for slv in solvers:
        view = df_input[df_input[key_solvers] == slv]
        df_structured[slv] = view[key_runtime].tolist()
    return df_structured

def sanitize_dataframe(df_input: pd.DataFrame, key_exit_with_error, key_runtime, timeout: float) -> pd.DataFrame:
    df_output = df_input.copy()
    df_output.loc[df_output[key_runtime] > timeout, key_runtime] = timeout
    df_output.loc[df_output[key_exit_with_error] == True, key_runtime] = timeout
    return df_output

def compute_vbs(df_input: pd.DataFrame, key_contributor, key_VBS):
    df_output = df_input.copy()
    solvers = df_output.columns.tolist()
    df_output[key_contributor] = df_output.idxmin(axis=1)
    df_output[key_VBS] = df_output[solvers].min(axis=1)
    return df_output

def build_table(df_runtimes, key_contributor, key_VBS, timeout):
    table_data = []
    solvers = df_runtimes.columns.tolist()
    solvers.remove(key_contributor)
    rel_vbs = df_runtimes[df_runtimes[key_VBS] < timeout]

    for name in solvers:
        num_rows = len(df_runtimes[name])
        timeouts = df_runtimes[name].eq(timeout).sum()
        total_runtime = df_runtimes[name].sum() - (timeouts* timeout)
        par_10 = (df_runtimes[name].sum() + (1 * timeouts * timeout)) / num_rows
        
        if name != key_VBS:
            vbs = rel_vbs[key_contributor].value_counts().get(name, 0)
        else:
            vbs = "-"

        table_data.append([name, num_rows, timeouts, total_runtime, par_10, vbs])

    df_table = pd.DataFrame(table_data, columns=["Algorithm", "N", "#TO", "RT", "PAR10", "#"+key_VBS])

    df_table.sort_values(["#TO", "RT"], inplace=True)
    df_table.index = np.arange(1, len(df_table)+1)
    df_table.index.name = "No."
    df_table.reset_index(inplace=True)

    return df_table

def build_vbsCount(df_runtimes, key_contributor):
    s_vbsCount = df_runtimes[[key_contributor]].value_counts()
    return s_vbsCount

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

def limit_outliers(df_input, num_stdLimit):
    upper_limit = df_input.mean() + num_stdLimit * df_input.std()

    print(upper_limit)

    lower_limit = df_input.mean() - num_stdLimit * df_input.std()

    df_capped = df_input.where(df_input <= upper_limit, upper_limit, axis = 1).where(df_input >= lower_limit, lower_limit, axis = 1)
    return df_capped


def create_table_runtime(df_rawAnswered, key_answer, key_answerType, key_benchmarks, key_instance, key_runtime, key_solvers, key_task, key_exit_with_error, dataset, task, timeout, num_stdLimit):
    """
    Method to create a table visualizing the runtimes of all solvers for instances with the given answerType solution
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance 
    
    Returns:
    - df_answers_tmp: DataFrame visualizing the runtimes of all solvers for instances with the given answerType solution
    """

    key_contributor = 'contributor'
    key_VBS = 'VBS'

    # filter to keep only rows with an answer similiar to the given answerType
    df_rawAnswered = df_rawAnswered[df_rawAnswered[key_answer] == key_answerType]
    df_IntersectionAll = filter_intersection(df_rawAnswered, key_benchmarks, key_instance, key_solvers)
    df_IntersectionAll = df_IntersectionAll.astype({key_runtime: 'float'})
    df_IntersectionAllRunTime = sanitize_dataframe(df_IntersectionAll, key_exit_with_error, key_runtime, timeout)
    df_IntersectionAllRunTime = restructure_dataframe(df_IntersectionAllRunTime, key_solvers, key_runtime)
    
    # print(df_IntersectionAllRunTime)
    # print(df_IntersectionAllRunTime.mean())
    # print(df_IntersectionAllRunTime.std())
    # df_IntersectionAllRunTimeCapped = limit_outliers(df_IntersectionAllRunTime, num_stdLimit)
    # print(df_IntersectionAllRunTimeCapped)
    # print(df_IntersectionAllRunTimeCapped.mean())
    # print(df_IntersectionAllRunTimeCapped.std())

    df_runtimeVBS = compute_vbs(df_IntersectionAllRunTime, key_contributor, key_VBS)
    s_vbsCount = build_vbsCount(df_runtimeVBS, key_contributor)
    # print(s_vbsCount)
    
    
    
    #print(df_table)

