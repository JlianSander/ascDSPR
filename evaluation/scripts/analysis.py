import sys
import pandas as pd

from parser_iccmaInfo import *
from analysis_util import *
from analysis_applicability import *
from analysis_overlap import *
from analysis_runtime import *
from analysis_runtime_intersection import *
from analysis_runtime_comparison import *


# ---------------- CONSTANTS ---------------
NAME_MUTOSKIA = 'mu-toksia-glucose'
NAME_COLUMN_PERCENTAGE = 'percentage'
NAME_ROW_SOLUTION = 'solution'
NAME_ANSWER_YES = 'YES'
NAME_ANSWER_NO = 'NO'
SUFFIX_PERCENTAGE = '_PCT'
TABLE_FORMAT_OVERLAP_INT = "INT"
TABLE_FORMAT_OVERLAP_PCT = "PCT"
TABLE_FORMAT_OVERLAP_FORMATTED = "STRING"
NUM_STD_LIMIT = 3
NUM_STD_DIGITS = 3
TITLE_INSTANCES = '#AF'
TITLE_RUNTIME_MEAN = "mean RT"
TITLE_RUNTIME_STD = "std RT"
TITLE_RUNTIME_SUM = "sum RT"
TITLE_RUNTIME_MEAN_CAPPED = "mean RT*"
TITLE_RUNTIME_STD_CAPPED = "std RT*"
TITLE_RUNTIME_SUM_CAPPED = "sum RT*"
TITLE_RUNTIME_VBS_COUNT = "#VBS"
TITLE_SOLVER_VBS = 'VBS'


## ------------- DEBUG ------------- 
PRINT_APP_YES = True
PRINT_APP_NO = True
PRINT_OVERLAP_YES = True
PRINT_OVERLAP_NO = True
PRINT_RT_INTERSEC_YES = True
PRINT_RT_INTERSEC_NO = True
PRINT_RT_COMP_YES = True
PRINT_RT_COMP_NO = True
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

