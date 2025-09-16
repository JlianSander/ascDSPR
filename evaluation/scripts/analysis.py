import sys

import pandas as pd

# Method to extract the number of instances with a given answer for each benchmark as a row
def extract_solution_data(df_iccmas, solution_type):
    """
    Extracts solution data for a given solution type ('YES' or 'NO') and returns the corresponding row.
    
    Parameters:
    - df_iccmas: DataFrame containing the benchmark data
    - solution_type: String, either 'YES' or 'NO' to extract corresponding solution data
    
    Returns:
    - dfrow_solution: A DataFrame containing the extracted solution data for the given type
    """
    if solution_type == "YES":
        s_solution = df_iccmas['number_yes']
    elif solution_type == "NO":
        s_solution = df_iccmas['number_no']
    else:
        raise ValueError("solution_type must be either 'YES' or 'NO'")

    dfrow_solution = pd.DataFrame(s_solution).T  # .T transposes the series to match the row format
    dfrow_solution.index = ['solution']
    
    return dfrow_solution

# Method to create a table counting the answers of a given type for each solver
def create_table_number_answers(answerType, df_answers, dfrow_solution, dfrow_total_instances):
    """
    Processes the answers, calculates percentages, and returns the updated DataFrame.
    
    Parameters:
    - answerType: string containing 'NO' or 'YES' to indicate which answers are to be processed
    - df_answers: DataFrame containing the answers for each solver and benchmark
    - dfrow_solution: Row containing the number of NO-solutions
    - dfrow_total_instances: Row containing the total number of instances
    
    Returns:
    - df_answers_tmp: DataFrame with the number of answers for each solver, the total instances, and the percentages of answers found of the solver compared to the solution
    """
    # Filter out only those rows with answer {answerType}
    df_answers_tmp = df_answers.xs(answerType, level='answer')
    
    # Reorder position of rows so that 'mu-toksia' is at the top
    dfrow_mu = df_answers_tmp.loc[['mu-toksia-glucose']]
    df_answers_tmp = df_answers_tmp.drop('mu-toksia-glucose')
    df_answers_tmp = pd.concat([dfrow_mu, df_answers_tmp])
    
    # Add row for total number of instances and row of the solutions to the dataframe
    df_answers_tmp = pd.concat([dfrow_solution, df_answers_tmp])
    df_answers_tmp = pd.concat([dfrow_total_instances, df_answers_tmp])
    
    # Calculate the sum of the 'solution' row 
    solution_sum = df_answers_tmp.loc['solution'].sum()
    
    # Add an empty column 'percentage'
    df_answers_tmp['percentage'] = None
    
    # Calculate the percentage for each row (except 'solution')
    for index in df_answers_tmp.index:
        if index != 'number_instances':
            row_sum = df_answers_tmp.loc[index].sum()
            percentage = (row_sum / solution_sum) * 100
            df_answers_tmp.loc[index, 'percentage'] = percentage
    
    return df_answers_tmp 


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
    
    # read paths to data
    file_path_raw = sys.argv[1]
    file_path_resultsDetails = sys.argv[2]
    file_path_iccmas = sys.argv[3]
    output_file = sys.argv[4]
    
    # read data frames
    df_raw = read_csv_to_dataframe(file_path_raw)
    df_resDetails = read_csv_to_dataframe(file_path_resultsDetails)
    df_iccmas = read_csv_to_dataframe(file_path_iccmas)
    df_iccmas = df_iccmas.set_index('benchmark_name')

    # get the total number of instances as a row
    s_total_instances = df_iccmas['number_instances']
    dfrow_total_instances = pd.DataFrame(s_total_instances).T  # .T transposes the series to match the row format
    #dfrow_total_instances.index = [('number_instances', '')]  # Set the correct index for the new row to match the multi-index structure of df_answers
    #print(dfrow_total_instances) #DEBUG

    # merge answers with raw data
    df_rawAnswered = pd.merge(df_raw, df_resDetails, on=['solver_name','task','benchmark_name','instance'], how='left')
     
    # count answers for each solver and each benchmark
    df_rawSolvBench = df_rawAnswered.groupby(['solver_name','benchmark_name'])
    df_answers = df_rawSolvBench['answer'].value_counts().unstack(level=1)
    df_answers = df_answers.fillna(0).astype('int')
    #print(df_answers) #DEBUG

    # create the tables for visualizing the number of answered found by each solver
    print(create_table_number_answers("YES", df_answers, extract_solution_data(df_iccmas, 'YES'), dfrow_total_instances))
    print(create_table_number_answers("NO", df_answers, extract_solution_data(df_iccmas, 'NO'), dfrow_total_instances))

    


    # #DEBUG
    # stop=False
    # # iterate through each combination of solver and benchmark
    # for (solver, benchmark), subdf in df_rawSolvBench:
    #     #DEBUG
    #     if stop==True: break

    #     print(f"Processing solver: {solver}, benchmark: {benchmark}")
    
    #     if solver not in df_answers.index.get_level_values(0):
    #         continue
        
    #     s_answers = df_answers.loc[(solver, benchmark)]

    #     # Check if 'No' exists in the index
    #     if 'NO' in s_answers.index:
    #         #print(f"'NO' exists in the index for solver {solver}, benchmark {benchmark}")
            
    #         answers_solver = s_answers['NO']
    #         answers_solution = df_iccmas.loc[benchmark]['number_no']
    #         print(f"{answers_solver}/{answers_solution}")

        
        #if 'YES' in s_answers.index:
            #print(f"'YES' exists in the index for solver {solver}, benchmark {benchmark}")

        #DEBUG
        #stop=True

    
    #TODO set number of answers in relation to total number of instances in data set
    


    # group DataFrame by the solver name
    #grouped_dataframe = df_rawAnswered.groupby("solver_name")
    # # Create a table with one row for each group
    # table_data = []
    # timeout = df_raw.loc[0,"cut_off"]
    # X_in_parX = 2
    # for name, group in grouped_dataframe:
    #     nb_rows = len(group)
    #     nb_timeouts = group["runtime"].eq(timeout).sum()
    #     nb_empty_runtime_rows = group['runtime'].isna().sum() + (group['runtime'] == '').sum()
    #     nb_rt_too_high = group["runtime"].apply(lambda x: (x > timeout)).sum()
    #     nb_errors = nb_empty_runtime_rows + nb_rt_too_high
    #     nb_timeout_counted = nb_timeouts + nb_rt_too_high
    #     nb_timeouts_all = nb_timeout_counted + nb_empty_runtime_rows
        
    #     delta_rt_too_high = group.loc[group["runtime"] > timeout, "runtime"].sum() - nb_rt_too_high * timeout
    #     sum_rt_correct = group["runtime"].sum() - delta_rt_too_high

    #     runtime_solved = sum_rt_correct - nb_timeout_counted * timeout
    #     average_runtime_solved = runtime_solved / (nb_rows - nb_timeouts_all)
    #     average_runtime = (sum_rt_correct + nb_empty_runtime_rows * timeout)/ nb_rows
    #     par_X = (runtime_solved + (nb_timeouts_all * X_in_parX * timeout)) / nb_rows
    #     table_data.append([name, nb_rows, nb_timeouts, round(runtime_solved, 2), round(average_runtime_solved, 2),round(average_runtime, 2), par_X, nb_errors, delta_rt_too_high])
    # table_df = pd.DataFrame(table_data, columns=["Algorithm", "N", "#TO", "RTslv", "avgRTslv", "avgRT", "PAR"+ str(X_in_parX), "#err", "RTerr"])
    
    # Save table to file
    #table_df.to_latex(output_file + '_table.tex', index=False) 
    