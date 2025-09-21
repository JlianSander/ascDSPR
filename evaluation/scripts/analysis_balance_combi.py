import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *
from analysis_balance import *

def __compute_balance_combi(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, list_combination, title_combination):
    
    df_balance = pd.DataFrame([[0]], index = unique_instances, columns=[title_combination])

    # Iterate through each instance
    for instanceX in unique_instances:

        # Filter out the rows of this instance
        df_rows_instanceX = df[df[key_instance] == instanceX]
        
        for solverX in list_combination:
            # Filter out the rows of this solver
            rowX = df_rows_instanceX[df_rows_instanceX[key_solvers] == solverX]
            # set runtime of solver as negative number in the corresponding cell
            df_balance.loc[instanceX] = rowX[key_runtime]

            print(df_balance)
            return

    #     for _, rowX in solver_rows.iterrows():
    #         # set runtime of solver as negative number in the corresponding cell
    #         instanceX = rowX[key_instance]
    #         df_balance.loc[instanceX, solverX] = rowX[key_runtime]
            
    #         # Check if answer of the solver for this instance was NaN, if not add Mu-Toksia's runtime for this instance
    #         if pd.notna(rowX[key_answer]):
    #             # Find the corresponding instance solved by Mu_Toksia
    #             row_muToksia = df_muToksia[(df_muToksia[key_instance] == instanceX)]

    #             if not row_muToksia.empty:
    #                 # Add the runtime of Mu-Toksia
    #                 df_balance.loc[instanceX, solverX] -= row_muToksia.iloc[0][key_runtime]

    # return df_balance


def create_table_balance_sheet_combination(df, key_answer, key_instance, key_mutoksia, key_runtime, key_solvers, title_balance, title_pct_change, title_resulting_sum_rt, title_solver_VBS, title_vbsCount):
    list_combi = ('asc_01','asc_02')

    # get a list of all instances
    unique_instances = df[key_instance].unique()

    # get only those rows of Mu-Toksia
    df_muToksia = df[(df[key_solvers] == key_mutoksia)]
    df_muToksia = df_muToksia[[key_instance, key_runtime]]

    __compute_balance_combi(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, list_combi, 'asc_01/02')