if __name__ == "__main__":
    # Check if file path is provided as command-line argument
    if len(sys.argv) != 5:
        print("Usage: python3 analysis.py <file_path_raw> <file_path_resultsDetails> <file_path_iccma_summary> <output_file>")
        sys.exit(1)
    
    #-------------------------------- initializing data --------------------------------

    # read paths to data
    file_path_raw = sys.argv[1]
    file_path_resultsDetails = sys.argv[2]
    file_path_iccmas = sys.argv[3]
    output_file = sys.argv[4]
    
    # read data frame of raw results from probo
    df_raw = read_csv_to_dataframe(file_path_raw)

    # read keys from input data frames
    key_benchmarks = df_raw.columns[15]  #'benchmark_name'
    key_instance = df_raw.columns[4] #'instance'
    key_solvers = df_raw.columns[0] #'solver_name'
    key_task = df_raw.columns[6] #'task'
    key_runtime = 'runtime'
    timeout = df_raw.loc[0,"cut_off"]
    key_exit_with_error = 'exit_with_error'

    # read data frame from analyzing the .out files of the experiment
    df_resDetails = read_csv_to_dataframe(file_path_resultsDetails)

    # read keys from input data frames
    key_answer = df_resDetails.columns[4] #'answer'

    # read data frame from the general information about the iccma benchmark datasets
    df_iccmas = read_csv_to_dataframe(file_path_iccmas)
    df_iccmas = df_iccmas.set_index(key_benchmarks)

    # read keys from input data frames
    key_number_no = df_iccmas.columns[2] #'number_no'
    key_number_yes = df_iccmas.columns[1] #'number_yes'
    key_total_number_instances = df_iccmas.columns[0] #'number_instances'


    #-------------------------------- preprocessing data --------------------------------
    
    # get the total number of instances as a row
    dfrow_total_instances = extract_total_number_instances(df_iccmas, key_total_number_instances)

    # merge answers with raw data
    df_rawAnswered = pd.merge(df_raw, df_resDetails, on=[key_solvers,key_task,key_benchmarks,key_instance], how='left')

    # filter data frame to have only answers of one type
    df_answeredYES = filter_by_answer(df_rawAnswered, key_answer, NAME_ANSWER_YES)
    df_answeredNO = filter_by_answer(df_rawAnswered, key_answer, NAME_ANSWER_NO)

    #-------------------------------- creating analysis --------------------------------

    # create the tables for visualizing the number of answers found by each solver
    df_tabApplicability_yes = create_table_number_answers(df_answeredYES, extract_solution_data(df_iccmas, key_number_yes, NAME_ROW_SOLUTION), dfrow_total_instances, key_answer,  
                                      key_benchmarks, NAME_MUTOSKIA, key_total_number_instances, NAME_COLUMN_PERCENTAGE, NAME_ROW_SOLUTION, key_solvers)
    df_tabApplicability_no = create_table_number_answers(df_answeredNO, extract_solution_data(df_iccmas, key_number_no, NAME_ROW_SOLUTION), dfrow_total_instances, key_answer,  
                                      key_benchmarks, NAME_MUTOSKIA, key_total_number_instances, NAME_COLUMN_PERCENTAGE, NAME_ROW_SOLUTION, key_solvers)
    if(PRINT_APP_YES):
        print()
        print("----------------- applicability YES -----------------")    
        print(df_tabApplicability_yes)
    if(PRINT_APP_NO):
        print()
        print("----------------- applicability NO -----------------")  
        print(df_tabApplicability_no)
    
    # create the tables for visualizing the overlap of the applicability of the different solvers
    df_tabOverlap_int_yes = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_YES, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_INT)
    df_tabOverlap_pct_yes = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_YES, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_PCT)
    df_tabOverlap_formatted_yes = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_YES, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_FORMATTED)

    if(PRINT_OVERLAP_YES):
        print()
        print("----------------- overlap YES -----------------")
        # print(df_tabOverlap_int_yes)
        # print(df_tabOverlap_pct_yes)
        print(df_tabOverlap_formatted_yes)

    df_tabOverlap_int_no = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_NO, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_INT)
    df_tabOverlap_pct_no = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_NO, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_PCT)
    df_tabOverlap_formatted_no = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_NO, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_FORMATTED)

    if(PRINT_OVERLAP_NO):
        print()
        print("----------------- overlap NO -----------------")
        # print(df_tabOverlap_int_no)
        # print(df_tabOverlap_pct_no)
        print(df_tabOverlap_formatted_no)

    # filter out all rows of the solver 'asc_01'
    df_rawAnsweredNoASC01 = df_answeredNO[df_answeredNO['solver_name'] != 'asc_01']
    # analyze runtime of the intersection of instances of solved instances of solvers
    df_tabRuntime_intersect_yes = create_table_runtime_intersection(df_answeredYES, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, timeout, NUM_STD_LIMIT, False,
                         TITLE_SOLVER_VBS, TITLE_INSTANCES, TITLE_RUNTIME_MEAN, TITLE_RUNTIME_STD, TITLE_RUNTIME_SUM, TITLE_RUNTIME_MEAN_CAPPED, TITLE_RUNTIME_STD_CAPPED, TITLE_RUNTIME_SUM_CAPPED, TITLE_RUNTIME_VBS_COUNT)
    df_tabRuntime_intersectNoASC01_no = create_table_runtime_intersection(df_rawAnsweredNoASC01, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, timeout, NUM_STD_LIMIT, True,
                         TITLE_SOLVER_VBS, TITLE_INSTANCES, TITLE_RUNTIME_MEAN, TITLE_RUNTIME_STD, TITLE_RUNTIME_SUM, TITLE_RUNTIME_MEAN_CAPPED, TITLE_RUNTIME_STD_CAPPED, TITLE_RUNTIME_SUM_CAPPED, TITLE_RUNTIME_VBS_COUNT)
    
    if(PRINT_RT_INTERSEC_YES):
        print()
        print("----------------- runtime intersection YES -----------------")
        print(df_tabRuntime_intersect_yes)

    if(PRINT_RT_INTERSEC_NO):
        print()
        print("----------------- runtime intersection NO (no asc_01) -----------------")
        print(df_tabRuntime_intersectNoASC01_no)
        
    df_tabRuntime_comparisonYes = create_table_runtime_comparison(df_answeredYES, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, NUM_STD_DIGITS, timeout, TITLE_SOLVER_VBS)
    df_tabRuntime_comparisonNo = create_table_runtime_comparison(df_answeredNO, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, NUM_STD_DIGITS, timeout, TITLE_SOLVER_VBS)
   

    if(PRINT_RT_COMP_YES):
        print()
        print("----------------- runtime comparison YES -----------------")
        print(" - mean -")
        print(df_tabRuntime_comparisonNo[0])
        print()
        print(" - mean difference -")
        print(df_tabRuntime_comparisonNo[1])
        print()
        print(" - std -")
        print(df_tabRuntime_comparisonNo[3])
        print()
        print(" - sum -")
        print(df_tabRuntime_comparisonNo[4])
        print()
        print(" - sum difference -")
        print(df_tabRuntime_comparisonNo[5])
        print()
        print(" - mean/sum procentual -")
        print(df_tabRuntime_comparisonNo[2])
        print()
        print(" - #VBS -")
        print(df_tabRuntime_comparisonNo[6])

    if(PRINT_RT_COMP_NO):
        print()
        print("----------------- runtime comparison NO -----------------")
        print(" - mean -")
        print(df_tabRuntime_comparisonNo[0])
        print()
        print(" - mean difference -")
        print(df_tabRuntime_comparisonNo[1])
        print()
        print(" - std -")
        print(df_tabRuntime_comparisonNo[3])
        print()
        print(" - sum -")
        print(df_tabRuntime_comparisonNo[4])
        print()
        print(" - sum difference -")
        print(df_tabRuntime_comparisonNo[5])
        print()
        print(" - mean/sum procentual -")
        print(df_tabRuntime_comparisonNo[2])
        print()
        print(" - #VBS -")
        print(df_tabRuntime_comparisonNo[6])


    # Save table to file
    #table_df.to_latex(output_file + '_table.tex', index=False) 
    