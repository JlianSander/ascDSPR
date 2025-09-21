import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def __compute_balance(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, unique_solvers):
    # create the data frame containing for each instance and each solver the calculated balance
    df_balance = pd.DataFrame(index=unique_instances, columns=unique_solvers)

    # Iterate through each solver
    for solverX in unique_solvers:

        # Filter out the rows of this solver
        solver_rows = df[df[key_solvers] == solverX]

        for _, rowX in solver_rows.iterrows():
            # set runtime of solver as negative number in the corresponding cell
            instanceX = rowX[key_instance]
            df_balance.loc[instanceX, solverX] = rowX[key_runtime]
            
            # Check if answer of the solver for this instance was NaN, if not add Mu-Toksia's runtime for this instance
            if pd.notna(rowX[key_answer]):
                # Find the corresponding instance solved by Mu_Toksia
                row_muToksia = df_muToksia[(df_muToksia[key_instance] == instanceX)]

                if not row_muToksia.empty:
                    # Add the runtime of Mu-Toksia
                    df_balance.loc[instanceX, solverX] -= row_muToksia.iloc[0][key_runtime]

    return df_balance