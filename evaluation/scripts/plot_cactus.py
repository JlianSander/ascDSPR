import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from analysis import *
from analysis_util import *
from analysis_runtime import *
from analysis_cascading_combi_standard import *

from plot import *

"""
    Based on work of Lars Bengel, published as: 
    Lars Bengel, Julian Sander, and Matthias Thimm. A reduct-based approach to skeptical
    preferred reasoning in abstract argumentation. In Proceedings of the 22th International 
    Conference on Principles of Knowledge Representation and Reasoning, KR 2025, 2025.
"""

# names = {
#     'reducto': r'\texttt{reducto}',
#     'mu-toksia-glucose': r'$\mu$-\textsc{toksia} (\textsc{Glucose})',
#     'asc_01': r'S\textsf{1}',
#     'asc_02': r'S\textsf{2}',
#     'asc_03': r'S\textsf{3}',
#     'asc_04': r'S\textsf{4}',
#     'asc_05': r'S\textsf{5}',
#     'asc_06': r'S\textsf{6}',
#     'asc_07': r'S\textsf{7}',
#     'asc_08': r'S\textsf{8}',
#     'asc_09': r'S\textsf{9}',
#     'asc_10': r'S\textsf{10}',
# }

names = {
    'mu-toksia-glucose': r'$\mu$-TOKSIA',
    'asc_01': 'S1',
    'asc_02': 'S2',
    'asc_03': 'S3',
    'asc_04': 'S4',
    'asc_05': 'S5',
    'asc_06': 'S6',
    'asc_07': 'S7',
    'asc_08': 'S8',
    'asc_09': 'S9',
    'asc_10': 'S10',
}

style_map = [
    {'marker': '*', 'linestyle': '-'},
    {'marker': 'P', 'linestyle': '--'},
    {'marker': '^', 'linestyle': '-.'},
    {'marker': 'D', 'linestyle': ':'},
    {'marker': 'o', 'linestyle': '-'},
    {'marker': 'x', 'linestyle': '--'},
    {'marker': 'v', 'linestyle': '-.'},
    {'marker': 's', 'linestyle': ':'},
    {'marker': '.', 'linestyle': '-'},
    {'marker': '1', 'linestyle': '--'},
    {'marker': '>', 'linestyle': '-.'}
]

#----------------------------------------------------------------------------------------------------------------------------------

def get_name(s_list):
    # Remove the outer parentheses and quotes
    mystring_cleaned = s_list[1:-1]  # removes the outermost parentheses and quotes

    # Handle the case with trailing commas by stripping any excess commas at the end
    mystring_cleaned = mystring_cleaned.rstrip(',')  # Remove any trailing commas

    # Replace the escaped single quotes with a clean backslash
    mystring_cleaned = re.sub("'", "", mystring_cleaned)

    # Convert the string to a list (split by commas)
    list_parsed = [item.strip() for item in mystring_cleaned.split(',')]

    name_output ="("

    for i, name_solver in enumerate(list_parsed):
        if i == 0:
            name_output = name_output + names[name_solver]
        else:
            name_output = name_output + ", " + names[name_solver]
        

    name_output = name_output + ")"
    return name_output

#----------------------------------------------------------------------------------------------------------------------------------

def create_data(df, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, title_runtime):
     # get list of the solvers
    unique_solvers = sorted(df[key_solvers].unique().tolist())
    # get a list wihtout Mu-Toksia
    unique_solvers_no_mu = [solver for solver in unique_solvers if solver != key_mutoksia]

    # create output data frame
    df_runtimes = pd.DataFrame()

    for solver in unique_solvers_no_mu:
        cascading_solvers = (solver, key_mutoksia)
        df_temp = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())
        df_runtimes = pd.concat([df_runtimes, df_temp], ignore_index=True)

    # calculate runtimes for only MuToksia
    cascading_solvers = (key_mutoksia,)
    df_temp = compute_runtime_combi(df, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, cascading_solvers, title_runtime, cascading_solvers.__str__())
    df_runtimes = pd.concat([df_runtimes, df_temp], ignore_index=True)
    

    return df_runtimes

#----------------------------------------------------------------------------------------------------------------------------------

