import pandas as pd

def load_icpsr(path):
    '''
    Load the ICPSR data
    returns: dictionnary with alcohol per capita consumption by country each year between 2001 and 2017
    '''
    years = list(range(2001, 2018))
    df = pd.read_csv(path)
    dict_icpsr = {}
    df.columns = df.columns.str.strip()
    df = df[df['year'].isin(years)]
    #make the first letter of the state column uppercase
    df['state'] = df['state'].str.capitalize()
    df = df[['year', 'state', 'ethanol_beer_gallons_per_capita', 'number_of_beers']]
    #separate the data by year, and use the year as key in dictionnary
    for year in years:
        dict_icpsr[str(year)] = df[df['year'] == year].drop(columns=['year']).reset_index(drop=True)
    
    return dict_icpsr

def load_urban_frac_df(path, filename):
    """ loads and cleans datasets from census.org about urban population 
    Additionnaly calculates the fraction of urban population

    Args:
        path (string): path where the raw dataset is saved
        filename (string): filename of csv file

    Returns:
        pd.df: dataframe with urban_pop, rural_pop, urban_frac data per US-state
    """
    urban_df = pd.read_csv(path + filename, index_col=0)
    # delete inside urban clusters and urbanized
    if len(urban_df.index) == 6:
        urban_df = urban_df.drop(urban_df.index[2:4], axis='rows')

    urban_df = (
        urban_df
        .drop(urban_df.index[-1], axis='rows')  # droping not defined for this file
        .rename(index={urban_df.index[0]: 'total_pop', 
                    urban_df.index[1]: 'urban_pop', 
                    urban_df.index[2]: 'rural_pop'})
        .transpose()
        .apply(lambda x : x.str.replace(',', ''))   # get rid of commas in US number format
        .apply(lambda x : x.str.split(' \(r').str[0]) 
        .apply(pd.to_numeric)   
    )
    urban_df.index.names = ['state']
    urban_df.columns.names = [None]

    urban_df['urban_frac'] = urban_df['urban_pop'] / urban_df['total_pop']

    return urban_df

def merge_census_years(dfs, suffixes):
    # ! ne fonctionne pas
    merged = dfs[0].merge(dfs[1], how='inner', on='state', suffixes=suffixes[0:2])
    if len(dfs) > 3:
        for i in range(len(dfs)-2):     # 2 firs already merged
            # will not work as no overlapping
            merged.merge(dfs[i+2], how='inner', on='state', suffixes=['', suffixes[i+2]])

    return merged

def load_age_data(path, load_gender=False):
    '''
    Load the age data, filtered so only over 21 years old remain
    inputs:
        - path: path to the csv file
        - load_gender: boolean, if True additionally returns 2 dataframes for male and female
    returns: dataframe with age data, totale if load_gender is False, else 3 dataframes
    
    '''
    df = pd.read_csv(path)
    df = df.T

    df.reset_index(inplace=True)
    df.columns = df.iloc[0]
    df = df[1:]
    #replace label of first column by "state"
    df.columns.values[0] = 'state'
    #remove all unwanted characters
    df.columns = df.columns.str.strip() #remove spaces at beginning and end of columns
    pd.set_option('future.no_silent_downcasting', True)
    df = df.replace(',', '', regex=True)
    df = df.replace('!!', ' ', regex=True)
    df = df.drop(columns=['SEX AND AGE', 'VACANCY RATES', 'HOUSING TENURE', 'Under 5 years', '5 to 9 years', '10 to 14 years', '15 to 19 years'])

    #remove % and convert to decimal
    df = df.map(lambda x: float(x.replace('%', ''))/100 if '%' in str(x) else x)

    df_total = df.iloc[:, :16]
    if not load_gender:
        return df_total
    else:
        df_male = pd.concat([df['state'], df.iloc[:, 22:37]], axis=1)
        df_female = pd.concat([df['state'], df.iloc[:, 43:58]], axis=1)
        return df_total, df_male, df_female

def loadBEA(path, filename, income_name={}):
    """loads and arranges csv from BEA containing info about incomes per state and years

    Args:
        path (string): path where the raw dataset is saved
        filename (string): filename of csv file
        income_name (dict): dict with name for the Income type (String : int (1 to 15))

    Returns:
        pd.df: loaded dataframe, multiindex ['State', 'Year'] and one column per indicator
    """

    col_dict = {v: k for k, v in income_name.items()}

    df = pd.read_csv(path+filename, header=3)

    df = (
        df 
        .set_index(['GeoName', 'LineCode'])   # creating multiindex
        .drop(['GeoFips', 'Description'], axis=1)   # are redundant
        .dropna(axis=0, thresh=3)               # both indexes
        .stack()                           
        .rename_axis(index={'GeoName': 'State', 'LineCode': 'Income', None: 'Year'})
        .unstack(level=['Income'])            # to get years as index and indicators as columns
        .rename(columns=col_dict)           # rename columns
        .apply(pd.to_numeric, errors='coerce') 
    )

    return df
