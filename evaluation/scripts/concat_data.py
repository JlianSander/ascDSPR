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
        print("Usage: python3 concatenate_data.py <file_path_raw_up> <file_path_raw_below> <file_path_output_raw>")
        sys.exit(1)
    
    #-------------------------------- initializing data --------------------------------

    # read paths to data
    file_path_raw_first = sys.argv[1]
    file_path_raw_second = sys.argv[2]
    file_path_output = sys.argv[3]
    
    # read data frame of raw results from probo
    df_raw_first = read_csv_to_dataframe(file_path_raw_first)
    df_raw_second = read_csv_to_dataframe(file_path_raw_second)

    print()
    print("-----------------------------------------------------------------")
    print("df_raw_first:")
    print(df_raw_first)

    print()
    print("-----------------------------------------------------------------")
    print("df_raw_second:")
    print(df_raw_second)

    # read keys from input data frames
    key_benchmarks = df_raw_first.columns[15]  #'benchmark_name'
    key_instance = df_raw_first.columns[4] #'instance'
    key_solvers = df_raw_first.columns[0] #'solver_name'

    df_raw_first = pd.concat([df_raw_first, df_raw_second], axis=0, ignore_index=True)

    print()
    print("-----------------------------------------------------------------")
    print("df_Output:")
    print(df_raw_first)

    df_raw_first.to_csv(file_path_output, index=False)