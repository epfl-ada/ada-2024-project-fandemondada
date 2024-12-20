import os
import warnings
import pandas as pd

common_replacements = {
    "Ã¡": "á", "Ã­": "í", "Ãº": "ú",
    "Ã±": "ñ", "Ã": "Ñ", "Ã¼": "ü", "Ã": "Ü",
    "Ã€": "À", "Ã©": "é", "Ã³": "ó", "Ã": "Í", "â": "'", "Ã": "ß", "": "'",
}

def clean_data(data_path, clean_load=False):
    """
    Clean data for BeerAdvocate, RateBeer, and Matched datasets and generates the corresponding usa restriced dataset and saves them as .
    
    Parameters:
    - raw_data_path: The root directory containing raw data folders.
    - clean_data_path: The root directory where cleaned data will be saved.
    - clean_load: If False, skips cleaning datasets if cleaned files already exist.
    """
    clean_dataset(data_path, 'BeerAdvocate', clean_load=clean_load,)
    
    clean_dataset(data_path, 'Ratebeer', clean_load=clean_load,)
    
    clean_dataset(data_path, 'Matched', clean_load=clean_load)

def clean_dataset(data_path, dataset_name, clean_load=False):
    """
    Clean the BeerAdvocate data stored at raw_data_path and save it in the clean_data_path.
    """

    full_data_path = os.path.join(data_path, dataset_name)

    # Ensure the clean data folder exists
    os.makedirs(full_data_path, exist_ok=True)

    # Clean users
    usa_users_path = os.path.join(full_data_path, "usa_users.csv")
    if clean_load or not os.path.exists(usa_users_path):
        users = pd.read_csv(os.path.join(full_data_path, dataset_name + "_users.csv"), low_memory=False)
        if dataset_name == 'Matched': 
            users = matched_data_common_clean(users)
        us_users = filter_only_americans(users.dropna(subset=["user_name", "location"]))
        extract_nans_as_columns_df(us_users, numerical_columns(us_users), replace_value=0)
        extract_nans_as_columns_df(us_users, string_columns(us_users), replace_value="")
        us_users.to_csv(usa_users_path, index=False)
        del users, us_users

    # Clean ratings
    usa_ratings_path = os.path.join(full_data_path, "usa_ratings.csv")
    if clean_load or not os.path.exists(usa_ratings_path):
        ratings = pd.read_csv(os.path.join(full_data_path, dataset_name + "_ratings.csv"), low_memory=False)
        if dataset_name == 'Matched': 
            ratings = matched_data_common_clean(ratings)
            ratings.drop(columns=["ba_text", "ba_review", "ba_text_nan", "rb_text"], inplace=True)
        ratings.drop(columns=["text", "review"], inplace=True)
        ratings = ratings.dropna(subset=["user_id", "beer_id"])
        ratings = clean_ratings(ratings)
        us_ratings = filter_by_users(ratings, pd.read_csv(usa_users_path))
        us_ratings.to_csv(usa_ratings_path, index=False)
        del ratings, us_ratings

    # Clean beers
    beers_path = os.path.join(full_data_path, "beers.csv")
    if clean_load or not os.path.exists(beers_path):
        beer = pd.read_csv(os.path.join(full_data_path, dataset_name + "_beers.csv"), low_memory=False)
        if dataset_name == 'Matched': 
            beer = matched_data_common_clean(beer)
        extract_nans_as_columns_df(beer, numerical_columns(beer), replace_value=0)
        extract_nans_as_columns_df(beer, string_columns(beer), replace_value="")
        beer = replace_common_enc_errors(beer)
        beer.to_csv(beers_path, index=False)
        del beer

    # Clean breweries
    breweries_path = os.path.join(full_data_path, "breweries.csv")
    if clean_load or not os.path.exists(breweries_path):
        brewery = pd.read_csv(os.path.join(full_data_path, dataset_name + "_breweries.csv"))
        if dataset_name == 'Matched': 
            brewery = matched_data_common_clean(brewery)
        remove_links(brewery)
        brewery.to_csv(breweries_path, index=False)
        del brewery


