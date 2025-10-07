import sys
import pandas as pd
import re
from itertools import count

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

# Function to unify the alignment for each table
def get_alignment(df):
    alignments = []
    alignments.append('l')  # Left alignment for the indexes
    for col in df.columns:
        alignments.append('r')  # Right alignment all other columns

    return ''.join(alignments)

#---------------------------------------------------------------------------------------------------------------------------

def create_general_latex(df : pd.DataFrame, num_digits, suffix, asc_label_prefix, color_row, label_iccma, fill_na): 
           
    # Function to format numbers with commas for thousands and digits
    def format_numbers(val):
        if isinstance(val, (float)):
            return f"{val:,.{num_digits}f}"
        elif isinstance(val, (int)):
            return f"{val:,.0f}" 
        return val

    # Apply the formatting function to the entire DataFrame
    df = df.applymap(format_numbers)
    
    # add the given suffix to all values of the data frame
    if suffix is not None:
        df = df.applymap(lambda x: x.__str__() + "\%")

    # Convert the DataFrame to LaTeX format
    # clean the alignment of the table to create
    alignment = get_alignment(df)
    latex_code = df.to_latex(index=True, column_format=alignment) 

    # after formatting number fill the NaN values
    updated_latex_table = re.sub("nan", fill_na, latex_code)

    # replace invalid symbols
    updated_latex_table = re.sub("_", '\_', updated_latex_table)
    updated_latex_table = re.sub("#", '\#', updated_latex_table)

    # remove signs ' and ) and (
    updated_latex_table = re.sub("'", '', updated_latex_table)

    # replace names
    updated_latex_table = re.sub("mu-toksia-glucose", r"\\muToksia", updated_latex_table)

    # Replace names of shortcuts with the custom command of the thesis
    updated_latex_table = replace_asc_labels(updated_latex_table, asc_label_prefix)

    # replace 'iccma' with correct formatting
    updated_latex_table = re.sub("iccma", label_iccma, updated_latex_table)

    


    # Add coloring of every 2nd row
    c = count(0)
    updated_latex_table = re.sub(r"\\\\", lambda x: f"\\\\\n\\rowcolor{color_row}" if next(c) % 2 == 1 else x.group(), updated_latex_table)

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

#---------------------------------------------------------------------------------------------------------------------------
 
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def remove_last_occurence(latex_code, pattern):
    return rreplace(latex_code, pattern, '', 1)

#---------------------------------------------------------------------------------------------------------------------------
