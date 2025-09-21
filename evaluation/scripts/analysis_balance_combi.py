import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *
from analysis_balance import *

def compute_balance_combi(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, cascading_solvers, title_combination):
    
    df_balance = pd.DataFrame([[0]], index = unique_instances, columns=[title_combination])

    #counter_Prints = 0#DEBUG

    # Iterate through each instance
    for instanceX in unique_instances:

        skip_successive_solvers = False

        # Filter out the rows of this instance
        df_rows_instanceX = df[df[key_instance] == instanceX]
        # print("--- new instance ---")#DEBUG
        # print_debug = False#DEBUG
        # print_1 = "NaN"#DEBUG
        # print_2 = "NaN"#DEBUG
        # print_3 = "NaN"#DEBUG
        # print_1 = df_balance.loc[instanceX].__str__()#DEBUG
        for solverX in cascading_solvers:

            # if the problem was already solved by preceding solver, then the runtime of this does not need to be accounted
            if(skip_successive_solvers):
                continue

            # Filter out the rows of this solver
            rowX = df_rows_instanceX[df_rows_instanceX[key_solvers] == solverX]
            rowX = rowX.reset_index()
            # set runtime of solver as negative number in the corresponding cell
            df_balance.loc[instanceX] += rowX.loc[0, key_runtime]
            # print_2 = df_balance.loc[instanceX].__str__()#DEBUG

            if pd.notna(rowX.loc[0, key_answer]):
                # this solver solved the problem, therefore ignore all subsequent solvers
                skip_successive_solvers = True

                # Find the corresponding instance solved by Mu_Toksia
                row_muToksia = df_muToksia[(df_muToksia[key_instance] == instanceX)]

                if not row_muToksia.empty:
                    # Add the runtime of Mu-Toksia
                    runtime_muToksia = row_muToksia.iloc[0][key_runtime]
                    df_balance.loc[instanceX] -= runtime_muToksia 
                    # print_3 = df_balance.loc[instanceX].__str__()#DEBUG
                    # if(print_debug):#DEBUG
                    #     counter_Prints += 1#DEBUG
        #     else:#DEBUG
        #         print_debug = True#DEBUG

        #     if(print_debug):#DEBUG
        #         print(print_1)#DEBUG
        #         print(print_2)#DEBUG
        #         print(print_3)#DEBUG

        # if(counter_Prints > 4):#DEBUG
        #     return#DEBUG

    return df_balance

def create_table_balance_sheet_combination(df, key_answer, key_instance, key_mutoksia, key_runtime, key_solvers, title_balance, title_pct_change, title_resulting_sum_rt, title_solver_VBS, title_vbsCount, cascading_solvers):
    

    # get a list of all instances
    unique_instances = df[key_instance].unique()

    # get only those rows of Mu-Toksia
    df_muToksia = df[(df[key_solvers] == key_mutoksia)]
    df_muToksia = df_muToksia[[key_instance, key_runtime]]

    df_balance = create_table_balance_sheet(df, key_answer, key_instance, key_mutoksia, key_runtime, key_solvers, title_balance, title_pct_change, title_resulting_sum_rt, title_solver_VBS, title_vbsCount)

    df_balance[cascading_solvers.__str__()] = compute_balance_combi(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, cascading_solvers, cascading_solvers.__str__())


    return df_balance
    