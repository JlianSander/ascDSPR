import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def create_table_runtime_intersection(df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_muToksia, key_runtime, key_solvers, timeout, num_stdLimit, show_capped,
                         title_solver_VBS, title_instances, title_mean, title_std, title_sum, title_meanCapped, title_stdCapped, title_sumCapped, title_vbsCount, delta_percentage):
    """
    Method to create a table visualizing the runtimes of all solvers for instances with the given answerType solution
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_mutoksia: string to access the rows of the benchmark-solver
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - timeout: number of seconds after which the calculation was aborted
    - num_stdLimit: number indicating how many times the standard deviation is add/substracted from the mean value to define a limit for outliers
    - show_capped: if 'True' the returned data frame contains columns for mean and std with capped values
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - title_instances: string used as a title for the column 'number_instances'
    - title_mean: string used as a title for the column 'mean RT'
    - title_std: string used as a title for the column 'std RT'
    - title_sum: string used as a title for the column 'sum RT'
    - title_meanCapped: string used as a title for the column 'mean RT capped'
    - title_stdCapped: string used as a title for the column 'std RT capped'
    - title_sumCapped: string used as a title for the column 'sum RT capped'
    - title_vbsCount: string used as a title for the column '#VBS'
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    
    Returns:
    - DataFrame visualizing the runtimes of all solvers for instances with the given answerType solution
    """

    key_VBS = title_solver_VBS

    # initialize output dataframe
    df_output = pd.DataFrame()

    # prepare data frame
    df_IntersectionAll = filter_intersection(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_solvers)
    df_IntersectionAll = df_IntersectionAll.astype({key_runtime: 'float'})
    df_IntersectionAllRunTime = sanitize_dataframe(df_IntersectionAll, key_exit_with_error, key_runtime, timeout)
    df_IntersectionAllRunTime = pivot_dataframe(df_IntersectionAllRunTime, key_solvers, key_runtime)
    df_IntersectionAllRunTime = df_IntersectionAllRunTime[[col for col in df_IntersectionAllRunTime.columns if col != key_muToksia] + [key_muToksia]]
    
    # compute the virtual best solver
    res = compute_vbs_with_delta(df_IntersectionAllRunTime, key_VBS, True, delta_percentage)
    df_IntersectionAllRunTimeVBS = res[0]
    df_contribution = res[1]

    # count contribution to the VBS
    s_vbsCount = count_vbsContribution_with_delta(df_contribution)

    # compute statistical values for each solver    
    df_output[title_instances] = df_IntersectionAllRunTimeVBS.count()
    df_output[title_mean] = df_IntersectionAllRunTimeVBS.mean()
    df_output[title_std] = df_IntersectionAllRunTimeVBS.std()
    df_output[title_sum] = df_IntersectionAllRunTimeVBS.sum()

    if(show_capped):
        df_IntersectionAllRunTimeVBSCapped = limit_outliers(df_IntersectionAllRunTimeVBS, num_stdLimit)
        df_output[title_meanCapped] = df_IntersectionAllRunTimeVBSCapped.mean()
        df_output[title_stdCapped] = df_IntersectionAllRunTimeVBSCapped.std()
        df_output[title_sumCapped] = df_IntersectionAllRunTimeVBSCapped.sum()

    df_output[title_vbsCount] = df_output.index.map(s_vbsCount)

    # cleaning output df of NaN values
    df_output[title_vbsCount] = df_output[title_vbsCount].fillna(0).astype('int')
    df_output.loc[key_VBS, title_vbsCount] = ""
    df_output = df_output.fillna(0)
    return df_output 