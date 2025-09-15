import sys

import pandas as pd


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
    
    file_path_raw = sys.argv[1]
    file_path_resultsDetails = sys.argv[2]
    file_path_iccmas = sys.argv[3]
    output_file = sys.argv[4]
    
    df_raw = read_csv_to_dataframe(file_path_raw)
    df_resDetails = read_csv_to_dataframe(file_path_resultsDetails)
    df_iccmas = read_csv_to_dataframe(file_path_iccmas)
    df_iccmas = df_iccmas.set_index('benchmark_name')
    #print(df_raw.info())
    #print(df_resDetails.info())
    print(df_iccmas)

    df_rawAnswered = pd.merge(df_raw, df_resDetails, on=['solver_name','task','benchmark_name','instance'], how='left')
    #print(df_rawAnswered.info())
    #print(df_rawAnswered)

     
    # group DataFrame by the solver name
    grouped_dataframe = df_rawAnswered.groupby("solver_name")
    

    # number of answers over all data sets per solver
    #print(grouped_dataframe['answer'].value_counts())
    # number of all instances of each solver
    #print(grouped_dataframe.size())

    df_groupDouble = df_rawAnswered.groupby(['solver_name','benchmark_name'])
    # number of  answers per data set and per solver
    df_answerCount = df_groupDouble['answer'].value_counts().unstack(level=1)
    df_answerCount = df_answerCount.fillna(0).astype('int')
    print(df_answerCount)
    
    #DEBUG
    stop=False
    # iterate through each combination of solver and benchmark
    for (solver, benchmark), subdf in df_groupDouble:
        #DEBUG
        if stop==True: break

        print(f"Processing solver: {solver}, benchmark: {benchmark}")
    
        if solver not in df_answerCount.index.get_level_values(0):
            continue
        
        s_answers = df_answerCount.loc[(solver, benchmark)]

        # Check if 'No' exists in the index
        if 'NO' in s_answers.index:
            #print(f"'NO' exists in the index for solver {solver}, benchmark {benchmark}")
            
            answers_solver = s_answers['NO']
            answers_solution = df_iccmas.loc[benchmark]['number_no']
            print(f"{answers_solver}/{answers_solution}")

        
        #if 'YES' in s_answers.index:
            #print(f"'YES' exists in the index for solver {solver}, benchmark {benchmark}")

        #DEBUG
        stop=True

    
    #TODO set number of answers in relation to total number of instances in data set
    
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
    