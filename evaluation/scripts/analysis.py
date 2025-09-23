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
from analysis_balance import *
from analysis_balance_combi import *
from formatter_tables_thesis import *


# ---------------- CONSTANTS ---------------
DELTA_PERCENTAGE = 0.05
NAME_MUTOSKIA = 'mu-toksia-glucose'
NAME_ANSWER_YES = 'YES'
NAME_ANSWER_NO = 'NO'
NAME_PREFIX_ASC_LATEX = 'Sc'
NUM_DIGITS = 2
NUM_DIGITS_PCT = 0
NUM_DIGITS_SUM = 0
NUM_DIGITS_STD = 3
NUM_STD_LIMIT = 3
SUFFIX_PERCENTAGE = ' %'
TABLE_FORMAT_OVERLAP_INT = "INT"
TABLE_FORMAT_OVERLAP_PCT = "PCT"
TABLE_FORMAT_OVERLAP_FORMATTED = "STRING"
TITLE_APPLICABILITY_PERCENTAGE = 'percentage'
TITLE_APPLICABILITY_ROW_SOLUTION = 'solution'
TITLE_APPLICABILITY_TOTAL = "total"
TITLE_INSTANCES = '#AF'
TITLE_RUNTIME_MEAN = "mean RT"
TITLE_RUNTIME_STD = "std RT"
TITLE_RUNTIME_SUM = "sum RT"
TITLE_RUNTIME_SUM_PCT = " %"
TITLE_RUNTIME_MEAN_CAPPED = "mean RT*"
TITLE_RUNTIME_STD_CAPPED = "std RT*"
TITLE_RUNTIME_SUM_CAPPED = "sum RT*"
TITLE_VBS_COUNT = "#VBS"
TITLE_VBS_COUNT_PCT = "%"
TITLE_SOLVER_VBS = 'VBS'
TITLE_BALANCE = "Balance"
TITLE_BALANCE_PCT_CHANGE = " %"
TITLE_BALANCE_SUM_RT = "sum RT"


## ------------- DEBUG ------------- 
PRINT_APP_YES = False
PRINT_APP_NO = False
PRINT_OVERLAP_INT_YES = False
PRINT_OVERLAP_PCT_YES = False
PRINT_OVERLAP_FORMATTED_YES = False
PRINT_OVERLAP_INT_NO = False
PRINT_OVERLAP_PCT_NO = False
PRINT_OVERLAP_FORMATTED_NO = False
PRINT_RT_INTERSEC_YES = False
PRINT_RT_INTERSEC_NO = False
PRINT_RT_COMP_YES = False
PRINT_RT_COMP_NO = False
PRINT_RT_COMP_MUTOKSIA = False
PRINT_BL_ALL = False
PRINT_BL_YES = False
PRINT_BL_NO = False
PRINT_BL_COMBI = False

CALCULATE_APP = True
CALCULATE_OVERLAP = False
CALCULATE_RT_INTERSEC = False
CACLCULATE_RT_COMP_MUTOKSIA = False
CALCULATE_RT_COMP = False
CALCULATE_BL = False
CALCULATE_BL_COMBI = False

SAVE_LATEX = True
## ------------- DEBUG ------------- 

# Method to read a dataframe from a csv file
def __read_csv_to_dataframe(file_path):
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


def __save_latex_file(dir_path, filename, latex_code):
    # Full path to the new file
    file_path = os.path.join(dir_path, filename)

    # Save the LaTeX code to the file
    with open(file_path, 'w') as f:
        f.write(latex_code)
    
    print(f"LaTeX table saved to: {file_path}")

