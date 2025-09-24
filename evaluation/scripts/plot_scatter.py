import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from analysis import *
from analysis_util import *
from analysis_runtime import *

from plot import *

"""
    Based on work of Lars Bengel, published as: 
    Lars Bengel, Julian Sander, and Matthias Thimm. A reduct-based approach to skeptical
    preferred reasoning in abstract argumentation. In Proceedings of the 22th International 
    Conference on Principles of Knowledge Representation and Reasoning, KR 2025, 2025.
"""

#----------------------------------------------------------------------------------------------------------------------------------

def __preprocess_data(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, solver1, solver2):
    """
    Method to preprocess the data, so that it can be used to create a scatter plot
    
    Parameters:
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - solver1: solver on the x-axis of the plot to create
    - solver2: solver on the y-axis of the plot to create
    
    Returns:
        Data frame with two columns, each containing the runtimes of one solver for each instance
    """

    # Filter the dataframe for rows where solver_name is either solver1 or solver2
    df_intersection = filter_intersection_pair(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_solvers, solver1 , solver2)

    # keep only columns of interest
    df_intersection = df_intersection.loc[:, [key_instance, key_solvers, key_runtime]]

    # Add a counter to make 'instance' unique for each combination of 'instance' and 'solver_name'
    df_intersection[key_instance] = df_intersection.groupby([key_instance, key_solvers]).cumcount().astype(str) + '_' + df_intersection[key_instance]

    # pivot data
    df_intersection_pivoted = df_intersection.pivot(columns=key_solvers, index=key_instance, values=key_runtime)
    df_intersection_pivoted = df_intersection_pivoted.reset_index(drop=True)
    return df_intersection_pivoted

#----------------------------------------------------------------------------------------------------------------------------------

def save_plot_scatter(output_directory, save_pgf, save_png, df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, timeout, solver1, solver2, 
                      title_file, title_label):
    """
    Method to create and save a scatter plot of the two given solvers
    
    Parameters:
    - output_directory: string indicating the path to the output folder, where the plots are saved to
    - save_pgf: if 'True' saves the plot as a '.pgf' file in the given output directory
    - save_png: if 'True' saves the plot as a '.png' file in the given output directory
    - df_rawAnswered: DataFrame containing the raw results of the experiment including the answers of each solver for each instance
    - key_answer: string to access the answer column
    - key_benchmarks: string to access the rows of a specific benchmark dataset
    - key_instance: string to access column indicating the framework of the problem instance solved
    - key_runtime: string to access column of the runtime used to compute the solution of the problem instance
    - key_solvers: string to access the rows of a specific solver
    - timeout: number of seconds after which the calculation was aborted
    - solver1: solver on the x-axis of the plot to create
    - solver2: solver on the y-axis of the plot to create
    - title_file: string used as name of the file to create
    - title_label: string set in front of solver name as label
    
    Returns:
        void
    """


    # preprocess data
    df_data = __preprocess_data(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, solver1, solver2)
    s1 = df_data[solver1]
    s2 = df_data[solver2]

    # Set up Matplotlib for producing .tex output
    plt.rcParams.update({
        "backend": "pdf",
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        'pgf.preamble': r'\usepackage{amsmath}\usepackage[utf8x]{inputenc}\usepackage[T1]{fontenc}'
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    
    # SCALE 
    # set exponential scale at labels
    ax.set_xscale("log")
    ax.set_yscale("log")
    all_vals = np.concatenate([s1.tolist(), s2.tolist()])
    min_val = 10 ** np.floor(np.log10(all_vals.min()))
    max_val = 10 ** np.ceil(np.log10(all_vals.max()))

    # Extend range by one order in both directions
    x_min = min_val# / 10
    x_max = max_val# * 10
    
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(x_min, x_max)

    # AUX LINES
    # auxiliary lines and areas (trends and limits)
    x_vals = np.logspace(np.log10(min_val), np.log10(max_val), 100)

    # Fill between x/10 and x*10
    plt.fill_between(
        x_vals,
        x_vals * 0.1,
        x_vals * 10,
        color='gray',
        alpha=0.2,
        label='±1 order of magnitude'
    )

    # draw diagonal line
    ax.plot([min_val, max_val], [min_val, max_val],
         linestyle=':', color='gray', label='Equal Runtime')
    
    # draw timeout limit lines
    ax.axvline(x=timeout, color='r', linestyle='--', label=None,linewidth=1)
    ax.axhline(y=timeout, color='r', linestyle='--', label=None,linewidth=1)

    # PLOT DATA
    ax.scatter(s1, s2, marker="o",s=11,linewidths=0.75,facecolors='red',edgecolors='black',alpha=0.7)

    # FORMAT
    majorFormatter = plt.LogFormatterMathtext(base=10)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.yaxis.set_major_formatter(majorFormatter)

    # LABELS
    ax.set_xlabel(title_label + get_name(solver1), fontsize=16)
    ax.set_ylabel(title_label + get_name(solver2), fontsize=16)
    ax.tick_params(axis='both', which='major',labelsize=14)
    ax.grid(True, color='gray', ls=':', lw=1, zorder=1,alpha=0.5)

    plt.tight_layout()

    # save as files
    if(save_pgf):
        path_pgf = output_directory + title_file + ".pgf"
        file_output = open(path_pgf, "w")
        plt.savefig(file_output, format='pgf')

    if(save_png):
        path_png = output_directory + title_file + ".png"
        file_output = open(path_png, "wb")
        plt.savefig(file_output, format='png')