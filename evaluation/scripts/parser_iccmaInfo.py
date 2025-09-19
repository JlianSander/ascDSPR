import sys
import pandas as pd

def extract_total_number_instances(df_iccmas, keyColumn):
    """
    Method to extract the total number of instances per benchmark as a row
    
    Parameters:
    - df_iccmas: DataFrame containing the benchmark data
    
    Returns:
    - DataFrame containing a row of the total number of instances per benchmark
    """

    s_total_instances = df_iccmas[keyColumn]
    dfrow_num_instances = pd.DataFrame(s_total_instances).T  # .T transposes the series to match the row format
    return dfrow_num_instances

def extract_solution_data(df_iccmas, key_answerType, indexName):
    """
    Method to extract the number of instances with a given answer for each benchmark as a row
    
    Parameters:
    - df_iccmas: DataFrame containing the benchmark data
    - key_answerType: String, either 'YES' or 'NO' to extract corresponding solution data
    - indexName: String, which is set as the index of the returned dataframe row
    
    Returns:
    - DataFrame containing the extracted solution data for the given type
    """
    
    s_solution = df_iccmas[key_answerType]
    dfrow_solution = pd.DataFrame(s_solution).T  # .T transposes the series to match the row format
    dfrow_solution.index = [indexName]
    
    return dfrow_solution