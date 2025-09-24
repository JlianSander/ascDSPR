import sys
import pandas as pd
import numpy as np


def populate_tab_overlap_int(df_overlap, s_rowSumsAnswers, key_solverPair_key, key_solverPair_value):
    """
    Method to create a table showing the overlap of the applicability between each solver as absolute number (integers)
    
    Parameters:
    - df_overlap: DataFrame of the number of overlapping solved instances for each possible pair of solvers
    - s_rowSumsAnswers: series listing the total number of answers given by each solver overall benchmark sets
    - key_solverPair_key: string to access the key values of the dictionary in df_overlap
    - key_solverPair_value: string to access the values of the dictionary in df_overlap
    
    Returns:
    - DataFrame showing the absolute (integer) overlap between the different solvers
    """

    # Extract unique solvers of interest
    unique_solvers = pd.Series(s_rowSumsAnswers.index)
    unique_solvers.name = None

    # Initialize a dataframe with solvers as columns and rows
    df_tabOverLap = pd.DataFrame(np.nan, index=unique_solvers, columns=unique_solvers)

    # Populate the result dataframe
    for _, row in df_overlap.iterrows():
        solver1, solver2 = row[key_solverPair_key]
        pair_count = row[key_solverPair_value]
        
        # Fill the values
        df_tabOverLap.at[solver1, solver2] = pair_count
        df_tabOverLap.at[solver2, solver1] = pair_count
        df_tabOverLap.at[solver1, solver1] = s_rowSumsAnswers[solver1]
        df_tabOverLap.at[solver2, solver2] = s_rowSumsAnswers[solver2]

    # convert to integers
    df_tabOverLap = df_tabOverLap.fillna(0).astype('int')
    return df_tabOverLap


#---------------------------------------------------------------------------------------------------------------------------


def populate_tab_overlap_string(df_overlap, s_rowSumsAnswers, key_solverPair_key, key_solverPair_value, num_digits_pct, suffix_percentage):
    """
    Method to create a table showing the overlap of the applicability between each solver as a formatted string
    
    Parameters:
    - df_overlap: DataFrame of the number of overlapping solved instances for each possible pair of solvers
    - s_rowSumsAnswers: series listing the total number of answers given by each solver overall benchmark sets
    - key_solverPair_key: string to access the key values of the dictionary in df_overlap
    - key_solverPair_value: string to access the values of the dictionary in df_overlap
    - num_digits_pct: number of digits for the percentage value
    - suffix_percentage: string to concatenate after solver name to title the column of percentage values
    
    Returns:
    - DataFrame showing the absolute (formatted string) overlap between the different solvers
    """

    # Extract unique solvers of interest
    unique_solvers = pd.Series(s_rowSumsAnswers.index)
    unique_solvers.name = None

    # Create an empty DataFrame with the required structure
    columns = []
    for item in unique_solvers:
        columns.append(item)         # Add the original columns
        columns.append(item + suffix_percentage)  # Add the percentage columns

    # Initialize the DataFrame with NaN values
    df_tabOverLap = pd.DataFrame(np.nan, index=unique_solvers, columns=columns).astype("string")

    # Populate the result dataframe
    for _, row in df_overlap.iterrows():
        solver1, solver2 = row[key_solverPair_key]
        pair_count = row[key_solverPair_value]

        # Fill the values
        df_tabOverLap.at[solver1, solver2] = pair_count.__str__() + '/' + s_rowSumsAnswers[solver2].__str__()
        pct_slv1 = pair_count /s_rowSumsAnswers[solver2] * 100
        df_tabOverLap.at[solver1, solver2 + suffix_percentage] = f"{pct_slv1:.{num_digits_pct}f}\%"
        df_tabOverLap.at[solver2, solver1] = pair_count.__str__() + '/' + s_rowSumsAnswers[solver1].__str__()
        pct_slv2 = pair_count / s_rowSumsAnswers[solver1] * 100
        df_tabOverLap.at[solver2, solver1 + suffix_percentage] = f"{pct_slv2:.{num_digits_pct}f}\%" 
        df_tabOverLap.at[solver1, solver1] = '-'
        df_tabOverLap.at[solver1, solver1 + suffix_percentage] = '-'
        df_tabOverLap.at[solver2, solver2] = '-'
        df_tabOverLap.at[solver2, solver2 + suffix_percentage] = '-'

    return df_tabOverLap


#---------------------------------------------------------------------------------------------------------------------------


def populate_tab_overlap_percentage(df_overlap, s_rowSumsAnswers, key_solverPair_key, key_solverPair_value):
    """
    Method to create a table showing the overlap of the applicability between each solver as percentage
    
    Parameters:
    - df_overlap: DataFrame of the number of overlapping solved instances for each possible pair of solvers
    - s_rowSumsAnswers: series listing the total number of answers given by each solver overall benchmark sets
    - key_solverPair_key: string to access the key values of the dictionary in df_overlap
    - key_solverPair_value: string to access the values of the dictionary in df_overlap
    
    Returns:
    - DataFrame showing the percentage overlap between the different solvers
    """

    # Extract unique solvers of interest
    unique_solvers = pd.Series(s_rowSumsAnswers.index)
    unique_solvers.name = None

    # Initialize a dataframe with solvers as columns and rows
    df_tabOverLap = pd.DataFrame(np.nan, index=unique_solvers, columns=unique_solvers)

    # Populate the result dataframe
    for _, row in df_overlap.iterrows():
        solver1, solver2 = row[key_solverPair_key]
        pair_count = row[key_solverPair_value]
        
        # Fill the values
        df_tabOverLap.at[solver1, solver2] = pair_count /s_rowSumsAnswers[solver2] * 100
        df_tabOverLap.at[solver2, solver1] = pair_count / s_rowSumsAnswers[solver1] * 100
        df_tabOverLap.at[solver1, solver1] = 100
        df_tabOverLap.at[solver2, solver2] = 100

    df_tabOverLap = df_tabOverLap.fillna(0).astype('float64')
    return df_tabOverLap