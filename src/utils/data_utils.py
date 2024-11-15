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

def get_mutliIndex_sub_df(df, income_index,  years):  
    """helper function to slice a multiindex df. income_index is the second level and years are in a single level column index

    Args:
        df (pd.df): dataframe to slice
        income_index (list or single item): list of indexes of the second level to extract
        years (list or single item): list of column names to extract from df

    Returns:
        pd.df: the extracted datafram
    """
    idx = pd.IndexSlice
    return df.loc[idx[:, years], income_index]