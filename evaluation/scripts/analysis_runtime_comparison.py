import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *


def analyse_intersection(df_rawAnswered, key_benchmarks, key_contributor, key_exit_with_error, key_instance, key_runtime, key_solvers, list_solvers, timeout, title_VBS):
    
    # Filter the dataframe for rows where solver_name is either solver1 or solver2
    df_filtered = df_rawAnswered[df_rawAnswered[key_solvers].isin(list_solvers)]

    # keep only those rows which are in the intersection of solved rows by each of the two solvers
    df_intersection = filter_intersection(df_filtered, key_benchmarks, key_instance, key_solvers)
    df_intersection = df_intersection.loc[:, [key_solvers, key_runtime]]
    # # ------------- DEBUG ------------- 
    # df_intersection = df_intersection.loc[:, [key_solvers, key_instance, key_runtime]]
    # # ------------- DEBUG ------------- 

    # calculate VBS for this intersection
    df_intersectionVBS = df_intersection.astype({key_runtime: 'float'})
    df_intersectionVBS = sanitize_dataframe(df_intersectionVBS, key_exit_with_error, key_runtime, timeout)
    df_intersectionVBS = restructure_dataframe(df_intersectionVBS, key_solvers, key_runtime)
    df_intersectionVBS = compute_vbs(df_intersectionVBS, key_contributor, title_VBS)

    # count contribution to the VBS
    s_vbsCount = count_vbsContribution(df_intersectionVBS, key_contributor)
    s_vbsCount[title_VBS] = 0 

    # prepare dataframe to compute statistical values for each solver
    df_intersectionVBS = df_intersectionVBS.drop(columns=[key_contributor])

    # # ------------- DEBUG ------------- 
    # if(print_debug):
    #     print(df_intersectionVBS)
    # # ------------- DEBUG ------------- 

    if(df_intersectionVBS.empty):
        # # ------------- DEBUG -------------
        # print("Sovler1: " + solver1.__str__())
        # print("Sovler2: " + solver2.__str__())
        # # ------------- DEBUG -------------
        return ()
            
    # # ------------- DEBUG ------------- 
    # if(print_debug):
    #     print_full(df_intersectionVBS)
    # # ------------- DEBUG ------------- 

    # calculate mean and std values of the runtimes on these filtered instances
    df_runtimeMean = df_intersectionVBS.mean()
    df_runtimeStd = df_intersectionVBS.std()
    df_runtimeSum = df_intersectionVBS.sum()

    return (df_runtimeMean, df_runtimeStd, df_runtimeSum, s_vbsCount)

def fill_table(df_outputMean, df_outputMeanDiff, df_outputStd, df_outputSum, df_outputSumDiff, df_outputMeanSumPct, num_digits_std, df_runtimeMean, df_runtimeStd, df_runtimeSum, is_under_diagonale, solver1, solver2):
    # retrieve values
    mean_solver1 = df_runtimeMean.loc[solver1]
    mean_solver2 = df_runtimeMean.loc[solver2]
    mean_diff = mean_solver2 - mean_solver1
    std_solver1 = df_runtimeStd.loc[solver1]
    std_solver2 = df_runtimeStd.loc[solver2]
    sum_solver1 = df_runtimeSum.loc[solver1]
    sum_solver2 = df_runtimeSum.loc[solver2]
    sum_diff = sum_solver2 - sum_solver1
            

    # fill cells in data frame
    if(is_under_diagonale):
        df_outputMean[solver1][solver2] = f"{mean_solver2:.{num_digits_std}f}" + "/" + f"{mean_solver1:.{num_digits_std}f}"
        df_outputMeanDiff[solver1][solver2] = mean_diff
        df_outputStd[solver1][solver2] = f"{std_solver2:.{num_digits_std}f}" + "/" + f"{std_solver1:.{num_digits_std}f}"
        df_outputSum[solver1][solver2] = f"{sum_solver2:.{num_digits_std}f}" + "/" + f"{sum_solver1:.{num_digits_std}f}"
        df_outputSumDiff[solver1][solver2] = sum_diff
            
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

