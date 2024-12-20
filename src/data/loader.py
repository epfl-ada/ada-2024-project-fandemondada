import os
import pandas as pd
import tarfile
import tqdm
import csv
import gzip
import shutil
import datetime

def load(load_path, save_path, clean_load=False):
    """
    Load Extracts tar.gz archives in the given folder and saves them as .csv files.

    Args:
        load_path (str): Path where the .tar.gz files are located.
        save_path (str): Directory to save extracted data.
        clean_load (bool, optional): If True, overwrites existing files. Defaults to False.

    Returns:
        dict[str, pd.DataFrame]: Dictionary with all the extracted dataframes.
    """
    data = {}
    subfolders = {
        "BeerAdvocate": os.path.join(save_path, "BeerAdvocate"),
        "RateBeer": os.path.join(save_path, "RateBeer"),
        "MatchedBeerData": os.path.join(save_path, "MatchedBeerData"),
        "Other": os.path.join(save_path, "Other")
    }
    complete = not clean_load
    
    # Ensure subfolders exist
    for folder in subfolders.values():
        os.makedirs(folder, exist_ok=True)
        if clean_load:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        elif "BeerAdvocate" in folder and len(os.listdir(folder)) < 5:
            complete = False
        elif "RateBeer" in folder and len(os.listdir(folder)) < 5:
            complete = False
        elif "matched_beer_data" in folder and len(os.listdir(folder)) < 9:
            complete = False
    
    if complete:
        for file in subfolders.values():
            if file.endswith('.csv') and not file.contains('usa'):
                data[file.name[:-4]] = pd.read_csv(csv_path, low_memory=False)
        return data

    for folder in os.listdir(load_path):
        if folder.endswith('.tar.gz'):
            tar_files = tarfile.open(os.path.join(load_path, folder), "r:gz")

            for file in tar_files:
                if file.name.endswith(".csv"):
                    subfolder_path = (
                        subfolders["BeerAdvocate"] if "BeerAdvocate" in folder
                        else subfolders["RateBeer"] if "RateBeer" in folder
                        else subfolders["MatchedBeerData"] if "matched_beer_data" in folder
                        else subfolders["Other"]
                    )
                    csv_path = os.path.join(subfolder_path, folder[:-7] + '_' + file.name)

                    if not os.path.exists(csv_path):
                        extracted_file = tar_files.extractfile(file)
                        df = pd.read_csv(extracted_file, low_memory=False)
                        data[file.name] = df
                        df.to_csv(csv_path, index=False)
                    else:
                        data[file.name] = pd.read_csv(csv_path, low_memory=False)


                elif file.name.endswith(".txt.gz"):

                    subfolder_path = (
                        subfolders["BeerAdvocate"] if "BeerAdvocate" in folder
                        else subfolders["RateBeer"] if "RateBeer" in folder
                        else subfolders["MatchedBeerData"] if "matched_beer_data" in folder
                        else subfolders["Other"]
                    )

                    csv_path = os.path.join(subfolder_path, folder[:-7] + '_' + file.name[:-7] + ".csv")
                

                    if not os.path.exists(csv_path):
                        temp_dir = "temp"
                        os.makedirs(temp_dir, exist_ok=True)
                        tar_files.extract(file, path=temp_dir)
                        load_txt(os.path.join(temp_dir, file.name), csv_path)
                        shutil.rmtree(temp_dir)
                        
                    data[file.name] = pd.read_csv(csv_path, low_memory=False)
                    

    return data

def load_txt(file_path, csv_path):
    """
    
    """
    with gzip.open(file_path,'rb') as f:
        reviews = []
        review = {}
        
        for line in tqdm.tqdm(f):
            line = str(line)
           
            if len(line.strip()) <= 5:
                reviews.append(review)
                review = {}
            else:
                field_name, field_value = line.split(':', 1)
                review[field_name.strip()[2:]] = field_value.strip()[:-3]

        file = csv.writer(open(csv_path, 'w'))
        file.writerow(reviews[0].keys())
        for review in tqdm.tqdm(reviews):
            file.writerow(review.values())
    

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


def load_breweries():
    breweries = pd.read_csv("data/clean/BeerAdvocate/breweries.csv")
    breweries = breweries[~breweries["location"].str.contains("<a href")]
    breweries['location'] = breweries['location'].apply(lambda x: x.replace('United States, ', ''))
    breweries['state'] = breweries['location'].apply(lambda x: x.split(', ')[-1])
    breweries.loc[breweries['location'].str.contains('Canada, '), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('Ontario'), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('Quebec'), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('Nova Scotia'), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('Manitoba'), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('British Columbia'), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('Alberta'), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('Newfoundland and Labrador'), 'location'] = 'Canada'
    breweries.loc[breweries['location'].str.contains('United Kingdom, '), 'location'] = 'United Kingdom'
    breweries = breweries.rename(columns={'id': 'brewery_id'})
    
    
    return breweries


def get_ba_beer_merged():
    ba_usa_ratings = pd.read_csv("data/clean/BeerAdvocate/usa_ratings.csv")
    ba_usa_users = pd.read_csv("data/clean/BeerAdvocate/usa_users.csv")

    ba_usa_ratings = ba_usa_ratings.merge(ba_usa_users[['user_id', 'location']], on='user_id', how='left')
    ba_usa_ratings['state'] = ba_usa_ratings['location'].apply(lambda x: x.split(', ')[-1])
    ba_usa_ratings['date'] = ba_usa_ratings['date'].apply(lambda timestamp: datetime.fromtimestamp(timestamp).date())
    # datetime.fromtimestamp(timestamp) 
    return ba_usa_ratings

def get_states_from_df(df):
    """
    Get the unique state names from a df with the United States, prefix
    """
    states = df[df["location"].str.contains("United States,")]["location"].map(lambda x: x.replace("United States, ", "")).unique()
    return states

def merge_ratings_breweries(ratings_df, breweries_df):
    """
    Merge the ratings and breweries with new columns: brewery_state and user_state
    """
    merged_df = ratings_df.merge(breweries_df[['brewery_id', 'state']], on='brewery_id', how='left')
    merged_df = merged_df.rename(columns={'state_x': 'user_state', 'state_y': 'brewery_state'})
    merged_df = merged_df[~merged_df["brewery_state"].str.contains("<a href")]
    return merged_df