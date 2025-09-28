import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, title_combination):
    """
    Method to create a series containing for each benchmark and instance, the runtime of the given combination of cascading solvers
    
    Parameters:
    - df: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - cascading_solvers: list of cascading solvers, which are subsequently called to solve the problem
    - title_runtime: string used as a title for the column 'runtime'
    - title_combination: name of the combination of solvers
    
    Returns:
    - Series containing for each instance, the runtime of the given combination of cascading solvers
    """


    df_runtimes = pd.DataFrame(columns=[key_solvers, key_benchmarks, key_instance, title_runtime])

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
            # print_1 = df_runtimes.loc[instanceX].__str__()#DEBUG
            for solverX in cascading_solvers:

                # if the problem was already solved by preceding solver, then the runtime of this does not need to be accounted
                if(skip_successive_solvers):
                    continue

                # Filter out the rows of this solver
                rowX = df_rows_instanceX[df_rows_instanceX[key_solvers] == solverX]
                rowX = rowX.reset_index()
                # check if there is already a corresponding cell in df_runtimes
                exists = ((df_runtimes[key_solvers] == combi) & (df_runtimes[key_benchmarks] == benchmarkX) & (df_runtimes[key_instance] == instanceX)).any()
                if(exists):
                    # add value to existing cell
                    df_runtimes.loc[(df_runtimes[key_solvers] == combi) & (df_runtimes[key_benchmarks] == benchmarkX) & (df_runtimes[key_instance] == instanceX), title_runtime] += rowX.loc[0, key_runtime]
                else:
                    # add new row to data frame
                    new_row = pd.DataFrame({key_solvers: [combi], key_benchmarks: [benchmarkX], key_instance: [instanceX], title_runtime: [rowX.loc[0, key_runtime]]})
                    df_runtimes = pd.concat([df_runtimes, new_row], ignore_index=True)

                # print_2 = df_runtimes.loc[instanceX].__str__()#DEBUG

                if pd.notna(rowX.loc[0, key_answer]):
                    # this solver solved the problem, therefore ignore all subsequent solvers
                    skip_successive_solvers = True

            #     else:#DEBUG
            #         print_debug = True#DEBUG

            #     if(print_debug):#DEBUG
            #         print(print_1)#DEBUG
            #         print(print_2)#DEBUG
            #         print(print_3)#DEBUG

            # if(counter_Prints > 4):#DEBUG
            #     return#DEBUG

    df_runtimes_pivoted = df_runtimes.pivot_table(index=[key_benchmarks, key_instance], columns=key_solvers, values=title_runtime)
    return df_runtimes_pivoted


def create_df_runtimes_combis(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, title_runtime):
    # get list of the solvers
    unique_solvers = sorted(df[key_solvers].unique().tolist())
    # get a list wihtout Mu-Toksia
    unique_solvers_no_mu = [solver for solver in unique_solvers if solver != key_mutoksia]

    # create output data frame
    df_runtimes = pd.DataFrame()

    for solver in unique_solvers_no_mu:
        cascading_solvers = [solver, key_mutoksia]
        df_runtimes[cascading_solvers.__str__()] = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())

    # calculate runtimes for only MuToksia
    cascading_solvers = [key_mutoksia]
    df_runtimes[cascading_solvers.__str__()] = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())

    return df_runtimes

#---------------------------------------------------------------------------------------------------------------------------


def create_table_runtimes_combis(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_pct, title_balance, title_pct_change, title_runtime_sum,
                                 title_solver_VBS, title_vbsCount, title_vbsCount_pct, delta_percentage):
    """
    Method to create a table visualizing a comparison of all solvers with the benchmark solver
    
    Parameters:
    - df: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - num_digits_pct: number of digits for the percentage values
    - title_balance: string used as a title for the column 'Balance'
    - title_pct_change: string used as a title for the column 'pct Change'
    - title_runtime_sum: string used as a title for the column 'sum RT', describing the sum of RT if we add the balance and the sum RT of the benchmark solver
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - title_vbsCount: string used as a title for the column '#VBS'
    - title_vbsCount_pct: string ued as title for the colum '#VBS %'
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    
    Returns:
    - DataFrame visualizing a comparison of all solvers with the benchmark solver
    """

    # create output data frame
    df_runtimes = create_df_runtimes_combis(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, 'runtime')

    # compute the virtual best solver (VBS)
    df_runtimes = df_runtimes.astype('float64')
    res = compute_vbs_with_delta(df_runtimes, title_solver_VBS, True, delta_percentage)
    df_vbs  = res[0]
    df_contribution = res[1]

    # count the number of contributions to the VBS
    s_vbsCount = count_vbsContribution_with_delta(df_contribution)
    s_vbsCount.fillna(0).astype('int')
    num_vbs_total = df_contribution.shape[0]
    s_vbsCount_formatted = s_vbsCount.apply(lambda x: f"{x}/{num_vbs_total}")
    s_vbsCount_pct = s_vbsCount.apply(lambda x: f"{(x/num_vbs_total * 100):.{num_digits_pct}f}\%")
    
    # create the table
    df_table = pd.DataFrame()
    s_sum = df_vbs.sum()
    key_muToksia = [key_mutoksia].__str__()
    sum_muToksia = s_sum[key_muToksia]
    formatted_series_sum = s_sum.apply(lambda x: round(x))
    df_table[title_runtime_sum] = formatted_series_sum
    df_table[title_runtime_sum] = df_table[title_runtime_sum].astype('int')

    s_balance = df_table[title_runtime_sum] - sum_muToksia
    formatted_series_balance = s_balance.apply(lambda x: round(x))
    df_table[title_balance] = formatted_series_balance
    
    s_percentage = ((df_table[title_balance] / sum_muToksia) * 100)
    formatted_series_percentage = s_percentage.apply(lambda x: f"{round(x)}\%")
    df_table[title_pct_change] = formatted_series_percentage
    df_table[title_vbsCount] = df_table.index.map(s_vbsCount_formatted)
    df_table[title_vbsCount_pct] = df_table.index.map(s_vbsCount_pct)

    # cleaning table data frame
    df_table.loc[title_solver_VBS, title_vbsCount] = ""
    df_table.loc[title_solver_VBS, title_vbsCount_pct] = ""
    
    return df_table
