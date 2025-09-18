import sys
import pandas as pd
import numpy as np

"""
    Based on work of Lars Bengel, published as: 
    Lars Bengel, Julian Sander, and Matthias Thimm. A reduct-based approach to skeptical
    preferred reasoning in abstract argumentation. In Proceedings of the 22th International 
    Conference on Principles of Knowledge Representation and Reasoning, KR 2025, 2025.
"""

#---------------------------------------------------------------------------------------------------------------------------

def compute_vbs(df_input: pd.DataFrame, key_contributor, key_VBS):
    df_output = df_input.copy()
    solvers = df_output.columns.tolist()
    df_output[key_contributor] = df_output.idxmin(axis=1)
    df_output[key_VBS] = df_output[solvers].min(axis=1)
    return df_output

#---------------------------------------------------------------------------------------------------------------------------

def count_vbsContribution(df_runtimes, key_contributor):
    s_vbsCount = df_runtimes[[key_contributor]].value_counts()
    s_vbsCount.index = s_vbsCount.index.map(lambda x: x[0])
    return s_vbsCount

#---------------------------------------------------------------------------------------------------------------------------

def limit_outliers(df_input, num_stdLimit):
    upper_limit = df_input.mean() + num_stdLimit * df_input.std()
    lower_limit = df_input.mean() - num_stdLimit * df_input.std()
    df_capped = df_input.where(df_input <= upper_limit, upper_limit, axis = 1).where(df_input >= lower_limit, lower_limit, axis = 1)
    return df_capped 

#---------------------------------------------------------------------------------------------------------------------------

def restructure_dataframe(df_input: pd.DataFrame, key_solvers, key_runtime):
    solvers = df_input[key_solvers].unique().tolist()
    df_structured = pd.DataFrame()
    for slv in solvers:
        view = df_input[df_input[key_solvers] == slv]
        df_structured[slv] = view[key_runtime].tolist()
    return df_structured

#---------------------------------------------------------------------------------------------------------------------------

def sanitize_dataframe(df_input: pd.DataFrame, key_exit_with_error, key_runtime, timeout: float) -> pd.DataFrame:
    df_output = df_input.copy()
    df_output.loc[df_output[key_runtime] > timeout, key_runtime] = timeout
    df_output.loc[df_output[key_exit_with_error] == True, key_runtime] = timeout
    return df_output