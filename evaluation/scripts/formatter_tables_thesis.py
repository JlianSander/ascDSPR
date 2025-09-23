import sys
import pandas as pd
import re

#---------------------------------------------------------------------------------------------------------------------------

# Function to replace 'asc_0x' with '\Sc{x}' 
def replace_asc_labels(latex_code, prefix_replacement):
    # Regular expression to find 'asc_0x' where x is a number from 1 to 9
    pattern = r'asc\\_0([1-9])'
    pattern_10 = r'asc\\_(\d+)'

    # Function to replace 'asc_0x' with '\Sc{x}'
    updated_latex_table = re.sub(pattern, rf'\\{prefix_replacement}{{\1}}', latex_code)
    updated_latex_table = re.sub(pattern_10, rf'\\{prefix_replacement}{{\1}}', updated_latex_table)
    
    return updated_latex_table


#---------------------------------------------------------------------------------------------------------------------------


def create_general_latex(df, num_digits, suffix, asc_label_prefix): 
    
    
    # round all float values to have the given number of digits
    df = df.apply(lambda x: x.round(num_digits) if x.dtype == 'float64' else x)
    if num_digits == 0:
        df = df.fillna(0).astype('int')
    else:
        df = df.fillna('')

    # add the given suffix to all values of the data frame
    if suffix is not None:
        df = df.applymap(lambda x: x.__str__() + "%")

    # Convert the DataFrame to LaTeX format
    latex_code = df.to_latex(index=True)  # index=False to exclude the DataFrame index
    #df.to_latex(file_path, index=False) 
    
    # Replace names of shortcuts with the custom command of the thesis
    updated_latex_table = replace_asc_labels(latex_code, asc_label_prefix)

    return updated_latex_table


#---------------------------------------------------------------------------------------------------------------------------
 
def add_midrule_above_pattern(latex_code, pattern):
    
    #ensure find only single words
    pattern_single_word = "\b"+pattern+"(\b|\n)?"

    # Function to replace 'asc_0x' with '\Sc{x}'
    updated_latex_table = re.sub(pattern_single_word, rf'\\midrule\n{pattern}', latex_code)

    #if word was first in row
    pattern_single_word = "\n"+pattern+"(\b|\n)?"

    updated_latex_table = re.sub(pattern_single_word, rf'\n\\midrule\n{pattern}', latex_code)
    
    return updated_latex_table