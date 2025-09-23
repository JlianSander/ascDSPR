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

def compute_vbs(df_input: pd.DataFrame, key_contributor, key_VBS, search_for_min):
    """
    Method to compute the Virtual Best Solver (VBS)
    Parameters:
    - df_input: DataFrame containing for each solver a column and in each row the runtimes of the solvers
    - key_contributor: string to access column of contributors in the data frame of the VBS contributions
    - key_VBS: string used as a title for the column of the VBS solver
    - search_for_min: if 'True', then the best results are those minimal, otherwise the VBS is constitute of the maximum values
    
    Returns:
    - Data frame: [df_input][key_contributor][key_VBS] indicating which solver contributed to the VBS and the runtime of the VBS
    """

    df_output = df_input.copy()
    solvers = df_output.columns.tolist()

    print(df_input)

    if(search_for_min):
        df_output[key_contributor] = df_output.idxmin(axis=1)
        df_output[key_VBS] = df_output[solvers].min(axis=1)
    else:
        df_output[key_contributor] = df_output.idxmax(axis=1)
        df_output[key_VBS] = df_output[solvers].max(axis=1)

    print(df_output)
    return df_output

#---------------------------------------------------------------------------------------------------------------------------

def compute_vbs_with_delta(df_input: pd.DataFrame, key_VBS, search_for_min, delta_percentage):
    """
    Method to compute the Virtual Best Solver (VBS) with the given percentage delta
    Parameters:
    - df_input: DataFrame containing for each solver a column and in each row the runtimes of the solvers
    - key_VBS: string used as a title for the column of the VBS solver
    - search_for_min: if 'True', then the best results are those minimal, otherwise the VBS is constitute of the maximum values
    - delta_percentage: the percentage that defines the delta around the minimum (maximum) number, within which a values counts as contribution to the VBS
    
    Returns:
    - (df_runtime_incl_VBS, df_Contribution)
    df_Contribution: data frame indicating which solver contributed to the VBS and the runtime of the VBS
    df_runtime_incl_VBS: [df_input][runtime_VBS] concatenated the input data frame with a column for the runtime of the VBS
    """

    df_runtime_incl_VBS = df_input.copy()
    solvers = df_input.columns.tolist()

    if(search_for_min):
        df_runtime_incl_VBS[key_VBS] = df_runtime_incl_VBS[solvers].min(axis=1)
    else:
        df_runtime_incl_VBS[key_VBS] = df_runtime_incl_VBS[solvers].max(axis=1)

    # Function to check if value is within the range
    def is_in_range(value, vbs, delta_percentage):
        lower_bound = (1 - delta_percentage) * vbs
        upper_bound = (1 + delta_percentage) * vbs
        return lower_bound <= value <= upper_bound

    # Apply the function to each column of interest
    df_Contribution = df_runtime_incl_VBS[solvers].copy()

    for column in solvers:
        df_Contribution[column] = df_runtime_incl_VBS.apply(lambda row: is_in_range(row[column], row[key_VBS], delta_percentage), axis=1)

    return (df_runtime_incl_VBS, df_Contribution)

#---------------------------------------------------------------------------------------------------------------------------

def count_vbsContribution(df_runtimes, key_contributor):
    """
    Method to count the number of contributions to the Virtual Best Solver (VBS)
    Parameters:
    - df_runtimes: DataFrame containing a column accessible with 'key_contributor', that indicates in each row the contribution of one solver to the VBS
    - key_contributor: string to access column of contributors in the data frame of the VBS contributions
    
    Returns:
    - Series that is indexed by the name of the solvers. Each value describes the number of contributions to the VBS of that solver
    """

    s_vbsCount = df_runtimes[[key_contributor]].value_counts()
    s_vbsCount.index = s_vbsCount.index.map(lambda x: x[0])
    return s_vbsCount

#---------------------------------------------------------------------------------------------------------------------------

def count_vbsContribution_with_delta(df_contributions):
    """
    Method to count the number of contributions to the Virtual Best Solver (VBS)
    Parameters:
    - df_contributions: DataFrame indicating which solver contributed to the VBS
    
    Returns:
    - Series that is indexed by the name of the solvers. Each value describes the number of contributions to the VBS of that solver
    """

    s_vbsCount = df_contributions.sum()
    return s_vbsCount

#---------------------------------------------------------------------------------------------------------------------------

def limit_outliers(df_input, num_stdLimit):
    """
    Method to delete the extrem values, called outliers, of a dataframe. Limits for the values are maximum: [mean + num_stdLimit * \sigma] and minimum: [mean - num_stdLimit * \sigma]
    Parameters:
    - df_runtimes: a non-empty data frame, structure and number of rows and columns is not restricted
    - num_stdLimit: number indicating how many times the standard deviation is add/substracted from the mean value to define a limit for outliers
    
    Returns:
    - Data frame of the same structure than df_input, which values are capped to a maximum of [mean + num_stdLimit * \sigma] and a minimum of [mean - num_stdLimit * \sigma]
    """

    upper_limit = df_input.mean() + num_stdLimit * df_input.std()
    lower_limit = df_input.mean() - num_stdLimit * df_input.std()
    df_capped = df_input.where(df_input <= upper_limit, upper_limit, axis = 1).where(df_input >= lower_limit, lower_limit, axis = 1)
    return df_capped 

#---------------------------------------------------------------------------------------------------------------------------

def pivot_dataframe(df_input: pd.DataFrame, key_solvers, key_runtime):
    """
    Method to pivot a given dataframe, by making the unique values in 'key_solvers' the columns in the output data frame
    Parameters:
    - df_input: first column has to contain several similiar values in 'key_solvers', which serve as columns in the output data frame
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    
    Returns:
    - Data frame with the unique values of 'key_solvers' of the input data frame being the columns, values of the column 'key_runtime' are the rows under each associtated column
    """
    solvers = df_input[key_solvers].unique().tolist()
    df_pivoted = pd.DataFrame()
    for slv in solvers:
        view = df_input[df_input[key_solvers] == slv]
        df_pivoted[slv] = view[key_runtime].tolist()
    return df_pivoted

#---------------------------------------------------------------------------------------------------------------------------

def sanitize_dataframe(df_input: pd.DataFrame, key_exit_with_error, key_runtime, timeout: float) -> pd.DataFrame:
    """
    Method to overwrite any unrealistic runtime values
    Parameters:
    - df_input: data frame with a column 'key_runtime' and optionally with a column 'key_exit_with_error'
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - timeout: number of seconds after which the calculation was aborted
    
    Returns:
    - Dataframe with runtimes not above 'timeout'. Each row with an indicated 'exit_with_error' has the runtime 'timeout'
    """

    df_output = df_input.copy()
    df_output.loc[df_output[key_runtime] > timeout, key_runtime] = timeout

    if(key_exit_with_error in df_input.columns):
        df_output.loc[df_output[key_exit_with_error] == True, key_runtime] = timeout
    return df_output