#---------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Check if file path is provided as command-line argument
    if len(sys.argv) != 5:
        print("Usage: python3 analysis.py <file_path_raw> <file_path_resultsDetails> <file_path_iccma_summary> <output_directory>")
        sys.exit(1)
    
    #-------------------------------- initializing data --------------------------------

    # read paths to data
    file_path_raw = sys.argv[1]
    file_path_resultsDetails = sys.argv[2]
    file_path_iccmas = sys.argv[3]
    output_directory = sys.argv[4]
    if not os.path.isdir(output_directory):
        print(f"The path {output_directory} is not a directory.")
        sys.exit(1)
    
    # read data frame of raw results from probo
    df_raw = __read_csv_to_dataframe(file_path_raw)

    # read keys from input data frames
    key_benchmarks = df_raw.columns[15]  #'benchmark_name'
    key_instance = df_raw.columns[4] #'instance'
    key_solvers = df_raw.columns[0] #'solver_name'
    key_task = df_raw.columns[6] #'task'
    key_runtime = df_raw.columns[9] #'runtime'
    timeout = df_raw.loc[0,df_raw.columns[14]] #"cut_off"
    key_exit_with_error = df_raw.columns[11] #'exit_with_error'

    # read data frame from analyzing the .out files of the experiment
    df_resDetails = __read_csv_to_dataframe(file_path_resultsDetails)

    # read keys from input data frames
    key_answer = df_resDetails.columns[4] #'answer'

    # read data frame from the general information about the iccma benchmark datasets
    df_iccmas = __read_csv_to_dataframe(file_path_iccmas)
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

    if(CALCULATE_APP):
        #-------------------------------- APPLICABILITY --------------------------------
        # create the tables for visualizing the number of answers found by each solver
        df_tabApplicability_yes = create_table_number_answers(df_answeredYES, extract_solution_data(df_iccmas, key_number_yes, TITLE_APPLICABILITY_ROW_SOLUTION), key_answer,  
                                        key_benchmarks, NAME_MUTOSKIA, TITLE_APPLICABILITY_ROW_SOLUTION, key_solvers, TITLE_APPLICABILITY_PERCENTAGE, TITLE_APPLICABILITY_TOTAL)
        df_tabApplicability_no = create_table_number_answers(df_answeredNO, extract_solution_data(df_iccmas, key_number_no, TITLE_APPLICABILITY_ROW_SOLUTION), key_answer,  
                                        key_benchmarks, NAME_MUTOSKIA, TITLE_APPLICABILITY_ROW_SOLUTION, key_solvers, TITLE_APPLICABILITY_PERCENTAGE, TITLE_APPLICABILITY_TOTAL)
        if(PRINT_APP_YES):
            print()
            print("----------------- applicability YES -----------------")    
            print(df_tabApplicability_yes)
        if(PRINT_APP_NO):
            print()
            print("----------------- applicability NO -----------------")  
            print(df_tabApplicability_no)

        if(SAVE_LATEX):
            latex_code = create_general_latex(df_tabApplicability_yes, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            latex_code = add_midrule_above_pattern(latex_code, "solution")
            __save_latex_file(output_directory, "Analysis_Applicability_Yes.tex", latex_code)

            latex_code = create_general_latex(df_tabApplicability_no, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            latex_code = add_midrule_above_pattern(latex_code, "solution")
            __save_latex_file(output_directory, "Analysis_Applicability_No.tex", latex_code)
        
        
    if(CALCULATE_OVERLAP):
        #-------------------------------- OVERLAP --------------------------------
        # create the tables for visualizing the overlap of the applicability of the different solvers
        df_tabOverlap_int_yes = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_YES, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, NUM_DIGITS_PCT, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_INT)
        df_tabOverlap_pct_yes = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_YES, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, NUM_DIGITS_PCT, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_PCT)
        df_tabOverlap_formatted_yes = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_YES, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, NUM_DIGITS_PCT, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_FORMATTED)

        if(PRINT_OVERLAP_INT_YES):
            print()
            print("----------------- overlap INT YES -----------------")
            print(df_tabOverlap_int_yes)
        if(PRINT_OVERLAP_PCT_YES):
            print()
            print("----------------- overlap PCT YES -----------------")
            print(df_tabOverlap_pct_yes)
        if(PRINT_OVERLAP_FORMATTED_YES):
            print()
            print("----------------- overlap FORMATTED YES -----------------")
            print(df_tabOverlap_formatted_yes)

        df_tabOverlap_int_no = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_NO, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, NUM_DIGITS_PCT, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_INT)
        df_tabOverlap_pct_no = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_NO, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, NUM_DIGITS_PCT, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_PCT)
        df_tabOverlap_formatted_no = create_table_overlap(df_rawAnswered, key_answer, NAME_ANSWER_NO, key_benchmarks, key_instance, NAME_MUTOSKIA, key_solvers, NUM_DIGITS_PCT, SUFFIX_PERCENTAGE, TABLE_FORMAT_OVERLAP_FORMATTED)

        if(PRINT_OVERLAP_INT_NO):
            print()
            print("----------------- overlap INT NO -----------------")
            print(df_tabOverlap_int_no)
        if(PRINT_OVERLAP_PCT_NO):
            print()
            print("----------------- overlap PCT NO -----------------")
            print(df_tabOverlap_pct_no)
        if(PRINT_OVERLAP_FORMATTED_NO):
            print()
            print("----------------- overlap FORMATTED NO -----------------")
            print(df_tabOverlap_formatted_no)

        if(SAVE_LATEX):
            latex_code = create_general_latex(df_tabOverlap_int_yes, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Overlap_Integer_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabOverlap_pct_yes, NUM_DIGITS_PCT, "%", NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Overlap_Percentage_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabOverlap_formatted_yes, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Overlap_Formatted_Yes.tex", latex_code)
            
            latex_code = create_general_latex(df_tabOverlap_int_no, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Overlap_Integer_No.tex", latex_code)
            latex_code = create_general_latex(df_tabOverlap_pct_no, NUM_DIGITS_PCT, "%", NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Overlap_Percentage_No.tex", latex_code)
            latex_code = create_general_latex(df_tabOverlap_formatted_no, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Overlap_Formatted_No.tex", latex_code)

    if(CALCULATE_RT_INTERSEC):
        #-------------------------------- RUNTIME INTERSECTION --------------------------------
        # filter out all rows of the solver 'asc_01'
        df_rawAnsweredNoASC01 = df_answeredNO[df_answeredNO['solver_name'] != 'asc_01']
        # analyze runtime of the intersection of instances of solved instances of solvers
        df_tabRuntime_intersect_yes = create_table_runtime_intersection(df_answeredYES, key_answer, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, timeout, NUM_STD_LIMIT, False,
                            TITLE_SOLVER_VBS, TITLE_INSTANCES, TITLE_RUNTIME_MEAN, TITLE_RUNTIME_STD, TITLE_RUNTIME_SUM, TITLE_RUNTIME_MEAN_CAPPED, TITLE_RUNTIME_STD_CAPPED, TITLE_RUNTIME_SUM_CAPPED, TITLE_VBS_COUNT, DELTA_PERCENTAGE)
        df_tabRuntime_intersectNoASC01_no = create_table_runtime_intersection(df_rawAnsweredNoASC01, key_answer, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, timeout, NUM_STD_LIMIT, True,
                            TITLE_SOLVER_VBS, TITLE_INSTANCES, TITLE_RUNTIME_MEAN, TITLE_RUNTIME_STD, TITLE_RUNTIME_SUM, TITLE_RUNTIME_MEAN_CAPPED, TITLE_RUNTIME_STD_CAPPED, TITLE_RUNTIME_SUM_CAPPED, TITLE_VBS_COUNT, DELTA_PERCENTAGE)
        
        if(PRINT_RT_INTERSEC_YES):
            print()
            print("----------------- runtime intersection YES -----------------")
            print(df_tabRuntime_intersect_yes)

        if(PRINT_RT_INTERSEC_NO):
            print()
            print("----------------- runtime intersection NO (no asc_01) -----------------")
            print(df_tabRuntime_intersectNoASC01_no)

        if(SAVE_LATEX):
            latex_code = create_general_latex(df_tabRuntime_intersect_yes, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Intersection_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_intersectNoASC01_no, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Intersection_No.tex", latex_code)
        
    if(CACLCULATE_RT_COMP_MUTOKSIA):
        df_tabRuntime_comparison_muToksia = create_table_runtime_comparison_mutoksia(df_rawAnswered, key_answer, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, NUM_DIGITS_PCT, 1, timeout, 
                                                                                     TITLE_SOLVER_VBS, TITLE_RUNTIME_SUM, TITLE_RUNTIME_SUM_PCT, TITLE_VBS_COUNT, TITLE_VBS_COUNT_PCT, DELTA_PERCENTAGE)
        if(PRINT_RT_COMP_MUTOKSIA):
            print()
            print("----------------- runtime comparison MuToksia -----------------")
            print(df_tabRuntime_comparison_muToksia)

        if(SAVE_LATEX):
            latex_code = create_general_latex(df_tabRuntime_comparison_muToksia, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_MuToksia.tex", latex_code)

    if(CALCULATE_RT_COMP):
        #-------------------------------- RUNTIME COMPARISON --------------------------------
        df_tabRuntime_comparisonYes = create_table_runtime_comparison(df_answeredYES, key_answer, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, NUM_DIGITS_STD, 
                                                                      NUM_DIGITS_SUM, timeout, TITLE_SOLVER_VBS, DELTA_PERCENTAGE)
        df_tabRuntime_comparisonNo = create_table_runtime_comparison(df_answeredNO, key_answer, key_benchmarks, key_exit_with_error, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, 
                                                                     NUM_DIGITS_STD, NUM_DIGITS_SUM, timeout, TITLE_SOLVER_VBS, DELTA_PERCENTAGE)
        

        if(PRINT_RT_COMP_YES):
            print()
            print("----------------- runtime comparison YES -----------------")
            print(" - mean -")
            print(df_tabRuntime_comparisonYes[0])
            print()
            print(" - mean difference -")
            print(df_tabRuntime_comparisonYes[1])
            print()
            print(" - std -")
            print(df_tabRuntime_comparisonYes[3])
            print()
            print(" - sum -")
            print(df_tabRuntime_comparisonYes[4])
            print()
            print(" - sum difference -")
            print(df_tabRuntime_comparisonYes[5])
            print()
            print(" - mean/sum procentual -")
            print(df_tabRuntime_comparisonYes[2])
            print()
            print(" - #VBS -")
            print(df_tabRuntime_comparisonYes[6])

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

        if(SAVE_LATEX):
            latex_code = create_general_latex(df_tabRuntime_comparisonYes[0], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Mean_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonYes[1], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_MeanDiff_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonYes[2], NUM_DIGITS_PCT, "%", NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Percentage_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonYes[3], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Std_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonYes[4], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Sum_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonYes[5], NUM_DIGITS_SUM, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_SumDiff_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonYes[6], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_VBSCount_Yes.tex", latex_code)

            latex_code = create_general_latex(df_tabRuntime_comparisonNo[0], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Mean_No.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonNo[1], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_MeanDiff_No.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonNo[2], NUM_DIGITS_PCT, "%", NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Percentage_No.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonNo[3], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Std_No.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonNo[4], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_Sum_No.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonNo[5], NUM_DIGITS_SUM, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_SumDiff_No.tex", latex_code)
            latex_code = create_general_latex(df_tabRuntime_comparisonNo[6], NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Comparison_VBSCount_No.tex", latex_code)


    if(CALCULATE_BL):
        #-------------------------------- BALANCE --------------------------------
        df_tab_balance_all = create_table_balance_sheet(df_rawAnswered, key_answer, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, NUM_DIGITS_PCT, 
                                                        TITLE_BALANCE, TITLE_BALANCE_PCT_CHANGE, TITLE_BALANCE_SUM_RT, TITLE_SOLVER_VBS, TITLE_VBS_COUNT, TITLE_VBS_COUNT_PCT, DELTA_PERCENTAGE)
        df_tab_balance_yes = create_table_balance_sheet(df_answeredYES, key_answer, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, NUM_DIGITS_PCT, 
                                                        TITLE_BALANCE, TITLE_BALANCE_PCT_CHANGE, TITLE_BALANCE_SUM_RT, TITLE_SOLVER_VBS, TITLE_VBS_COUNT, TITLE_VBS_COUNT_PCT, DELTA_PERCENTAGE)
        df_tab_balance_no = create_table_balance_sheet(df_answeredNO, key_answer, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, NUM_DIGITS_PCT, 
                                                       TITLE_BALANCE, TITLE_BALANCE_PCT_CHANGE, TITLE_BALANCE_SUM_RT, TITLE_SOLVER_VBS, TITLE_VBS_COUNT, TITLE_VBS_COUNT_PCT, DELTA_PERCENTAGE)

        if(PRINT_BL_ALL):
            print()
            print("----------------- Balance all -----------------")
            print(df_tab_balance_all)

        if(PRINT_BL_YES):
            print()
            print("----------------- Balance only YES -----------------")
            print(df_tab_balance_yes)

        if(PRINT_BL_NO):
            print()
            print("----------------- Balance only NO -----------------")
            print(df_tab_balance_no)

        if(SAVE_LATEX):   
            latex_code = create_general_latex(df_tab_balance_all, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            latex_code = add_midrule_above_pattern(latex_code, TITLE_SOLVER_VBS)
            __save_latex_file(output_directory, "Analysis_Runtime_Balance_All.tex", latex_code)
            latex_code = create_general_latex(df_tab_balance_yes, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Balance_Yes.tex", latex_code)
            latex_code = create_general_latex(df_tab_balance_no, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Balance_No.tex", latex_code)


    if(CALCULATE_BL_COMBI):
        #-------------------------------- BALANCE COMBI --------------------------------
        single_solvers = ('asc_01','asc_02','asc_03','asc_04')
        combi_01 = ('asc_01','asc_02')
        combi_02 = ('asc_01','asc_02','asc_03','asc_04')
        combi_03 = ('asc_04','asc_01','asc_02','asc_03')
        list_combi = (combi_01, combi_02, combi_03)
        df_table_balance_combi = create_table_balance_sheet_combination(df_rawAnswered, key_answer, key_instance, NAME_MUTOSKIA, key_runtime, key_solvers, 
                                                                        TITLE_BALANCE, TITLE_BALANCE_PCT_CHANGE, TITLE_BALANCE_SUM_RT, 
                                                                        single_solvers, list_combi)
        if(PRINT_BL_COMBI):
            print()
            print("----------------- Balance combinations -----------------")
            print(df_table_balance_combi)

        if(SAVE_LATEX):
            latex_code = create_general_latex(df_table_balance_combi, NUM_DIGITS, None, NAME_PREFIX_ASC_LATEX)
            __save_latex_file(output_directory, "Analysis_Runtime_Balance_Combi.tex", latex_code)
    