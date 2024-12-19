import pandas as pd

def breweries_first_date(reviews_df, brew_df):
    rev = reviews_df.loc[:, ('brewery_id', 'date')].sort_values('date').drop_duplicates(subset=['brewery_id'])

    brew_df['first_rev']=brew_df['brewery_id'].map(dict(zip(rev.brewery_id,rev.date)))
    brew_df = brew_df.dropna(subset=['first_rev'])
    brew_df['year_month'] = pd.to_datetime(brew_df['first_rev']).dt.to_period('M')
    first_review = brew_df['year_month'].min()
    last_review = brew_df['year_month'].max()

    return brew_df, (first_review, last_review)

def monthly_new_breweries(brew_df, time_range):
    new_brew = brew_df.value_counts(subset=['year_month'], sort=False).to_frame().reset_index()
    #new_brew['year_month'] = new_brew['year_month'].dt.to_timestamp()
    # need to fill gaps to plot later:
    #new_brew = new_brew.set_index('year_month').resample('ME')
    new_brew = new_brew.rename(columns={0: 'count'})
    
    # Create a DataFrame with all months in the time range
    all_months = pd.DataFrame({'year_month': pd.period_range(start=time_range[0], end=time_range[1], freq='M')})
    
    # Merge with new_brew to ensure all months are included
    new_brew = all_months.merge(new_brew, on='year_month', how='left').fillna(0)
    

    new_brew['cumulative'] = new_brew['count'].cumsum()
    # set year month as index
    new_brew = new_brew.set_index('year_month')
    
    return new_brew