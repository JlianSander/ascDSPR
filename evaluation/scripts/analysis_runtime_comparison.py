import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def create_table_runtime_comparison(df_rawAnswered, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_std):
    solvers = sorted(df_rawAnswered[key_solvers].unique().tolist())
    
    ## ------------- DEBUG ------------- 
    # print(solvers)
    ## ------------- DEBUG ------------- 
    
    #initialize output dataframe
    df_outputMean = pd.DataFrame(index=solvers, columns=solvers)
    df_outputMeanDiff = pd.DataFrame(index=solvers, columns=solvers)
    df_outputMeanSumPct = pd.DataFrame(index=solvers, columns=solvers)
    df_outputStd = pd.DataFrame(index=solvers, columns=solvers)
    df_outputSum = pd.DataFrame(index=solvers, columns=solvers)
    df_outputSumDiff = pd.DataFrame(index=solvers, columns=solvers)

    for i, solver1 in enumerate(solvers):
        for solver2 in solvers:
            if(solver1 == solver2):
                continue

            is_under_diagonale = solver2 in solvers[i+1:]

            # # ------------- DEBUG ------------- 
            # print_debug = False
            # if((solver2 == "asc_02")):
            #     print_debug = True
            # # ------------- DEBUG ------------- 

            # Filter the dataframe for rows where solver_name is either solver_temp1 or solver_temp2
            df_filtered = df_rawAnswered[df_rawAnswered[key_solvers].isin([solver1, solver2])]

            # keep only those rows which are in the intersection of solved rows by each of the two solvers
            df_filtered = filter_intersection(df_filtered, key_benchmarks, key_instance, key_solvers)
            df_filtered = df_filtered.loc[:, [key_solvers, key_runtime]]

            # # ------------- DEBUG ------------- 
            # df_filtered = df_filtered.loc[:, [key_solvers, key_instance, key_runtime]]
            # # ------------- DEBUG ------------- 

            if(df_filtered.empty):
                # # ------------- DEBUG -------------
                # print("Sovler1: " + solver1.__str__())
                # print("Sovler2: " + solver2.__str__())
                # # ------------- DEBUG -------------

                continue
            
            # # ------------- DEBUG ------------- 
            # if(print_debug):
            #     print_full(df_filtered)
            # # ------------- DEBUG ------------- 

            # restructure data frame to be grouped by solvers
            df_filtered = df_filtered.groupby(key_solvers)
            
            # # ------------- DEBUG ------------- 
            # if(print_debug):
            #     for key, item in df_filtered:
            #         print_full(df_filtered.get_group(key))
            #         print("\n\n")
            # continue
            # # ------------- DEBUG ------------- 

            # calculate mean and std values of the runtimes on these filtered instances
            df_runtimeMean = df_filtered.mean()
            df_runtimeStd = df_filtered.std()
            df_runtimeSum = df_filtered.sum()

            # # ------------- DEBUG ------------- 
            # if(print_debug):
            #     print(df_runtimeMean)#DEBUG
            #     print(df_runtimeStd)#DEBUG
            #     return
            # # ------------- DEBUG ------------- 

            # retrieve values
            mean_solver1 = df_runtimeMean.loc[solver1].values[0]
            mean_solver2 = df_runtimeMean.loc[solver2].values[0]
            mean_diff = mean_solver2 - mean_solver1
            std_solver1 = df_runtimeStd.loc[solver1].values[0]
            std_solver2 = df_runtimeStd.loc[solver2].values[0]
            sum_solver1 = df_runtimeSum.loc[solver1].values[0]
            sum_solver2 = df_runtimeSum.loc[solver2].values[0]
            sum_diff = sum_solver2 - sum_solver1
            

            # fill cells in data frame
            if(is_under_diagonale):
                df_outputMean[solver1][solver2] = f"{mean_solver2:.{num_digits_std}f}" + "/" + f"{mean_solver1:.{num_digits_std}f}"
                df_outputMeanDiff[solver1][solver2] = mean_diff
                df_outputStd[solver1][solver2] = f"{std_solver2:.{num_digits_std}f}" + "/" + f"{std_solver1:.{num_digits_std}f}"
                df_outputSum[solver1][solver2] = f"{sum_solver2:.{num_digits_std}f}" + "/" + f"{sum_solver1:.{num_digits_std}f}"
                df_outputSumDiff[solver1][solver2] = sum_diff
            
            df_outputMeanSumPct[solver1][solver2] = (mean_solver2 / mean_solver1) * 100
            
            

            ## ------------- DEBUG ------------- 
            # if(print_debug):
            #     print(df_outputMean)#DEBUG
            #     print(df_outputStd)#DEBUG
            #     return
            ## ------------- DEBUG ------------- 
            
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