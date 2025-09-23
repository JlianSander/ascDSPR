import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *


def analyse_intersection(df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_runtime, key_solvers, list_solvers, timeout, title_solver_VBS, delta_percentage):
    """
    Method to compare the solvers runtimes on the intersection of their solved instances
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - list_solvers: list of solvers which runtimes are to be compared
    - timeout: number of seconds after which the calculation was aborted
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    
    Returns:
    (df_runtimeMean, df_runtimeStd, df_runtimeSum, s_vbsCount):
    - df_runtimeMean: data frame of the mean runtime values for the two solver of this comparison
    - df_runtimeStd: data frame of the standard deviation of the runtime values for the two solver of this comparison
    - df_runtimeSum: data frame of the sum of the runtime values for the two solver of this comparison
    - s_vbsCount: series of the number of contributions to the vbs for each solver of this comparison
    - num_total_instances_VBS: number of instances compared for the VBS
    """

    # Filter the dataframe for rows where solver_name is either solver1 or solver2
    df_filtered = df_rawAnswered[df_rawAnswered[key_solvers].isin(list_solvers)]

    # keep only those rows which are in the intersection of solved rows by each of the two solvers
    df_intersection = filter_intersection(df_filtered, key_answer, key_benchmarks, key_instance, key_solvers)
    df_intersection = df_intersection.loc[:, [key_solvers, key_runtime]] 

    # calculate VBS for this intersection
    df_intersectionVBS = df_intersection.astype({key_runtime: 'float'})
    df_intersectionVBS = sanitize_dataframe(df_intersectionVBS, key_exit_with_error, key_runtime, timeout)
    df_intersectionVBS = pivot_dataframe(df_intersectionVBS, key_solvers, key_runtime)
    res = compute_vbs_with_delta(df_intersectionVBS, title_solver_VBS, True, delta_percentage)
    
    df_intersectionVBS = res[0]
    df_contribution = res[1]

    # count contribution to the VBS
    s_vbsCount = count_vbsContribution_with_delta(df_contribution)
    num_total_instances_VBS = df_contribution.shape[0]

    if(df_intersectionVBS.empty):
        return ()

    # calculate mean and std values of the runtimes on these filtered instances
    df_runtimeMean = df_intersectionVBS.mean()
    df_runtimeStd = df_intersectionVBS.std()
    df_runtimeSum = df_intersectionVBS.sum()

    return (df_runtimeMean, df_runtimeStd, df_runtimeSum, s_vbsCount, num_total_instances_VBS)


#---------------------------------------------------------------------------------------------------------------------------


def __fill_table(df_outputMean, df_outputMeanDiff, df_outputMeanSumPct, df_outputStd, df_outputSum, df_outputSumDiff, df_outputVbsCount, num_digits_std, num_digits_sum, 
                 df_runtimeMean, df_runtimeStd, df_runtimeSum, s_vbsCount, num_total_instances_VBS,
                 is_under_diagonale, solver1, solver2):
    """
    Method to fill the table to visualize a pairwise comparison of the solvers runtimes on the intersection of their solved instances
    
    Parameters:
    - df_outputMean: OUTPUT data frame of the mean runtime for each solver in each pairwise comparison
    - df_outputMeanDiff: OUTPUT data frame of the differences between the mean runtime for each pairwise comparison of solvers
    - df_outputMeanSumPct: OUTPUT data frame of the percentage differences of the runtimes for each pairwise comparison of solvers
    - df_outputStd: OUTPUT data frame of the standard deviation for each solver in each pairwise comparison
    - df_outputSum: OUTPUT data frame of the sum of runtimes for each solver in each pairwise comparison
    - df_outputSumDiff: OUTPUT data frame of the differences between the sum of runtimes for each pairwise comparison of solvers
    - df_outputVbsCount: OUTPUT data frame of the number of contribution to the VBS for each solver in each pairwise comparison
    - num_digits_std: number indicating the number of digits displayed for the standard deviation
    - num_digits_sum: number indicating the number of digits displayed for the sum of runtime
    - df_runtimeMean: data frame of the mean runtime values for the two solver of this comparison
    - df_runtimeStd: data frame of the standard deviation of the runtime values for the two solver of this comparison
    - df_runtimeSum: data frame of the sum of the runtime values for the two solver of this comparison
    - s_vbsCount: series of the number of contributions to the vbs for each solver of this comparison
    - num_total_instances_VBS: number of instances compared for the VBS
    - is_under_diagonale: if 'True' the values are written under the diagonal of the table
    - solver1: first solver of this comparison
    - solver2: second solver of this comparison

    Returns:
    void
    """

    # retrieve values
    mean_solver1 = df_runtimeMean.loc[solver1]
    mean_solver2 = df_runtimeMean.loc[solver2]
    mean_diff = mean_solver2 - mean_solver1
    std_solver1 = df_runtimeStd.loc[solver1]
    std_solver2 = df_runtimeStd.loc[solver2]
    sum_solver1 = df_runtimeSum.loc[solver1]
    sum_solver2 = df_runtimeSum.loc[solver2]
    sum_diff = sum_solver2 - sum_solver1
    vbsCount_solver2 = s_vbsCount.loc[solver2]
    vbsCount_sum =  num_total_instances_VBS

    # fill cells in data frame
    if(is_under_diagonale):
        df_outputMean[solver1][solver2] = f"{mean_solver2:.{num_digits_std}f}" + "/" + f"{mean_solver1:.{num_digits_std}f}"
        df_outputMeanDiff[solver1][solver2] = mean_diff
        df_outputStd[solver1][solver2] = f"{std_solver2:.{num_digits_std}f}" + "/" + f"{std_solver1:.{num_digits_std}f}"
        df_outputSum[solver1][solver2] = f"{sum_solver2:.{num_digits_sum}f}" + "/" + f"{sum_solver1:.{num_digits_sum}f}"
        df_outputSumDiff[solver1][solver2] = sum_diff

    df_outputVbsCount[solver1][solver2] = vbsCount_solver2.__str__() + "/" + vbsCount_sum.__str__()     
    df_outputMeanSumPct[solver1][solver2] = (mean_solver2 / mean_solver1) * 100
            
    # # ------------- DEBUG ------------- 
    # if(print_debug):
    #     print(df_outputMean)
    #     print(df_outputMeanDiff)
    #     print(df_outputStd)
    #     print(df_outputSum)
    #     print(df_outputSumDiff)
    #     return
    # # ------------- DEBUG ------------- 