def __preprocess_data(df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_mutoksia, key_runtime, key_solvers, title_runtime, timeout):
    """
    Method to preprocess the data, so that it can be used to create a scatter plot
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - timeout: number of seconds after which the calculation was aborted
    
    Returns:
        Data frame with two columns, each containing the runtimes of one solver for each instance
    """

    df_data = create_data(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_mutoksia, key_runtime, key_solvers, title_runtime)

    df_data = sanitize_dataframe(df_data, key_exit_with_error, key_runtime, timeout)

    # Add a counter to make 'instance' unique for each combination of 'instance' and 'solver_name'
    df_data[key_instance] = df_data.groupby([key_instance, key_solvers]).cumcount().astype(str) + '_' + df_data[key_instance]

    # focus on columns of interest
    df_data_filtered = df_data.loc[:, [key_instance, key_solvers, key_runtime]]
    
    # Group by solver
    df_rawAnswered_grouped = df_data_filtered.groupby(key_solvers)

    return df_rawAnswered_grouped

#----------------------------------------------------------------------------------------------------------------------------------

def save_plot_cactus(output_directory, save_pgf, save_png, df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_mutoksia, key_runtime, key_solvers, timeout, 
                      title_file, title_label_x, title_label_y, draw_timeout_limit):
    """
    Method to create and save a scatter plot of the two given solvers
    
    Parameters:
    - output_directory: string indicating the path to the output folder, where the plots are saved to
    - save_pgf: if 'True' saves the plot as a '.pgf' file in the given output directory
    - save_png: if 'True' saves the plot as a '.png' file in the given output directory
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_exit_with_error: string to access column indicating an error during calculation
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - timeout: number of seconds after which the calculation was aborted
    - title_file: string used as name of the file to create
    - title_label_x: string set as label on axis x
    - title_label_y: string set as label on axis y
    - draw_timeout_limit: if 'True' a limit line for the timeout is drawn
    
    Returns:
        void
    """

    key_runtime = "runtime"

    # preprocess data
    df_data = __preprocess_data(df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_mutoksia, key_runtime, key_solvers, key_runtime, timeout)

    # Set up Matplotlib for producing .tex output
    plt.rcParams.update({
        "backend": "pdf",
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        'pgf.preamble': r'\usepackage{amsmath}\usepackage[utf8x]{inputenc}\usepackage[T1]{fontenc}'
    })

     # Create figure and axis objects
    fig, ax = plt.subplots(figsize=(10, 10))

    # PLOT
    for i, (name, group) in enumerate(df_data):
        group = group.sort_values(by=key_runtime)
        group = group.reset_index(drop=True)

        # Filter out data points with runtime >= timeout
        group = group[group[key_runtime] < timeout]

        ax.plot(group[key_runtime], group.index, 
                marker=style_map[i]['marker'], 
                markersize=4, 
                markerfacecolor='white', 
                markeredgewidth=0.75, 
                linewidth=0.75, 
                linestyle=style_map[i]['linestyle'], 
                alpha=0.7, 
                label=get_name(name))

    # LABELS + TITLES
    ax.set_xlabel(title_label_x,fontsize=16)
    ax.set_ylabel(title_label_y,fontsize=16)
    legend = ax.legend(loc='lower right', fontsize=13, markerscale=1.75, handlelength=2, handletextpad=0.65,borderpad=0.75,borderaxespad=0.35,fancybox=True)

    # AUX LINES
    if(draw_timeout_limit):
        ax.axvline(x=timeout, color='r', linestyle='--', label=None)
    ax.set_ylim(800, None)

    ax.tick_params(axis='both', which='major',labelsize=13)
    ax.grid(True, color='gray', ls=':', lw=1, zorder=1,alpha=0.5)
    
    plt.tight_layout()

    # save as files
    if(save_pgf):
        path_pgf = output_directory + title_file + ".pgf"
        file_output = open(path_pgf, "w")
        plt.savefig(file_output, format='pgf')
        print(f"pgf graphic saved to: {path_pgf}")

        path_pdf = output_directory + title_file + ".pdf"
        file_output = open(path_pdf, "wb")
        plt.savefig(file_output, format='pdf')
        print(f"pdf graphic saved to: {path_pdf}")

    if(save_png):
        path_png = output_directory + title_file + ".png"
        file_output = open(path_png, "wb")
        plt.savefig(file_output, format='png')
        print(f"png graphic saved to: {path_png}")

