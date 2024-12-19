import numpy as np
import pandas as pd


def transform_to_distribution(row):
    if row.sum() <= 0:
        return row
    return row/row.sum()

def get_state_adjacency_matrix(ratings_breweries_merged, states, as_ratio=True, drop_world=True):
    """
    Generates a state adjacency matrix from a merged dataframe of ratings and breweries.

    Args:
        - ratings_breweries_merged (pd.DataFrame): DataFrame containing merged ratings and breweries data.
        - states (list): List of state names to include in the matrix.
        - as_ratio (bool, optional): If True, converts counts to ratios. Defaults to True.
        - drop_world (bool, optional): If True, excludes non-listed states from the matrix. Defaults to True.

    Returns:
        pd.DataFrame: A DataFrame representing the state adjacency matrix where each element is the number of users 
                  from user_state that reviewed a beer in brewery_state. If as_ratio is True, the elements are 
                  ratios instead of counts.
    """
    state_matrix = ratings_breweries_merged.groupby(by=["user_state", "brewery_state"]).size().unstack(fill_value=0)
    foreign_counts = state_matrix.drop(columns=states, errors='ignore').T.sum().fillna(0)
    state_matrix = state_matrix.reindex(index=sorted(list(states)), columns=sorted(list(states)), fill_value=0)
    state_matrix = state_matrix.loc[:, sorted(list(states))]
    if not drop_world:
        state_matrix["World"] = foreign_counts
    if as_ratio:
        state_matrix = state_matrix.apply(transform_to_distribution, axis=1)
    
    return state_matrix

def get_counts_for_state_matrix(matrix, as_ratio=False):
    """
    Calculate local, national, and foreign counts for a given state matrix.

    Args:
    matrix (pd.DataFrame): A pandas DataFrame representing the state matrix. 
                           It must contain a column named 'World'.
    as_ratio (bool): If True, the counts are converted to ratios. Default is False.

    Returns:
    pd.DataFrame: A DataFrame with columns 'local_count', 'national_count', and 
                  'foreign_count'. If `as_ratio` is True, the counts are normalized 
                  to ratios.
    """
    if "World" not in matrix.columns:
        raise KeyError("World column not found cannot get foreign_count")
    local_count = np.diagonal(matrix.drop(columns=["World"]))
    foreign_count = matrix['World']
    non_world_sum = np.array(matrix.drop(columns=['World']).T.sum())
    national_count = non_world_sum - local_count
    ret = pd.DataFrame({
        'local_count': local_count.tolist(),
        'national_count': national_count.tolist(),
        'foreign_count': foreign_count
    })
    if as_ratio:
        ret = ret.div(ret.sum(axis=1)).fillna(0)
    return ret

def sort_matrix_by_diagonal(state_adj_matrix, ascending=False):
    """
    Sorts the adjency matrix according to the the local counts (the diagonal). 
    """
    diagonal_values = np.diagonal(state_adj_matrix)
    state2diagonal = [(state, diagonal_values[i]) for i, state in enumerate(state_adj_matrix.columns)]
    sorted_diagonal = sorted(state2diagonal, reverse=not ascending, key=lambda x: x[1])
    sorted_states = [x[0] for x in sorted_diagonal]
    sorted_ajd_matrix = state_adj_matrix.loc[sorted_states, sorted_states]
    return sorted_ajd_matrix


# ----- Code for monthly provenance data -----

def get_reviews_by_month(ratings_breweries_merged, start_month=None, end_month=None):
    """
    Filters and groups brewery reviews by month within a specified date range.

    Args:
    - ratings_breweries_merged (DataFrame): A DataFrame containing brewery reviews with a 'date' column.
    - start_month (datetime.date, optional): The start date to filter reviews. Defaults to None.
    - end_month (datetime.date, optional): The end date to filter reviews. Defaults to None.

    Returns:
    DataFrameGroupBy: A DataFrameGroupBy object with reviews grouped by month.
    """
    if start_month:
        ratings_breweries_merged = ratings_breweries_merged[pd.to_datetime(ratings_breweries_merged["date"]).dt.date >= start_month]
    if end_month:
        ratings_breweries_merged = ratings_breweries_merged[pd.to_datetime(ratings_breweries_merged["date"]).dt.date <= end_month]
    reviews_by_month = ratings_breweries_merged.groupby(pd.to_datetime(ratings_breweries_merged["date"]).dt.to_period('M'))
    return reviews_by_month

def get_state_matrix_per_month(reviews_by_month, states, cumulative=False):
    """
    Get a table indexed by year-month and user_state with the column for different brewery location, the values are the number of reviews from user_state to brewery_state.
    If cumulative, it's the total number of reviews from user_state to brewery_state at that point in time.
    """
    # For each month get the matrix of review count from user state to brewery locations
    counts_by_month = reviews_by_month.apply(lambda x: get_state_adjacency_matrix(x, states, as_ratio=False, drop_world=False).fillna(0))
    if cumulative:
        counts_by_month = counts_by_month.groupby(level="user_state").cumsum()
    return counts_by_month



def get_total_counts_from_monthly_data(counts_by_month, as_ratio=True):
    """
    Takes in a dataframe with the count of reviews from user state to brewery state by month and 
    outputs a df with the local_count, national_count and foreign_count by month
    """
    
    def total_counts_by_date(sub_df):
        local_count = np.diagonal(sub_df.drop(columns=["user_state", "date", "World"])).sum()
        foreign_count = sub_df['World'].sum() if 'World' in sub_df.columns else 0
        non_world_sum = np.array(sub_df.drop(columns=["user_state", 'World', 'date'])).sum()
        national_count = non_world_sum - local_count

        return pd.Series({
            'local_count': local_count,
            'national_count': national_count,
            'foreign_count': foreign_count
        })

    counts_by_month_compact = counts_by_month.reset_index().groupby("date").apply(total_counts_by_date)
    if as_ratio:
        row_sums = counts_by_month_compact.sum(axis=1)
        ratios_by_month_collapsed = counts_by_month_compact.div(row_sums, axis=0).fillna(0)
        return ratios_by_month_collapsed
    return counts_by_month_compact


def get_monthly_counts_usa(ratings_brewery_merged, states, start_month=None, end_month=None, cumulative=False, as_ratio=True):
    """
    Calculate the total counts (local, national and foreign) of reviews for US states within a specified date range.

    Args:
        - ratings_brewery_merged (pd.DataFrame): The merged DataFrame containing ratings and brewery information.
        - states (list): A list of US states (["Alabama", etc, ...])
        - start_month (str, optional): The start month for the date range filter in 'YYYY-MM' format. Defaults to None.
        - end_month (str, optional): The end month for the date range filter in 'YYYY-MM' format. Defaults to None.
        - cumulative (bool, optional): If True, returns cumulative counts over time. Defaults to False.
        - as_ratio (bool, optional): If True, returns the counts as ratios. Defaults to True.

    
    Returns:
        pd.DataFrame: A DataFrame containing the total counts of reviews for each state
    """
    rev_monthly = get_reviews_by_month(ratings_brewery_merged, start_month=start_month, end_month=end_month)
    counts_by_month = get_state_matrix_per_month(rev_monthly, states, cumulative=cumulative)
    us_counts = get_total_counts_from_monthly_data(counts_by_month, as_ratio=as_ratio)
    return us_counts