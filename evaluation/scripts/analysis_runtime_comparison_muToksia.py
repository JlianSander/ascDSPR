import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *
from analysis_runtime_comparison import *

#---------------------------------------------------------------------------------------------------------------------------

def __fill_table(df_output, df_runtimeSum, num_digits_pct, num_digits_sum, 
                  key_mutoksia, s_vbsCount, solver1, 
                  title_colmn_insts, title_colmn_rt_muToksia, title_column_sum, title_column_sum_pct, title_colum_vbs, title_column_vbsCount_pct, num_total_instances):
    """
    Method to fill the table to visualize a pairwise comparison of the solvers runtimes on the intersection of their solved instances
    
    Parameters:
    - df_output: OUTPUT data frame of the comparison
    - num_digits_pct: number indicating the number of digits displayed for the percentage
    - num_digits_sum: number indicating the number of digits displayed for the sum of runtime
    - df_runtimeSum: data frame of the sum of the runtime values for the two solver of this comparison
    - s_vbsCount: series of the number of contributions to the vbs for each solver of this comparison
    - solver1: first solver of this comparison
    - key_mutoksia: string to access the benchmark-solver
    - title_colmn_insts: string used as a title for the column '# instances'
    - title_colmn_rt_muToksia: string used as a title for the column 'RT MuToksia'
    - title_column_sum: string used as a title for the column 'sum'
    - title_column_sum_pct: string used as a title for the column 'sum %'
    - title_colum_vbs: string used as a title for the column '#VBS'
    - title_column_vbsCount_pct: string used as a title for the column '#VBS %'
    - num_total_instances: total number of instances of the comparison

    Returns:
    void
    """

    # retrieve values
    sum_solver1 = df_runtimeSum.loc[solver1]
    sum_muToksia = df_runtimeSum.loc[key_mutoksia]
    sum_pct = (sum_solver1 / sum_muToksia) * 100
    vbsCount_solver1 = s_vbsCount.loc[solver1]
    
    vbsCount_sum = num_total_instances
    vbsCount_pct = (vbsCount_solver1 / vbsCount_sum) * 100

    # fill the cells of the table
    df_output[title_colmn_insts][solver1] = num_total_instances
    df_output[title_column_sum][solver1] = f"{sum_solver1:.{num_digits_sum}f}"
    df_output[title_colmn_rt_muToksia][solver1] = f"{sum_muToksia:.{num_digits_sum}f}"
    df_output[title_column_sum_pct][solver1] = f"{sum_pct:.{num_digits_pct}f}\%"
    df_output[title_colum_vbs][solver1] = vbsCount_solver1
    df_output[title_column_vbsCount_pct][solver1] = f"{vbsCount_pct:.{num_digits_pct}f}\%" 


#---------------------------------------------------------------------------------------------------------------------------


def create_table_runtime_comparison_mutoksia(df_input, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_pct, num_digits_sum, timeout, 
                                             title_colmn_insts, title_colmn_rt_muToksia, title_solver_VBS, title_column_sum, title_column_sum_pct, title_colum_vbs, title_column_vbsCount_pct, delta_percentage):
    """
    Method to create a table visualizing a pairwise comparison of the runtimes of each solver with the benchmark solver on the intersection of their solved instances
    
    Parameters:
    - df_input: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_mutoksia: string to access the benchmark-solver
    - key_solvers: string to access the rows of a specific solver
    - num_digits_pct: number indicating the number of digits displayed for the percentage
    - num_digits_sum: number indicating the number of digits displayed for the sum of runtime
    - timeout: number of seconds after which the calculation was aborted
    - title_colmn_insts: string used as a title for the column '# instances'
    - title_colmn_rt_muToksia: string used as a title for the column 'RT MuToksia'
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - title_column_sum: string used as a title for the column 'sum'
    - title_column_sum_pct: string used as a title for the column 'sum %'
    - title_colum_vbs: string used as a title for the column '#VBS'
    - title_column_vbsCount_pct: string used as a title for the column '#VBS %'
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    
    Returns:
    - DataFrame visualizing a pairwise comparison of the runtimes of each solver with the benchmark solver on the intersection of their solved instances
    """

    key_contributor = 'contributor'
    # get list of the solvers, wihtout Mu-Toksia
    solvers = sorted(df_input[key_solvers].unique().tolist())
    solvers = [solver for solver in solvers if solver != key_mutoksia]

    #initialize output dataframe
    df_output = pd.DataFrame(index=solvers, columns=[title_colmn_insts, title_colmn_rt_muToksia, title_column_sum, title_column_sum_pct, title_colum_vbs, title_column_vbsCount_pct]) 

    # analyse the intersections of solved problem instances with each of the solvers
    for solver1 in solvers:
        list_solversForIntersection = [solver1, key_mutoksia]
        res = analyse_intersection(df_input, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_runtime, key_solvers, list_solversForIntersection, timeout, title_solver_VBS, delta_percentage)

        if(len(res) == 0):
            continue

        df_runtimeSum = res[2]
        s_vbsCount = res[3]
        num_total_instances = res[4]

        __fill_table(df_output, df_runtimeSum, num_digits_pct, num_digits_sum, 
                  key_mutoksia, s_vbsCount, solver1, 
                  title_colmn_insts, title_colmn_rt_muToksia, title_column_sum, title_column_sum_pct, title_colum_vbs, title_column_vbsCount_pct, num_total_instances)

    return df_output