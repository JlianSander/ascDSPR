import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *
from analysis_cascading_combi import *


def create_df_runtimes_combis_new(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, title_runtime, single_solvers, lists_cascading_solvers):
    # create output data frame
    df_runtimes = pd.DataFrame()

    for solver in single_solvers:
        cascading_solvers = (solver,)
        df_runtimes[cascading_solvers.__str__()] = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())

    for cascading_solvers in lists_cascading_solvers:
        df_runtimes[cascading_solvers.__str__()] = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())

    # calculate runtimes for only MuToksia
    cascading_solvers = (key_mutoksia,)
    df_runtimes[cascading_solvers.__str__()] = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())

    return df_runtimes


#---------------------------------------------------------------------------------------------------------------------------


def create_table_runtimes_combis_new(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_pct, title_balance, title_pct_change, title_runtime_sum, 
                                           title_solver_VBS, title_vbsCount, title_vbsCount_pct, delta_percentage,
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
    - num_digits_pct: number of digits for the percentage values
    - title_balance: string used as a title for the column 'Balance'
    - title_pct_change: string used as a title for the column 'pct Change'
    - title_runtime_sum: string used as a title for the column 'sum RT', describing the sum of RT if we add the balance and the sum RT of the benchmark solver
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - title_vbsCount: string used as a title for the column '#VBS'
    - title_vbsCount_pct: string ued as title for the colum '#VBS %'
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    - single_solvers: list of solvers, which are compared as singles with the benchmark solver
    - lists_cascading_solvers: a list of lists of solvers, each list of solvers describes a cascade of solvers, which are subsequently called to solve the problem
    
    Returns:
    - DataFrame visualizing a comparison of given single solvers and the given combinations of cascading solvers with the benchmark solver
    """

    df_runtimes = create_df_runtimes_combis_new(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, 'runtime', single_solvers, lists_cascading_solvers)

    return format_table_runtime_combis(df_runtimes, key_mutoksia, num_digits_pct, title_balance, title_pct_change, title_runtime_sum,
                                 title_solver_VBS, title_vbsCount, title_vbsCount_pct, delta_percentage)

    