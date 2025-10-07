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

    # iterate through benchmarks
    for benchmarkX in df[key_benchmarks].unique():
        
        # iterate through each instance of the benchmark
        for instanceX in df.loc[df[key_benchmarks] == benchmarkX, key_instance].unique():

            skip_successive_solvers = False

            # Filter out the rows of this instance in this benchmark
            df_rows_instanceX = df[(df[key_benchmarks] == benchmarkX) & (df[key_instance] == instanceX)]

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

                if pd.notna(rowX.loc[0, key_answer]):
                    # this solver solved the problem, therefore ignore all subsequent solvers
                    skip_successive_solvers = True

    return df_runtimes


def create_df_runtimes_combis(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, title_runtime):
    # get list of the solvers
    unique_solvers = sorted(df[key_solvers].unique().tolist())
    # get a list wihtout Mu-Toksia
    unique_solvers_no_mu = [solver for solver in unique_solvers if solver != key_mutoksia]

    # create output data frame
    df_runtimes = pd.DataFrame()

    for solver in unique_solvers_no_mu:
        cascading_solvers = (solver, key_mutoksia)
        df_temp = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())
        df_runtimes[cascading_solvers.__str__()] = df_temp.pivot_table(index=[key_benchmarks, key_instance], columns=key_solvers, values=title_runtime)

    # calculate runtimes for only MuToksia
    cascading_solvers = (key_mutoksia,)
    df_temp = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())
    df_runtimes[cascading_solvers.__str__()] = df_temp.pivot_table(index=[key_benchmarks, key_instance], columns=key_solvers, values=title_runtime)

    return df_runtimes

#---------------------------------------------------------------------------------------------------------------------------


def format_table_runtime_combis(df_runtimes, key_mutoksia, num_digits_pct, num_digit_par, title_balance, title_pct_change, title_runtime_sum,
                                 title_solver_VBS, title_vbsCount, title_vbsCount_pct, title_num_to, title_par, delta_percentage, timeout, num_par_x, print_row_VBS):
    # compute the virtual best solver (VBS)
    df_runtimes = df_runtimes.astype('float64')
    res = compute_vbs_with_delta(df_runtimes, title_solver_VBS, True, delta_percentage)
    df_runtimes  = res[0]
    df_contribution = res[1]

    # count the number of contributions to the VBS
    s_vbsCount = count_vbsContribution_with_delta(df_contribution)
    s_vbsCount.fillna(0).astype('int')
    s_vbsCount_formatted = s_vbsCount.apply(lambda x: f"{x}")
    
    # create the table
    df_table = pd.DataFrame()
    s_sum = df_runtimes.sum()
    key_muToksia = (key_mutoksia,).__str__()
    sum_muToksia = s_sum[key_muToksia]
    formatted_series_sum = s_sum.apply(lambda x: round(x))
    df_table[title_runtime_sum] = formatted_series_sum.astype('float64')

    s_balance = df_table[title_runtime_sum] - sum_muToksia
    formatted_series_balance = s_balance.apply(lambda x: round(x))
    df_table[title_balance] = formatted_series_balance.astype('float64')

    # ensure that for all instances and solvers it holds that runtime <= timeout
    df_clipped = df_runtimes.clip(upper=timeout)
    s_count_to = (df_clipped >= timeout).sum().astype('int')
    df_table[title_num_to] = s_count_to

    # calculat the PAR score for each solver
    s_par_punishment = s_count_to * (num_par_x - 1) * timeout
    s_sum_par = df_clipped.sum() + s_par_punishment
    num_rows = df_clipped.shape[0]
    s_par_value = s_sum_par / num_rows
    formatted_series_par = s_par_value.apply(lambda x: f"{x:.{num_digit_par}f}")
    df_table[title_par] = formatted_series_par

    df_table[title_vbsCount] = df_table.index.map(s_vbsCount_formatted)

    if(print_row_VBS):
        df_table.loc[title_solver_VBS, title_vbsCount] = "-"
    else:
        df_table = df_table.drop(title_solver_VBS)

    return df_table

def create_table_runtimes_combis(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, 
                                 num_digits_pct, num_digit_par, 
                                 title_balance, title_pct_change, title_runtime_sum,
                                 title_solver_VBS, title_vbsCount, title_vbsCount_pct, title_num_to, title_par, delta_percentage, timeout, num_par_x, print_row_VBS):
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
    - num_digit_par: number of digits for the PAR values
    - title_balance: string used as a title for the column 'Balance'
    - title_pct_change: string used as a title for the column 'pct Change'
    - title_runtime_sum: string used as a title for the column 'sum RT', describing the sum of RT if we add the balance and the sum RT of the benchmark solver
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - title_vbsCount: string used as a title for the column '#VBS'
    - title_vbsCount_pct: string ued as title for the colum '#VBS %'
    - title_num_to: string ued as title for the colum '#TO'
    - title_par: string ued as title for the colum 'PARX'
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    - timeout: number of seconds after which the calculation was aborted
    - num_par_x: number of the par value e.G. 2 if PAR2 is used
    - print_row_VBS: if True than the row of the VBS gets shown in the table
    
    Returns:
    - DataFrame visualizing a comparison of all solvers with the benchmark solver
    """

    # calculate runtimes of cascading combinations
    df_runtimes = create_df_runtimes_combis(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, 'runtime')

    return format_table_runtime_combis(df_runtimes, key_mutoksia, num_digits_pct, num_digit_par, title_balance, title_pct_change, title_runtime_sum,
                                 title_solver_VBS, title_vbsCount, title_vbsCount_pct, title_num_to, title_par, delta_percentage, timeout, num_par_x, print_row_VBS)
