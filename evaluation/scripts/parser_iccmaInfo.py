import sys
import pandas as pd

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