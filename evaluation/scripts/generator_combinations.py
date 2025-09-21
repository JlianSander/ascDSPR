import sys
import pandas as pd
import numpy as np
import itertools

from analysis_runtime import *
from analysis_util import *
from analysis_balance import *
from analysis_balance_combi import *

def create_table_balance_sheet_combination(df, key_answer, key_instance, key_mutoksia, key_runtime, key_solvers, title_balance, title_pct_change, title_resulting_sum_rt, title_solver_VBS, title_vbsCount):
    

    # get a list of all instances
    unique_instances = df[key_instance].unique()

    # get only those rows of Mu-Toksia
    df_muToksia = df[(df[key_solvers] == key_mutoksia)]
    df_muToksia = df_muToksia[[key_instance, key_runtime]]

    # create a series of balance values of the different combis
    s_balances_combies = pd.Series()

    # get the solvers, except for mutoksia
    unique_solvers = sorted(df[key_solvers].unique().tolist())
    unique_solvers = [solver for solver in unique_solvers if solver != key_mutoksia]


    #TODO build up the list of solvers so that each possible combination is visited

    # Generate all possible permutations
    permutations = list(itertools.permutations(unique_solvers))
    print(len(permutations))

    # iterate through each possible permutation
    for perm in permutations:
        df_balance = compute_balance_combi(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, perm, perm.__str__())
        sum_balance = df_balance.sum().iloc[0]
        s_balances_combies[perm.__str__()] = sum_balance
        break

    list_combi = ('asc_01','asc_02','asc_03','asc_04')
    df_balance = compute_balance_combi(df, df_muToksia, key_answer, key_instance, key_runtime, key_solvers, unique_instances, list_combi, list_combi.__str__())
    sum_balance = df_balance.sum().iloc[0]
    s_balances_combies[list_combi.__str__()] = sum_balance

    print(s_balances_combies)