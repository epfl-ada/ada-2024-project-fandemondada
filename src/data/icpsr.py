import pandas as pd
import os

def load_icpsr(path):
    '''
    Load the ICPSR data
    returns: dictionnary with alcohol per capita consumption by country each year between 2001 and 2017
    '''
    years = list(range(2001, 2018))
    df = pd.read_csv(path)
    dict_icpsr = {}
    df = df[df['year'].isin(years)]
    #make the first letter of the state column uppercase
    df['state'] = df['state'].str.capitalize()
    
    #separate the data by year, and use the year as key in dictionnary
    for year in years:
        dict_icpsr[str(year)] = df[df['year'] == year].drop(columns=['year']).reset_index(drop=True)
    
    
    return dict_icpsr