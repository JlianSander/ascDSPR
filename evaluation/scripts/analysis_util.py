import sys
import pandas as pd

def filter_by_answer(df_rawAnswered, key_answer, key_answerType):
    # filter to keep only rows with an answer similiar to the given answerType
    return df_rawAnswered[df_rawAnswered[key_answer] == key_answerType]