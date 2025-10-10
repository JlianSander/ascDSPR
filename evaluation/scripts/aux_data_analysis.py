import sys
import os
import pandas as pd

from parser_iccmaInfo import *
from analysis_util import *
from analysis_applicability import *
from analysis_overlap import *
from analysis_runtime import *
from analysis_runtime_intersection import *
from analysis_runtime_comparison import *
from analysis_runtime_comparison_muToksia import *
from analysis_cascading_combi_standard import *
from analysis_cascading_combi_flexible import *
from formatter_tables_thesis import *


# ---------------- CONSTANTS ---------------
NAME_MUTOSKIA = 'mu-toksia-glucose'
NAME_ANSWER_YES = 'YES'
NAME_ANSWER_NO = 'NO'


## ------------- DEBUG ------------- 

# Method to read a dataframe from a csv file
def read_csv_to_dataframe(file_path):
    try:
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path and try again.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)

#---------------------------------------------------------------------------------------------------------------------------

def analyze_muToksia(df_rawAnswered, key_answer, key_runtime, key_solvers):
    # only rows of MuToksia
    df_muToksia = df_rawAnswered[df_rawAnswered[key_solvers] == NAME_MUTOSKIA]
    

    df_muToksiaYes = filter_by_answer(df_muToksia, key_answer, NAME_ANSWER_YES)
    s_mu_runtimeYes = df_muToksiaYes[key_runtime]
    muRuntimeMeanYes = s_mu_runtimeYes.mean()
    muRuntimeStdYes = s_mu_runtimeYes.std()
    muRuntimeMaxYes = s_mu_runtimeYes.max()
    muRuntimeMinYes = s_mu_runtimeYes.min()
    muRuntimeMedianYes = s_mu_runtimeYes.median()
    print("Runtime MuToksia Yes Mean: " + muRuntimeMeanYes.__str__())
    print("Runtime MuToksia Yes Std: " + muRuntimeStdYes.__str__())
    print("Runtime MuToksia Yes Min/Max: " + muRuntimeMinYes.__str__() + "/" + muRuntimeMaxYes.__str__())
    print("Runtime MuToksia Yes Median: " + muRuntimeMedianYes.__str__())
    print()

    df_muToksiaNo = filter_by_answer(df_muToksia, key_answer, NAME_ANSWER_NO)
    s_mu_runtimeNo = df_muToksiaNo[key_runtime]
    muRuntimeMeanNo = s_mu_runtimeNo.mean()
    muRuntimeStdNo = s_mu_runtimeNo.std()
    muRuntimeMaxNo = s_mu_runtimeNo.max()
    muRuntimeMinNo = s_mu_runtimeNo.min()
    muRuntimeMedianNo = s_mu_runtimeNo.median()
    print("Runtime MuToksia No Mean: " + muRuntimeMeanNo.__str__())
    print("Runtime MuToksia No Std: " + muRuntimeStdNo.__str__())
    print("Runtime MuToksia No Min/Max: " + muRuntimeMinNo.__str__() + "/" + muRuntimeMaxNo.__str__())
    print("Runtime MuToksia No Median: " + muRuntimeMedianNo.__str__())
    print()

    ratio_mean_mutoksia = muRuntimeMeanYes / muRuntimeMeanNo
    print("Runtime MuToksia Ratio Mean_Yes/Mean_No: " + ratio_mean_mutoksia.__str__())


#---------------------------------------------------------------------------------------------------------------------------

def analyze_S10_muToksia(df_rawAnswered, df_solutions, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_runtime, key_solvers, timeout):
    # only rows of S10
    df_S10 = df_rawAnswered[df_rawAnswered[key_solvers] == "asc_10"]
    print(df_S10)

    df_solutions_yes = df_solutions[df_solutions[key_answer] == NAME_ANSWER_YES]
    df_instances = df_solutions_yes.loc[:, [key_benchmarks, key_instance]] 
    print(df_instances)

    # Filter 'df' based on the values in 's_instances'
    df_filtered = pd.merge(df_S10, df_instances, on=[key_benchmarks, key_instance], how='inner')
    df_S10_clean = sanitize_dataframe(df_filtered, key_exit_with_error, key_runtime, timeout)
    df_S10_clean = df_S10_clean.loc[:, [key_benchmarks, key_instance, key_runtime, key_answer]] 

    # Display the filtered DataFrame
    print_full(df_S10_clean)

    # Count the number of rows where runtime is timeout or higher
    count_timeouts = (df_S10_clean[key_runtime] >= timeout).sum()
    count_unsolved = (df_S10_clean[key_answer] != NAME_ANSWER_YES).sum()

    print(f"Number of rows with runtime >= timeout: {count_timeouts}")
    print(f"Number of rows with answer == 'NaN': {count_unsolved}")

#---------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Check if file path is provided as command-line argument
    if len(sys.argv) != 5:
        print("Usage: python3 analysis.py <file_path_raw> <file_path_resultsDetails> <file_path_solution_details> <output_directory>")
        sys.exit(1)
    
    #-------------------------------- initializing data --------------------------------

    # read paths to data
    file_path_raw = sys.argv[1]
    file_path_resultsDetails = sys.argv[2]
    file_path_solutions = sys.argv[3]
    output_directory = sys.argv[4]
    if not os.path.isdir(output_directory):
        print(f"The path {output_directory} is not a directory.")
        sys.exit(1)
    
    # read data frame of raw results from probo
    df_raw = read_csv_to_dataframe(file_path_raw)

    # read keys from input data frames
    key_benchmarks = df_raw.columns[15]  #'benchmark_name'
    key_instance = df_raw.columns[4] #'instance'
    key_solvers = df_raw.columns[0] #'solver_name'
    key_timedout = df_raw.columns[7] #timed_out
    key_task = df_raw.columns[6] #'task'
    key_runtime = df_raw.columns[9] #'runtime'
    timeout = df_raw.loc[0,df_raw.columns[14]] #"cut_off"
    key_exit_with_error = df_raw.columns[11] #'exit_with_error'

    # read data frame from analyzing the .out files of the experiment
    df_resDetails = read_csv_to_dataframe(file_path_resultsDetails)

    # read keys from input data frames
    key_answer = df_resDetails.columns[4] #'answer'

    # read data frame from the general information about the iccma benchmark datasets
    df_solutions = read_csv_to_dataframe(file_path_solutions)

    #-------------------------------- preprocessing data --------------------------------

    # get the total number of instances as a row
    dfrow_total_instances = extract_number_instances(df_solutions, key_benchmarks, key_instance)

    # merge answers with raw data
    df_rawAnswered = pd.merge(df_raw, df_resDetails, on=[key_solvers,key_task,key_benchmarks,key_instance], how='left')

    # filter data frame to have only answers of one type
    df_answeredYES = filter_by_answer(df_rawAnswered, key_answer, NAME_ANSWER_YES)
    df_answeredNO = filter_by_answer(df_rawAnswered, key_answer, NAME_ANSWER_NO)

    df_solutionsYes = filter_by_answer(df_solutions, key_answer, NAME_ANSWER_YES)
    df_solutionsNo = filter_by_answer(df_solutions, key_answer, NAME_ANSWER_NO)

    # analyze_muToksia(df_rawAnswered, key_answer, key_runtime, key_solvers)

    analyze_S10_muToksia(df_rawAnswered, df_solutions, key_answer, key_benchmarks, key_exit_with_error, key_instance, key_runtime, key_solvers, timeout)

    