#---------------------------------------------------------------------------------------------------------------------------


def create_table_runtime_comparison(df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_std, num_digits_sum, timeout, title_solver_VBS, delta_percentage):
    """
    Method to create a table visualizing a pairwise comparison of the solvers runtimes on the intersection of their solved instances
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_solvers: string to access the rows of a specific solver
    - num_digits_std: number indicating the number of digits displayed for the standard deviation
    - num_digits_sum: number indicating the number of digits displayed for the sum of runtime
    - timeout: number of seconds after which the calculation was aborted
    - title_solver_VBS: string used as a title for the row of the VBS solver
    - delta_percentage: the percentage that defines the delta around the minimum runtime, within which a values counts as contribution to the VBS
    
    Returns:
    - DataFrame visualizing a pairwise comparison of the solvers runtimes on the intersection of their solved instances
    """

    solvers = sorted(df_rawAnswered[key_solvers].unique().tolist())

    ## ------------- DEBUG ------------- 
    # print(solvers)
    ## ------------- DEBUG ------------- 
    
    #initialize output dataframe
    df_outputMean = pd.DataFrame(index=solvers, columns=solvers)
    df_outputMeanDiff = pd.DataFrame(index=solvers, columns=solvers).astype('float64')
    df_outputMeanSumPct = pd.DataFrame(index=solvers, columns=solvers).astype('float64')
    df_outputStd = pd.DataFrame(index=solvers, columns=solvers)
    df_outputSum = pd.DataFrame(index=solvers, columns=solvers)
    df_outputSumDiff = pd.DataFrame(index=solvers, columns=solvers)
    df_outputVbsCount = pd.DataFrame(index=solvers, columns=solvers)

    for i, solver1 in enumerate(solvers):

        # ------------- DEBUG ------------- 
        print_debug = False
        if((solver1 == "asc_01")):
            print_debug = True
        # ------------- DEBUG ------------- 

        # analyse the intersections of solved problem instances with each of the other solvers
        for solver2 in solvers:
            if(solver1 == solver2):
                continue

            is_under_diagonale = solver2 in solvers[i+1:]

            # # ------------- DEBUG ------------- 
            # print_debug = False
            # if((solver2 == "asc_01")):
            #     print_debug = True
            # # ------------- DEBUG ------------- 

            list_solversForIntersection = [solver1, solver2]
            res = analyse_intersection(df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_runtime, key_solvers, list_solversForIntersection, timeout, title_solver_VBS, delta_percentage)

            if(len(res) == 0):
                continue

            df_runtimeMean = res[0]
            df_runtimeStd = res[1]
            df_runtimeSum = res[2]
            s_vbsCount = res[3]
            num_total_instances_VBS = res[4]        

            # # ------------- DEBUG ------------- 
            # if(print_debug):
            #     print(df_runtimeMean)
            #     print(df_runtimeStd)
            #     print(df_runtimeSum)
            #     print(s_vbsCount)
            #     return
            # # ------------- DEBUG ------------- 

            __fill_table(df_outputMean, df_outputMeanDiff, df_outputMeanSumPct, df_outputStd, df_outputSum, df_outputSumDiff, df_outputVbsCount, num_digits_std, num_digits_sum, 
                         df_runtimeMean, df_runtimeStd, df_runtimeSum, s_vbsCount, num_total_instances_VBS,
                         is_under_diagonale, solver1, solver2)

            
    df_outputMean = df_outputMean.drop(columns=[key_mutoksia])
    df_outputMeanDiff = df_outputMeanDiff.drop(columns=[key_mutoksia])
    df_outputStd = df_outputStd.drop(columns=[key_mutoksia])
    df_outputSum = df_outputSum.drop(columns=[key_mutoksia])
    df_outputSumDiff = df_outputSumDiff.drop(columns=[key_mutoksia])

    #df_outputMean = df_outputMean.fillna('')
    #df_outputMeanDiff = df_outputMeanDiff.fillna('')
    #df_outputMeanSumPct = df_outputMeanSumPct.fillna('')
    #df_outputStd = df_outputStd.fillna('')
    #df_outputSum = df_outputSum.fillna('')
    #df_outputSumDiff = df_outputSumDiff.fillna('')
    #df_outputVbsCount = df_outputVbsCount.fillna('')

    df_outputMeanSumPct = df_outputMeanSumPct.astype('float64')
    df_outputSumDiff = df_outputSumDiff.astype('float64')
    
    ## ------------- DEBUG ------------- 
    # print(df_outputMean)
    # print(df_outputMeanSumPct)
    # print(df_outputStd)
    # print(df_outputSum)
    # print(df_outputSumDiff)
    ## ------------- DEBUG ------------- 


    return (df_outputMean, df_outputMeanDiff, df_outputMeanSumPct, df_outputStd, df_outputSum, df_outputSumDiff, df_outputVbsCount)