def replace_common_chars(string):
    for key, value in common_replacements.items():
        string = string.replace(key, value)
    return string


def replace_common_enc_errors(df):
    for column in string_columns(df):
        df[column] = df[column].apply(replace_common_chars)
    return df


def decode_string(column):
    """
    Decodes a column with weird characters like \x92\x09, they converted
    are utf-8 equivalent for readability, it is not perfect but most common
    characters are converted
    """
    return column[~column.isna()].apply(
        lambda x: replace_common_chars(x.encode().decode('unicode_escape').encode('latin1').decode('utf-8')))


def get_us_states(df):
    return df[df["location"].str.contains(",")]["location"].unique()


def filter_by_locations(df, locations):
    return df[df["location"].isin(locations)]


def filter_by_state(df, state):
    return df[df["location"].str.contains(state)]


def filter_only_americans(df):
    return filter_by_locations(df, get_us_states(df))


def filter_by_users(df, users):
    return df[df["user_id"].isin(users["user_id"])]

def remove_links(df):
    for index, column in df.iterrows():
        if "<" in df["location"][index]:
            df["location"][index] = df["location"][index].split("<")[0]


def extract_nan_as_column(df, column_name, replace_value=0):
    """
    If a column has nans it extracts them from the column and creates a new column with the same name and '_nan' appended. Nan values are replaced by the replace_value and the new column has 1 where the original column had nan.

    For logistic regression, this is useful to let the model decide how best to replace nan values
    """
    if df[column_name].isna().sum() == 0:
        return
    nan_column_name = f"{column_name}_nan"
    is_nan = df[column_name].isna()
    df.loc[is_nan, column_name] = replace_value
    # df[column_name][is_nan] = replace_value
    df[nan_column_name] = is_nan.astype(int)


def numerical_columns(df):
    return df.dtypes[df.dtypes != "object"].index[1:]


def string_columns(df):
    return df.dtypes[df.dtypes == "object"].index


def extract_nans_as_columns_df(df, column_names, replace_value=0):
    for column in column_names:
        extract_nan_as_column(df, column, replace_value=replace_value)


def clean_df(df, clean_nan_func, clean_chars_func):
    """
    Cleans a dataframe by cleaning all string columns and extracting nans as columns for columns with nans
    """
    for column in string_columns(df):
        df[column] = clean_chars_func(df[column], clean_nan_func, clean_chars_func)
    extract_nans_as_columns_df(df, string_columns(df), replace_value="")
    extract_nans_as_columns_df(df, numerical_columns(df), replace_value=0)

def extract_nans(df):
    for column in string_columns(df):
        extract_nan_as_column(df, column, replace_value="")
    for column in numerical_columns(df):
        extract_nan_as_column(df, column, replace_value=0)
    return df


def clean_ratings(df):
    """
    Cleans a dataframe by cleaning all string columns and extracting nans as columns for columns with nans
    """
    for column in string_columns(df):
        df[column] = decode_string(df[column])
    extract_nans_as_columns_df(df, string_columns(df), replace_value="")
    extract_nans_as_columns_df(df, numerical_columns(df), replace_value=0)
    return df

def matched_data_common_clean(df):
    """
    Basic cleaning that is common to all matched data:
    - Replace column names with right ones (e.g. 'ba_1' -> 'ba_user_id')
    - Delete the first row as it contains the column names in the original dataset
    - Convert columns to numeric if possible
    - Extract nans as columns for numerical columns
    """
    # Since the first row is the name of the columns, we drop it and change the column names to lowercase
    df.columns = df.columns.str.lower()
    first_rows = df.iloc[0]
    # Rename columns so we can remove the first row
    df.columns = [column if i == 0 else f"{column.split('.')[0]}_{first_rows[column]}" for i, column in
                  enumerate(df.columns)]
    df = df.iloc[1:]
    # ignore warnings when converting to numeric
    warnings.filterwarnings("ignore")
    df = df.apply(pd.to_numeric, errors='ignore')
    warnings.resetwarnings()
    extract_nans_as_columns_df(df, numerical_columns(df), replace_value=0)
    extract_nans_as_columns_df(df, string_columns(df), replace_value="")
    return df