def create_table_runtime_comparison(df_rawAnswered, key_benchmarks, key_exit_with_error, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_std, timeout, title_VBS):
    solvers = sorted(df_rawAnswered[key_solvers].unique().tolist())
    
    key_contributor = 'contributor'

    # add VBS as index
    indexes = solvers.copy()
    indexes.append(title_VBS)

    ## ------------- DEBUG ------------- 
    # print(solvers)
    ## ------------- DEBUG ------------- 
    
    #initialize output dataframe
    df_outputMean = pd.DataFrame(index=indexes, columns=solvers)
    df_outputMeanDiff = pd.DataFrame(index=indexes, columns=solvers)
    df_outputMeanSumPct = pd.DataFrame(index=indexes, columns=solvers)
    df_outputStd = pd.DataFrame(index=indexes, columns=solvers)
    df_outputSum = pd.DataFrame(index=indexes, columns=solvers)
    df_outputSumDiff = pd.DataFrame(index=indexes, columns=solvers)

    for i, solver1 in enumerate(solvers):

        # ------------- DEBUG ------------- 
        print_debug = False
        if((solver1 == "asc_01")):
            print_debug = True
        # ------------- DEBUG ------------- 

        # analyse the set of problem instances solved by this solver
        list_solversForIntersection = [solver1]
        res = analyse_intersection(df_rawAnswered, key_benchmarks, key_contributor, key_exit_with_error, key_instance, key_runtime, key_solvers, list_solversForIntersection, timeout, title_VBS)
        df_runtimeMean = res[0]
        df_runtimeStd = res[1]
        df_runtimeSum = res[2]
        s_vbsCount = res[3]

        # ------------- DEBUG ------------- 
        if(print_debug):
            print(df_runtimeMean)
            print(df_runtimeStd)
            print(df_runtimeSum)
        # ------------- DEBUG -------------

        fill_table(df_outputMean, df_outputMeanDiff, df_outputStd, df_outputSum, df_outputSumDiff, df_outputMeanSumPct, num_digits_std, df_runtimeMean, df_runtimeStd, df_runtimeSum, True, solver1, title_VBS)

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
            res = analyse_intersection(df_rawAnswered, key_benchmarks, key_contributor, key_exit_with_error, key_instance, key_runtime, key_solvers, list_solversForIntersection, timeout, title_VBS)

            if(len(res) == 0):
                continue

            df_runtimeMean = res[0]
            df_runtimeStd = res[1]
            df_runtimeSum = res[2]
            s_vbsCount = res[3]            

            # # ------------- DEBUG ------------- 
            # if(print_debug):
            #     print(df_runtimeMean)
            #     print(df_runtimeStd)
            #     print(df_runtimeSum)
            #     return
            # # ------------- DEBUG ------------- 

            fill_table(df_outputMean, df_outputMeanDiff, df_outputStd, df_outputSum, df_outputSumDiff, df_outputMeanSumPct, num_digits_std, df_runtimeMean, df_runtimeStd, df_runtimeSum, is_under_diagonale, solver1, solver2)

            
    df_outputMean = df_outputMean.drop(columns=[key_mutoksia])
    df_outputMeanDiff = df_outputMeanDiff.drop(columns=[key_mutoksia])
    df_outputStd = df_outputStd.drop(columns=[key_mutoksia])
    df_outputSum = df_outputSum.drop(columns=[key_mutoksia])
    df_outputSumDiff = df_outputSumDiff.drop(columns=[key_mutoksia])

    df_outputMean = df_outputMean.fillna('')
    df_outputMeanDiff = df_outputMeanDiff.fillna('')
    df_outputMeanSumPct = df_outputMeanSumPct.fillna('')
    df_outputStd = df_outputStd.fillna('')
    df_outputSum = df_outputSum.fillna('')
    df_outputSumDiff = df_outputSumDiff.fillna('')
    
    ## ------------- DEBUG ------------- 
    # print(df_outputMean)
    # print(df_outputMeanSumPct)
    # print(df_outputStd)
    # print(df_outputSum)
    # print(df_outputSumDiff)
    ## ------------- DEBUG ------------- 


    return (df_outputMean, df_outputMeanDiff, df_outputMeanSumPct, df_outputStd, df_outputSum, df_outputSumDiff)