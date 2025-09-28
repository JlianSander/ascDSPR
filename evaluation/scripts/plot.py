import sys
import pandas as pd
import matplotlib.pyplot as plt

from parser_iccmaInfo import *
from analysis import *
from analysis_util import *
from analysis_runtime import *
from plot_scatter import *
from plot_cactus import *

# ---------------- CONTROLS ---------------

SAVE_PLOT_PGF = True
SAVE_PLOT_PNG = True

# ---------------- CONSTANTS ---------------
NAME_MUTOSKIA = 'mu-toksia-glucose'
NAME_ANSWER_YES = 'YES'
NAME_ANSWER_NO = 'NO'

names = {
    'reducto': r'\texttt{reducto}',
    'mu-toksia-glucose': r'$\mu$-\textsc{toksia} (\textsc{Glucose})',
    'asc_01': r'S\textsf{1}',
    'asc_02': r'S\textsf{2}',
    'asc_03': r'S\textsf{3}',
    'asc_04': r'S\textsf{4}',
    'asc_05': r'S\textsf{5}',
    'asc_06': r'S\textsf{6}',
    'asc_07': r'S\textsf{7}',
    'asc_08': r'S\textsf{8}',
    'asc_09': r'S\textsf{9}',
    'asc_10': r'S\textsf{10}',
}

style_map = [
    {'marker': '*', 'linestyle': '-'},
    {'marker': 'P', 'linestyle': '--'},
    {'marker': '^', 'linestyle': '-.'},
    {'marker': 'D', 'linestyle': ':'},
    {'marker': 'o', 'linestyle': '-'},
    {'marker': 'x', 'linestyle': '--'},
    {'marker': 'v', 'linestyle': '-.'},
    {'marker': 's', 'linestyle': ':'}
]

def get_style(index):
    return style_map[index]

def get_name(solver):
    if solver in names:
        return names[solver]
    else:
        return solver

#---------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Check if file path is provided as command-line argument
    if len(sys.argv) != 4:
        print("Usage: python3 plot.py <file_path_raw> <file_path_resultsDetails> <output_directory>")
        sys.exit(1)
    
    #-------------------------------- initializing data --------------------------------

    # read paths to data
    file_path_raw = sys.argv[1]
    file_path_resultsDetails = sys.argv[2]
    output_directory = sys.argv[3]
    if not os.path.isdir(output_directory):
        print(f"The path {output_directory} is not a directory.")
        sys.exit(1)
    
    # read data frame of raw results from probo
    df_raw = read_csv_to_dataframe(file_path_raw)

    # read keys from input data frames
    key_benchmarks = df_raw.columns[15]  #'benchmark_name'
    key_instance = df_raw.columns[4] #'instance'
    key_solvers = df_raw.columns[0] #'solver_name'
    key_task = df_raw.columns[6] #'task'
    key_runtime = df_raw.columns[9] #'runtime'
    timeout = df_raw.loc[0,df_raw.columns[14]] #"cut_off"
    key_exit_with_error = df_raw.columns[11] #'exit_with_error'

    # read data frame from analyzing the .out files of the experiment
    df_resDetails = read_csv_to_dataframe(file_path_resultsDetails)

    # read keys from input data frames
    key_answer = df_resDetails.columns[4] #'answer'


    #-------------------------------- preprocessing data --------------------------------
    # clean runtimes
    df_raw = sanitize_dataframe(df_raw, key_exit_with_error, key_runtime, timeout)

    # merge answers with raw data
    df_rawAnswered = pd.merge(df_raw, df_resDetails, on=[key_solvers,key_task,key_benchmarks,key_instance], how='left')

    # filter data frame to have only answers of one type
    df_answeredYES = filter_by_answer(df_rawAnswered, key_answer, NAME_ANSWER_YES)
    df_answeredNO = filter_by_answer(df_rawAnswered, key_answer, NAME_ANSWER_NO)

    #-------------------------------- create plots --------------------------------

    save_plot_scatter(output_directory, SAVE_PLOT_PGF, SAVE_PLOT_PNG, df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, timeout, NAME_MUTOSKIA, 
                     'asc_05', 'scatter_muToksia_asc05', 'runtime[s] ')
    save_plot_scatter(output_directory, SAVE_PLOT_PGF, SAVE_PLOT_PNG, df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, timeout, NAME_MUTOSKIA, 
                     'asc_10', 'scatter_muToksia_asc10', 'runtime[s] ')
    
    save_plot_cactus(output_directory, SAVE_PLOT_PGF, SAVE_PLOT_PNG, df_rawAnswered, key_answer, key_benchmarks, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, timeout, 'cactus_all', "runtime~$(s)$", "instances~solved", True)