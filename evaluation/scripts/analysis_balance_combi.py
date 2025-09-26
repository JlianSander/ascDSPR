import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *
from analysis_balance import *

def compute_balance_combi(df, df_muToksia, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_balance, title_combination):
    """
    Method to create a series containing for each instance, the balance of the given combination of cascading solvers
    
    Parameters:
    - df: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - df_muToksia: subset of the dataframe df, containing only the rows of Mu-Toksia being the solver
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - cascading_solvers: list of cascading solvers, which are subsequently called to solve the problem
    - title_balance: string used as a title for the column 'Balance'
    - title_combination: name of the combination of solvers
    
    Returns:
    - Series containing for each instance, the balance of the given combination of cascading solvers
    """


    df_balance = pd.DataFrame(columns=[key_solvers, key_benchmarks, key_instance, title_balance])

    combi = title_combination

    #counter_Prints = 0#DEBUG

    # iterate through benchmarks
    for benchmarkX in df[key_benchmarks].unique():
        
        # iterate through each instance of the benchmark
        for instanceX in df.loc[df[key_benchmarks] == benchmarkX, key_instance].unique():

            skip_successive_solvers = False

            # Filter out the rows of this instance in this benchmark
            df_rows_instanceX = df[(df[key_benchmarks] == benchmarkX) & (df[key_instance] == instanceX)]
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
                # check if there is already a corresponding cell in df_balance
                exists = ((df_balance[key_solvers] == combi) & (df_balance[key_benchmarks] == benchmarkX) & (df_balance[key_instance] == instanceX)).any()
                if(exists):
                    # add value to existing cell
                    df_balance.loc[(df_balance[key_solvers] == combi) & (df_balance[key_benchmarks] == benchmarkX) & (df_balance[key_instance] == instanceX), title_balance] += rowX.loc[0, key_runtime]
                else:
                    # add new row to data frame
                    new_row = pd.DataFrame({key_solvers: [combi], key_benchmarks: [benchmarkX], key_instance: [instanceX], title_balance: [rowX.loc[0, key_runtime]]})
                    df_balance = pd.concat([df_balance, new_row], ignore_index=True)

                # print_2 = df_balance.loc[instanceX].__str__()#DEBUG

                if pd.notna(rowX.loc[0, key_answer]):
                    # this solver solved the problem, therefore ignore all subsequent solvers
                    skip_successive_solvers = True

                    # Find the corresponding instance solved by Mu_Toksia
                    row_muToksia = df_muToksia[(df_muToksia[key_benchmarks] == benchmarkX) & (df_muToksia[key_instance] == instanceX)]

                    if not row_muToksia.empty:
                        # Subtract the runtime of Mu-Toksia
                        runtime_muToksia = row_muToksia.iloc[0][key_runtime]
                        df_balance.loc[(df_balance[key_solvers] == combi) & (df_balance[key_benchmarks] == benchmarkX) & (df_balance[key_instance] == instanceX), title_balance] -= runtime_muToksia
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

    df_balance_pivoted = df_balance.pivot_table(index=[key_benchmarks, key_instance], columns=key_solvers, values=title_balance)
    return df_balance_pivoted


#---------------------------------------------------------------------------------------------------------------------------


def create_table_balance_sheet_combination(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, title_balance, title_pct_change, title_resulting_sum_rt, 
                                           single_solvers, lists_cascading_solvers):
    """
    Method to create a table visualizing a comparison of given single solvers and the given combinations of cascading solvers with the benchmark solver
    
    Parameters:
    - df: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - title_balance: string used as a title for the column 'Balance'
    - title_pct_change: string used as a title for the column 'pct Change'
    - title_resulting_sum_rt: string used as a title for the column 'sum RT', describing the sum of RT if we add the balance and the sum RT of the benchmark solver
    - single_solvers: list of solvers, which are compared as singles with the benchmark solver
    - lists_cascading_solvers: a list of lists of solvers, each list of solvers describes a cascade of solvers, which are subsequently called to solve the problem
    
    Returns:
    - DataFrame visualizing a comparison of given single solvers and the given combinations of cascading solvers with the benchmark solver
    """

    # get a list of all instances
    unique_instances = df[key_instance].unique()

    # get only those rows of Mu-Toksia
    df_muToksia = df[(df[key_solvers] == key_mutoksia)]
    df_muToksia = df_muToksia[[key_benchmarks, key_instance, key_runtime]]

    # compute a dataframe of balances of the single solvers
    df_balance = compute_balance(df, df_muToksia, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, single_solvers, title_balance)

    # compute the balance for the combination of cascading solvers
    for cascading_solvers in lists_cascading_solvers:
        df_balance[cascading_solvers.__str__()] = compute_balance_combi(df, df_muToksia, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_balance, cascading_solvers.__str__())

    # add Mu-Toksia as a column with only '0' as entry, since it is compared to itself
    df_balance[key_mutoksia] = 0

    # calculate sum of runtime of Mu-Toksia for comparison
    df_muToksia = df_muToksia.drop(columns=[key_instance])
    df_muToksia = df_muToksia.sum()
    rt_sum_mutoksia = df_muToksia[key_runtime]

    # create the table
    df_table = pd.DataFrame()
    s_sum = df_balance.sum()
    formatted_series_sum = s_sum.apply(lambda x: round(x))
    df_table[title_balance] = formatted_series_sum
    df_table[title_balance] = df_table[title_balance].astype('int')
    s_sum_resulting = (rt_sum_mutoksia + df_table[title_balance])
    s_formatted_sum_resulting = s_sum_resulting.apply(lambda x: round(x))
    df_table[title_resulting_sum_rt] = s_formatted_sum_resulting
    df_table[title_resulting_sum_rt] = df_table[title_resulting_sum_rt].astype('int')
    s_percentage = (df_table[title_resulting_sum_rt] / rt_sum_mutoksia - 1) * 100
    formatted_series_percentage = s_percentage.apply(lambda x: f"{round(x)}\%")
    df_table[title_pct_change] = formatted_series_percentage

    return df_table
    