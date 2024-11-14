import os
import warnings

import pandas as pd

common_replacements = {
    "Ã¡": "á", "Ã­": "í", "Ãº": "ú",
    "Ã±": "ñ", "Ã": "Ñ", "Ã¼": "ü", "Ã": "Ü",
    "Ã€": "À", "Ã©": "é", "Ã³": "ó", "Ã": "Í", "â": "'", "Ã": "ß", "": "'",
}


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


def clean_beer_advocate(
        raw_data_path,
        clean_data_path,
):
    """
    Clean the BeerAdvocate data stored at raw_data_path and save it in the clean_data_path
    """
    # users
    users_ba = pd.read_csv(raw_data_path + "/BeerAdvocate_users.csv")
    
    # Extract users only from the USA
    us_users_ba = filter_only_americans(users_ba.dropna(subset=["user_name", "location"]))
    
    # Replace missing values with 0 or "" if it is text
    extract_nans_as_columns_df(us_users_ba, numerical_columns(us_users_ba), replace_value=0)
    extract_nans_as_columns_df(us_users_ba, string_columns(us_users_ba), replace_value="")
    
    # save the cleaned data
    os.makedirs(clean_data_path, exist_ok=True)
    with open(clean_data_path + "/usa_users.csv", "w") as f:
        us_users_ba.to_csv(f, index=False)
    
    # ratings
    
    ratings_ba = pd.read_csv(raw_data_path + "/BeerAdvocate_ratings.csv")
    # Remove the reviews as we won't work with them
    ratings_ba.drop(columns=["text", "review"], inplace=True)
    ratings_ba = ratings_ba.dropna(subset=["user_id", "beer_id"])
    ratings_ba = clean_ratings(ratings_ba)
    us_ratings_ba = filter_by_users(ratings_ba, us_users_ba)
    
    # save
    with open(clean_data_path + "/usa_ratings.csv", "w") as f:
        us_ratings_ba.to_csv(f, index=False)
    
    del ratings_ba; del us_ratings_ba; del users_ba; del us_users_ba
    
    beer_ba = pd.read_csv(raw_data_path + "/BeerAdvocate_beers.csv")
    extract_nans_as_columns_df(beer_ba, numerical_columns(beer_ba), replace_value=0)
    extract_nans_as_columns_df(beer_ba, string_columns(beer_ba), replace_value="")
    beer_ba = replace_common_enc_errors(beer_ba)
    
    with open(clean_data_path + "/beers.csv", "w") as f:
        beer_ba.to_csv(f, index=False)
    
    del beer_ba
    
    # Clean breweries not much to do here as there are no missing values
    brewery_ba = pd.read_csv(raw_data_path + "/BeerAdvocate_breweries.csv")
    with open(clean_data_path + "/breweries.csv", "w") as f:
        brewery_ba.to_csv(f, index=False)
        
        
def clean_ratebeer(
        raw_data_path,
        clean_data_path,
):
    """
    Clean the Ratebeer data stored at raw_data_path and save it in the clean_data_path
    """
    # Create a clean folder for the Ratebeer data
    os.makedirs(clean_data_path, exist_ok=True)
    
    users_rb = pd.read_csv(raw_data_path + "/Ratebeer_users.csv")
    # clean users
    
    us_users_rb = filter_only_americans(users_rb.dropna(subset=["user_name", "location", "joined"]))
    
    with open(clean_data_path + "/usa_users.csv", "w") as f:
        us_users_rb.to_csv(f, index=False)
    
    #Clean ratings
    ratings_rb = pd.read_csv(raw_data_path + "/Ratebeer_ratings.csv")
    
    # Remove the reviews as we won't work with them
    ratings_rb.drop(columns=["text"], inplace=True)
    ratings_rb = ratings_rb.dropna(subset=["user_id", "beer_id"])
    ratings_rb = clean_ratings(ratings_rb)

    us_ratings_rb = filter_by_users(ratings_rb, us_users_rb)
    with open(clean_data_path + "/usa_ratings.csv", "w") as f:
        us_ratings_rb.to_csv(f, index=False)
    
    del ratings_rb; del us_ratings_rb; del users_rb; del us_users_rb
    
    # Clean beers
    beer_rb = pd.read_csv(raw_data_path + "/Ratebeer_beers.csv")
    
    extract_nans_as_columns_df(beer_rb, numerical_columns(beer_rb), replace_value=0)
    extract_nans_as_columns_df(beer_rb, string_columns(beer_rb), replace_value="")
    replace_common_enc_errors(beer_rb)
    
    with open(clean_data_path + "/beers.csv", "w") as f:
        beer_rb.to_csv(f, index=False)
    
    del beer_rb
    
    brewery_rb = pd.read_csv(raw_data_path + "/Ratebeer_breweries.csv")
    with open(clean_data_path + "/breweries.csv", "w") as f:
        brewery_rb.to_csv(f, index=False)
        
def clean_matched_data(
        raw_data_path,
        clean_data_path,
):
    """
    Clean the matched data and save it in the clean_data_path
    """
    users = pd.read_csv(raw_data_path + "/matched_beer_data_users.csv", low_memory=False)
    ratings = pd.read_csv(raw_data_path + "/matched_beer_data_ratings.csv", low_memory=False)
    beers = pd.read_csv(raw_data_path + "/matched_beer_data_beers.csv", low_memory=False)
    breweries = pd.read_csv(raw_data_path + "/matched_beer_data_breweries.csv", low_memory=False)
    users_approx = pd.read_csv(raw_data_path + "/matched_beer_data_users_approx.csv", low_memory=False)
    
    # Create a clean folder for the matched data
    os.makedirs(clean_data_path, exist_ok=True)
    
    # clean matched users
    users = matched_data_common_clean(users)
    us_states = users[users["ba_location"].str.contains(",")]["ba_location"].unique()
    us_users = users[users["ba_location"].isin(us_states)]
    
    with open(clean_data_path + "/usa_users.csv", "w") as f:
        us_users.to_csv(f, index=False)
    
    # clean matched users_approx
    users_approx = matched_data_common_clean(users_approx)
    us_users_approx = users_approx[users_approx["ba_location"].isin(us_states)]
    
    with open(clean_data_path + "/usa_users_approx.csv", "w") as f:
        us_users_approx.to_csv(f, index=False)
    
    # clean matched ratings
    ratings = matched_data_common_clean(ratings)
    # Remove the reviews as we won't work with them
    ratings.drop(columns=["ba_text", "ba_review", "ba_text_nan", "rb_text"], inplace=True)
    extract_nans_as_columns_df(ratings, numerical_columns(ratings), replace_value=0)
    extract_nans_as_columns_df(ratings, string_columns(ratings), replace_value="")
    
    with open(clean_data_path + "/ratings.csv", "w") as f:
        ratings.to_csv(f, index=False)
    
    # clean matched beers
    beers = matched_data_common_clean(beers)
    with open(clean_data_path + "/beers.csv", "w") as f:
        beers.to_csv(f, index=False)
    
    # clean matched breweries
    breweries = matched_data_common_clean(breweries)
    with open(clean_data_path + "/breweries.csv", "w") as f:
        breweries.to_csv(f, index=False)
