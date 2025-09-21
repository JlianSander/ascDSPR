import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def create_table_balance_sheet(df, key_answer, key_instance, key_mutoksia, key_runtime, key_solvers, title_balance, title_solver_VBS, title_vbsCount):
    """
    Method to create a table visualizing a pairwise comparison of the solvers runtimes on the intersection of their solved instances
    
    Parameters:
    - df: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_mutoksia: string to access the row of the benchmark-solver
    - key_solvers: string to access the rows of a specific solver
    - num_digits_std: number indicating the number of digits displayed for the standard deviation
    - timeout: number of seconds after which the calculation was aborted
    - title_solver_VBS: string used as a title for the row of the VBS solver
    
    Returns:
    - DataFrame visualizing a pairwise comparison of the solvers runtimes on the intersection of their solved instances
    """

    # Create the output data frame

    # get list of the solvers, wihtout Mu-Toksia
    unique_solvers = df[key_solvers].unique()
    unique_solvers = [solver for solver in unique_solvers if solver != key_mutoksia]
    df_result = pd.DataFrame(index=unique_solvers, columns=[title_balance])

    # Iterate through each solver
    for solverX in df_result.index:
        sumX = 0.0

        # Filter out the rows of this solver
        solver_rows = df[df[key_solvers] == solverX]

        for _, rowX in solver_rows.iterrows():
            # Subtract runtime for each row/instance of the solver from the sum
            sumX -= rowX[key_runtime]
            instanceX = rowX[key_instance]
            
            # Check if answer of the solver for this instance was NaN, if not add Mu-Toksia's runtime for this instance
            if pd.notna(rowX[key_answer]):
                # Find the corresponding instance solved by Mu_Toksia
                rowY = df[(df[key_solvers] == key_mutoksia) & (df[key_instance] == instanceX)]

                if not rowY.empty:
                    # Add the runtime of Mu-Toksia
                    sumX += rowY.iloc[0][key_runtime]

        # fill the cell in the result data frame
        df_result.loc[solverX, title_balance] = sumX

    # Now, df_result contains the 'balance' for each solver.
    print(df_result)

