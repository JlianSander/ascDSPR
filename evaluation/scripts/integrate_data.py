import sys
import os
import pandas as pd

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
    if len(sys.argv) != 4:
        print("Usage: python3 analysis.py <file_path_raw> <file_path_raw_new_data> <file_path_output_raw>")
        sys.exit(1)
    
    #-------------------------------- initializing data --------------------------------

    # read paths to data
    file_path_raw = sys.argv[1]
    file_path_newData = sys.argv[2]
    file_path_output = sys.argv[3]
    
    # read data frame of raw results from probo
    df_raw = read_csv_to_dataframe(file_path_raw)
    df_newData = read_csv_to_dataframe(file_path_newData)

    print()
    print("-----------------------------------------------------------------")
    print("df_raw:")
    print(df_raw)

    print()
    print("-----------------------------------------------------------------")
    print("df_newData:")
    print(df_newData)

    # read keys from input data frames
    key_benchmarks = df_raw.columns[15]  #'benchmark_name'
    key_instance = df_raw.columns[4] #'instance'
    key_solvers = df_raw.columns[0] #'solver_name'

    # delete rows of solvers in old data
    for solver in df_newData[key_solvers].unique():
        df_raw = df_raw[df_raw[key_solvers] != solver]

    df_raw = pd.concat([df_raw, df_newData], axis=0, ignore_index=True)

    print()
    print("-----------------------------------------------------------------")
    print("df_Output:")
    print(df_raw)

    df_raw.to_csv(file_path_output, index=False)