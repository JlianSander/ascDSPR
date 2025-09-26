import sys
import pandas as pd

from analysis_util import *

def extract_number_instances(df_iccmas, key_benchmarks, key_instance):
    """
    Method to extract the total number of instances per benchmark as a row
    
    Parameters:
    - df_iccmas: DataFrame containing the benchmark data
    - key_benchmarks: key to access the column indicating the benchmarks
    - key_instance: key to access the column indicating the instances
    
    Returns:
    - DataFrame containing a row of the total number of instances per benchmark
    """

    df_grouped_benchmarks = df_iccmas.groupby(key_benchmarks)
    s_total_instances = df_grouped_benchmarks.count()[key_instance]
    dfrow_num_instances = pd.DataFrame(s_total_instances).T  # .T transposes the series to match the row format
    return dfrow_num_instances


#---------------------------------------------------------------------------------------------------------------------------


def extract_solution_data(df_iccmas, key_answer, key_answerType, key_benchmarks, key_instance, indexName):
    """
    Method to extract the number of instances with a given answer for each benchmark as a row
    
    Parameters:
    - df_iccmas: DataFrame containing the benchmark data
    - key_answerType: String, either 'YES' or 'NO' to extract corresponding solution data
    - indexName: String, which is set as the index of the returned dataframe row
    
    Returns:
    - DataFrame containing the extracted solution data for the given type
    """

    df_filtered = filter_by_answer(df_iccmas, key_answer, key_answerType)
    df_row_number_instances = extract_number_instances(df_filtered, key_benchmarks, key_instance)
    df_row_number_instances.index = [indexName]
    return df_row_number_instances