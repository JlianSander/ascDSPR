import sys
import pandas as pd
import numpy as np

from analysis_runtime import *
from analysis_util import *

def create_table_rt_naiv(df_rawAnswered, key_solvers, key_runtime):
    # Group by 'solver_name' and sum the 'runtime' column
    return df_rawAnswered.groupby('solver_name')['runtime'].sum()