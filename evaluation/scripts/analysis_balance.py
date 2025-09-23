import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def compute_balance(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, unique_solvers):
    """
    Method to create the data frame containing for each instance and each solver the calculated balance
    
    Parameters:
    - df: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - df_muToksia: subset of the dataframe df, containing only the rows of Mu-Toksia being the solver
    - key_answer: string to access the answer column
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - unique_instances: list of all instances in the data frame
    - unique_solvers: list of all solvers in the data frame
    
    Returns:
    - DataFrame containing for each instance and each solver the calculated balance
    """
    
    df_balance = pd.DataFrame(index=unique_instances, columns=unique_solvers)

    # Iterate through each solver
    for solverX in unique_solvers:

        # Filter out the rows of this solver
        solver_rows = df[df[key_solvers] == solverX]

        for _, rowX in solver_rows.iterrows():
            # set runtime of solver as negative number in the corresponding cell
            instanceX = rowX[key_instance]
            df_balance.loc[instanceX, solverX] = rowX[key_runtime]
            
            # Check if answer of the solver for this instance was NaN, if not add Mu-Toksia's runtime for this instance
            if pd.notna(rowX[key_answer]):
                # Find the corresponding instance solved by Mu_Toksia
                row_muToksia = df_muToksia[(df_muToksia[key_instance] == instanceX)]

                if not row_muToksia.empty:
                    # Add the runtime of Mu-Toksia
                    df_balance.loc[instanceX, solverX] -= row_muToksia.iloc[0][key_runtime]

    return df_balance


#---------------------------------------------------------------------------------------------------------------------------


def create_table_balance_sheet(df, key_answer, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_pct, title_balance, title_pct_change, title_resulting_sum_rt, title_solver_VBS, title_vbsCount, title_vbsCount_pct, delta_percentage):
    """
    Method to create a table visualizing a comparison of all solvers with the benchmark solver
    
    Parameters:
    - df: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - num_digits_pct: number of digits for the percentage values
    - title_balance: string used as a title for the column 'Balance'
    - title_pct_change: string used as a title for the column 'pct Change'
    - title_resulting_sum_rt: string used as a title for the column 'sum RT', describing the sum of RT if we add the balance and the sum RT of the benchmark solver
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - title_vbsCount: string used as a title for the column '#VBS'
    - title_vbsCount_pct: string ued as title for the colum '#VBS %'
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    
    Returns:
    - DataFrame visualizing a comparison of all solvers with the benchmark solver
    """

    # get list of the solvers, wihtout Mu-Toksia
    unique_solvers = sorted(df[key_solvers].unique().tolist())
    unique_solvers = [solver for solver in unique_solvers if solver != key_mutoksia]

    # get a list of all instances
    unique_instances = df[key_instance].unique()

    # get only those rows of Mu-Toksia
    df_muToksia = df[(df[key_solvers] == key_mutoksia)]
    df_muToksia = df_muToksia[[key_instance, key_runtime]]

    # compute a dataframe for each instance [rows] and each solver [columns] the calculated balance
    df_balance = compute_balance(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, unique_solvers)
    # add Mu-Toksia as a column with only '0' as entry, since it is compared to itself
    df_balance[key_mutoksia] = 0

    # compute the virtual best solver (VBS)
    df_balance = df_balance.astype('float64')
    res = compute_vbs_with_delta(df_balance, title_solver_VBS, True, delta_percentage)
    df_vbs  = res[0]
    df_contribution = res[1]

    # count the number of contributions to the VBS
    s_vbsCount = count_vbsContribution_with_delta(df_contribution)
    s_vbsCount.fillna(0).astype('int')
    num_vbs_total = df_contribution.shape[0]
    s_vbsCount_formatted = s_vbsCount.apply(lambda x: f"{x}/{num_vbs_total}")
    s_vbsCount_pct = s_vbsCount.apply(lambda x: f"{(x/num_vbs_total * 100):.{num_digits_pct}f}%")
    

    # calculate sum of runtime of Mu-Toksia for comparison
    df_muToksia = df_muToksia.drop(columns=[key_instance])
    df_muToksia = df_muToksia.sum()
    rt_sum_mutoksia = df_muToksia[key_runtime]

    # create the table
    df_table = pd.DataFrame()
    s_sum = df_vbs.sum()
    formatted_series_sum = s_sum.apply(lambda x: round(x))
    df_table[title_balance] = formatted_series_sum
    df_table[title_balance] = df_table[title_balance].astype('int')
    s_sum_resulting = (rt_sum_mutoksia + df_table[title_balance])
    formatted_series_sum_resulting = s_sum_resulting.apply(lambda x: round(x))
    df_table[title_resulting_sum_rt] = formatted_series_sum_resulting
    df_table[title_resulting_sum_rt] = df_table[title_resulting_sum_rt].astype('int')
    s_percentage = ((df_table[title_resulting_sum_rt] / rt_sum_mutoksia - 1) * 100)
    formatted_series_percentage = s_percentage.apply(lambda x: f"{round(x)}%")
    df_table[title_pct_change] = formatted_series_percentage
    df_table[title_vbsCount] = df_table.index.map(s_vbsCount_formatted)
    df_table[title_vbsCount_pct] = df_table.index.map(s_vbsCount_pct)

    # cleaning table data frame
    df_table.loc[title_solver_VBS, title_vbsCount] = ""
    df_table.loc[title_solver_VBS, title_vbsCount_pct] = ""
    
    return df_table
