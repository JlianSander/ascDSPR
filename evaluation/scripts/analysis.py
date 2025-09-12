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
    if len(sys.argv) != 4:
        print("Usage: python3 analysis.py <file_path_raw> <file_path_resultsDetails> <output_file>")
        sys.exit(1)
    
    file_path_raw = sys.argv[1]
    file_path_resultsDetails = sys.argv[2]
    output_file = sys.argv[3]
    
    df_raw = read_csv_to_dataframe(file_path_raw)
    df_resDetails = read_csv_to_dataframe(file_path_resultsDetails)
    #print(df_raw.info())
    #print(df_resDetails.info())

    df_resDetails = df_resDetails.rename(columns={'result':'answer'})
    df_resDetails = df_resDetails.rename(columns={'dataset':'benchmark_name'})
    df_rawAnswered = pd.merge(df_raw, df_resDetails, on=['solver_name','task','benchmark_name','instance'], how='left')
    #print(df_rawAnswered.info())

     
    # group DataFrame by the solver name
    grouped_dataframe = df_rawAnswered.groupby("solver_name")
    # number of answers over all data sets per solver
    #print(grouped_dataframe['answer'].value_counts())
    # number of all instances of each solver
    #print(grouped_dataframe.size())

    df_groupDouble = df_rawAnswered.groupby(['solver_name','benchmark_name'])
    # number of  answers per data set and per solver
    df_answerCount = df_groupDouble['answer'].value_counts().unstack(level=1)
    print(df_answerCount)
    df_datasetInstTotal = df_groupDouble.size()
    #TODO how to iterate over the double grouped dataframe
    #TODO set number of answers in relation to total number of instances in data set
    
    # Create a table with one row for each group
    table_data = []
    timeout = df_raw.loc[0,"cut_off"]
    X_in_parX = 2
    for name, group in grouped_dataframe:
        nb_rows = len(group)
        nb_timeouts = group["runtime"].eq(timeout).sum()
        nb_empty_runtime_rows = group['runtime'].isna().sum() + (group['runtime'] == '').sum()
        nb_rt_too_high = group["runtime"].apply(lambda x: (x > timeout)).sum()
        nb_errors = nb_empty_runtime_rows + nb_rt_too_high
        nb_timeout_counted = nb_timeouts + nb_rt_too_high
        nb_timeouts_all = nb_timeout_counted + nb_empty_runtime_rows
        
        delta_rt_too_high = group.loc[group["runtime"] > timeout, "runtime"].sum() - nb_rt_too_high * timeout
        sum_rt_correct = group["runtime"].sum() - delta_rt_too_high

        runtime_solved = sum_rt_correct - nb_timeout_counted * timeout
        average_runtime_solved = runtime_solved / (nb_rows - nb_timeouts_all)
        average_runtime = (sum_rt_correct + nb_empty_runtime_rows * timeout)/ nb_rows
        par_X = (runtime_solved + (nb_timeouts_all * X_in_parX * timeout)) / nb_rows
        table_data.append([name, nb_rows, nb_timeouts, round(runtime_solved, 2), round(average_runtime_solved, 2),round(average_runtime, 2), par_X, nb_errors, delta_rt_too_high])
    table_df = pd.DataFrame(table_data, columns=["Algorithm", "N", "#TO", "RTslv", "avgRTslv", "avgRT", "PAR"+ str(X_in_parX), "#err", "RTerr"])
    
    # Save table to file
    #table_df.to_latex(output_file + '_table.tex', index=False) 
    