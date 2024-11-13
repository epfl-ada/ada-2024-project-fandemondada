import pandas as pd

def remove_txt_columns(data_ba, data_rb, data_matched):
    """
    Remove textual review columns from the dataframes
    Inputs:
        - data_ba: dictionary containing the BeerAdvocate dataframes
        - data_rb: dictionary containing the RateBeer dataframes
        - data_matched: dictionary containing the Matched dataframes
    Outputs:
        - data_ba, data_rb, data_matched: dictionaries containing the dataframes without the textual review columns
    """
    for key in data_ba.keys():
        #check if the dataframe has the text column
        if 'text' in data_ba[key].columns:
            data_ba[key] = data_ba[key].drop(columns=['text'])
            
    for key in data_rb.keys():
        #check if the dataframe has the text column
        if 'text' in data_rb[key].columns:
            data_rb[key] = data_rb[key].drop(columns=['text'])
            
    for key in data_matched.keys():
        #check if the dataframe has the text column
        if 'text' in data_matched[key].columns:
            data_matched[key] = data_matched[key].drop(columns=['text'])
    return 