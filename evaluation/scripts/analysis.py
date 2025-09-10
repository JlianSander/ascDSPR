import pandas as pd
import matplotlib.pyplot as plt
import sys

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
        print("Usage: python script.py <file_path> <output_file> <PARX> <timeOut>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_file = sys.argv[2]
    X_in_parX = int(sys.argv[3])
    timeout = int(sys.argv[4])
    
    dataframe = read_csv_to_dataframe(file_path)

    # Group DataFrame by the "name" column
    grouped_dataframe = dataframe.groupby("solver_name")
    
    # Define markers for each group
    markers = ['o', 's', '^', 'x', '*', '+', 'D', 'v', '>', '<']

    # Set up Matplotlib for producing .tex output
    plt.rcParams.update({
        "pgf.texsystem": "pdflatex",
        "pgf.preamble": r"\usepackage{amsmath}"
    })

    # Create figure and axis objects
    fig, ax = plt.subplots()

    # Print the grouped DataFrame
    for i, (name, group) in enumerate(grouped_dataframe):
        group = group.sort_values(by="runtime")
        group = group.reset_index(drop=True)
        ax.plot(group.index, group["runtime"], marker=markers[i % len(markers)], markersize=5, linewidth=1, label=name)

    ax.axhline(y=timeout, color='r', linestyle='--', label=None)

    # Add labels and title
    ax.set_xlabel("Instance")
    ax.set_ylabel("Runtime in s")
    #ax.set_title("Line Plot of Runtime for Each Group")
    ax.legend()

    #ax.set_yscale('log')
    
    # Save plot to file
    if output_file.endswith(".pgf"):
        plt.savefig(output_file, format='pgf')
    elif output_file.endswith(".png"):
        plt.savefig(output_file)
    else:
        raise NameError("Unsupported Output type")
    
    # Create a table with one row for each group
    table_data = []
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
    table_df.to_latex(output_file + '_table.tex', index=False)