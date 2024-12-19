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

def merge_reviews(data_ba, data_rb, data_matched):
    """
    Merge the BeerAdvocate and RateBeer dataframes by removing the matched data from RateBeer data so reviews do not appear twice
    Inputs:
        - data_ba: dataframe with BeerAdvocate data
        - data_rb: dataframe with RateBeer data
        - data_matched: dataframe with matched data
    Outputs:
        - beer_data: conbined dataframes without double reviews
    """
    data_matched_renamed = data_matched[['rb_beer_id', 'rb_user_id']].rename(columns={
    'rb_beer_id': 'beer_id',
    'rb_user_id': 'user_id'
    })
    data_rb['beer_id'] = data_rb['beer_id'].astype(int)
    data_rb['user_id'] = data_rb['user_id'].astype(str)
    data_matched_renamed['beer_id'] = data_matched_renamed['beer_id'].astype(int)
    data_matched_renamed['user_id'] = data_matched_renamed['user_id'].astype(str)
    data_rb = data_rb.merge(data_matched_renamed, on=['beer_id', 'user_id'], how='left', indicator=True)
    data_rb = data_rb[data_rb['_merge'] == 'left_only']
    beer_data = pd.concat([data_ba, data_rb], axis=0, ignore_index=True)
    return beer_data

def merge_breweries(breweries_ba, breweries_rb, breweries_matched):
    breweries_matched_renamed = breweries_matched[['rb_id']].rename(columns={'rb_id': 'brewery_id'})
    breweries_rb = breweries_rb.merge(breweries_matched_renamed, on='brewery_id', how='left', indicator=True)
    breweries_rb = breweries_rb[breweries_rb['_merge'] == 'left_only'].drop(columns='_merge')
    breweries = pd.concat([breweries_ba, breweries_rb], axis=0, ignore_index=True)
    return breweries