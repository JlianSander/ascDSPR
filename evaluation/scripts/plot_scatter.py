import sys
import pandas as pd
import matplotlib.pyplot as plt

from analysis import *
from analysis_util import *
from analysis_runtime import *


SAVE_PLOT_PGF = True
SAVE_PLOT_PNG = True


style_map = [
    {'marker': 'x', 'linestyle': '-'},
    {'marker': 'o', 'linestyle': '--'},
    {'marker': '^', 'linestyle': '-.'},
    {'marker': 'D', 'linestyle': ':'},
    {'marker': 'P', 'linestyle': '-'},
    {'marker': '*', 'linestyle': '--'},
    {'marker': 'v', 'linestyle': '-.'},
    {'marker': 's', 'linestyle': ':'}
]

#----------------------------------------------------------------------------------------------------------------------------------

def preprocess_data(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, solver1, solver2):

    # Filter the dataframe for rows where solver_name is either solver1 or solver2
    list_solvers = (solver1, solver2)
    df_filtered = df_rawAnswered[df_rawAnswered[key_solvers].isin(list_solvers)]

    # keep only those rows which are in the intersection of solved rows by each of the two solvers
    df_intersection = filter_intersection(df_filtered, key_answer, key_benchmarks, key_instance, key_solvers)
    df_intersection = df_intersection.loc[:, [key_instance, key_solvers, key_runtime]]

    # Add a counter to make 'instance' unique for each combination of 'instance' and 'solver_name'
    df_intersection['instance'] = df_intersection.groupby(['instance', 'solver_name']).cumcount().astype(str) + '_' + df_intersection['instance']

    # pivot data
    df_intersection_pivoted = df_intersection.pivot(columns=key_solvers, index=key_instance, values=key_runtime)
    df_intersection_pivoted = df_intersection_pivoted.reset_index(drop=True)
    return df_intersection_pivoted

#----------------------------------------------------------------------------------------------------------------------------------

def create_plot_scatter(output_directory, df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, timeout, solver1, solver2, title_file, title_label):
    
    # preprocess data
    df_data = preprocess_data(df_rawAnswered, key_answer, key_benchmarks, key_instance, key_runtime, key_solvers, solver1, solver2)
    s1 = df_data[solver1]
    s2 = df_data[solver2]

    # Set up Matplotlib for producing .tex output
    plt.rcParams.update({
        "backend": "pdf",
        "pgf.texsystem": "pdflatex",
        "text.usetex": True,
        "font.family": "serif",
        #"font.sans-serif": ['Helvetica', "Tahoma"],
        'pgf.preamble': r'\usepackage{amsmath}\usepackage[utf8x]{inputenc}\usepackage[T1]{fontenc}'
        #"pgf.preamble": r"\usepackage{amsmath}\usepackage{courier}\usepackage{textcomp}"#\setmonofont{Fira Mono}"#\renewcommand{\familydefault}{\ttdefault}"
    })

    # Create figure and axis objects
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_yscale("log")
    ax.set_xscale("log")
    all_vals = np.concatenate([s1.tolist(), s2.tolist()])
    min_val = 10 ** np.floor(np.log10(all_vals.min()))
    max_val = 10 ** np.ceil(np.log10(all_vals.max()))

    # Extend range by one order in both directions
    x_min = min_val# / 10
    x_max = max_val# * 10
    
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(x_min, x_max)

    # PLOT DATA
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

    ax.plot([min_val, max_val], [min_val, max_val],
         linestyle=':', color='gray', label='Equal Runtime')
    
    
    ax.axvline(x=timeout, color='r', linestyle='--', label=None,linewidth=1)
    ax.axhline(y=timeout, color='r', linestyle='--', label=None,linewidth=1)

    ax.scatter(s1, s2, marker="o",s=11,linewidths=0.75,facecolors='red',edgecolors='black',alpha=0.7)
    

    # CREATE TICKS
    ticks = [1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4]
    #ax.set_xticks(ticks)
    #ax.set_yticks(ticks)
    
    #ax.set_xticklabels(ax.get_xticks(), f_props)
    #ax.set_yticklabels(ax.get_yticks(), f_props)

    majorFormatter = plt.LogFormatterMathtext(base=10)
    ax.xaxis.set_major_formatter(majorFormatter)
    ax.yaxis.set_major_formatter(majorFormatter)

 
    # LABELS
    ax.set_ylabel(get_name(solver1), fontsize=16)
    ax.set_xlabel(get_name(solver2), fontsize=16)
    ax.tick_params(axis='both', which='major',labelsize=14)
    #ax.grid(True, linestyle=":",linewidth=0.75)
    ax.grid(True, color='gray', ls=':', lw=1, zorder=1,alpha=0.5)



    # OUTPUT
    plt.tight_layout()

    # df_data.plot(kind = 'scatter', x = solver1, y = solver2)
    # plt.xlabel(title_label + solver1)
    # plt.ylabel(title_label + solver2)

    # save as pgf file
    if(SAVE_PLOT_PGF):
        path_pgf = output_directory + title_file + ".pgf"
        file_output = open(path_pgf, "w")
        plt.savefig(file_output, format='pgf')

    if(SAVE_PLOT_PNG):
        path_png = output_directory + title_file + ".png"
        file_output = open(path_png, "wb")
        plt.savefig(file_output, format='png')