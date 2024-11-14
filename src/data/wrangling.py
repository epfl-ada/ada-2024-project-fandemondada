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


def clean_matched_data(df):
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
