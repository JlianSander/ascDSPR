import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def create_table_runtime_comparison(df_rawAnswered, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, num_digits_std):
    solvers = sorted(df_rawAnswered[key_solvers].unique().tolist())
    
    #initialize output dataframe
    df_outputMean = pd.DataFrame(index=solvers, columns=solvers)
    df_outputStd = pd.DataFrame(index=solvers, columns=solvers)

    for i, solver1 in enumerate(solvers):
        for solver2 in solvers[i+1:]:
            if(solver1 == solver2):
                df_outputMean[solver1][solver1] = "-"
                df_outputStd[solver1][solver1] = "-"
                continue

            # Filter the dataframe for rows where solver_name is either solver_temp1 or solver_temp2
            df_filtered = df_rawAnswered[df_rawAnswered[key_solvers].isin([solver1, solver2])]
            # keep only those rows which are in the intersection of solved rows by each of the two solvers
            df_filtered = filter_intersection(df_filtered, key_benchmarks, key_instance, key_solvers)
            df_filtered = df_filtered.loc[:, [key_solvers, key_runtime]]
            
            # calculate mean and std values of the runtimes on these filtered instances
            df_runtimeMean = df_filtered.groupby(key_solvers).mean()
            df_runtimeStd = df_filtered.groupby(key_solvers).std()
            # print(df_runtimeMean)#DEBUG
            # print(df_runtimeStd)#DEBUG

            # fill cells in data frame
            df_outputMean[solver1][solver2] = df_runtimeMean.loc[solver2].values[0] - df_runtimeMean.loc[solver1].values[0]
            df_outputStd[solver1][solver2] = f"{df_runtimeStd.loc[solver2].values[0]:.{num_digits_std}f}" + "/" + f"{df_runtimeStd.loc[solver1].values[0]:.{num_digits_std}f}"

            # print(df_outputMean)#DEBUG
            # print(df_outputStd)#DEBUG
            # return
            
    df_outputMean = df_outputMean.drop(columns=[key_mutoksia])
    df_outputStd = df_outputStd.drop(columns=[key_mutoksia])
    df_outputMean = df_outputMean.fillna('')
    df_outputStd = df_outputStd.fillna('')
    
    print(df_outputMean)
    print(df_outputStd)

    # for jede solver combination intersection bilden
    # für jedes solver paar
        # für beide solver runtime auf intersectino berechnen
        # differenz in ensprechende zelle eintragen
        # wenn solver gleich dann '-' in zelle eintragen

    return (df_outputMean, df_outputStd)