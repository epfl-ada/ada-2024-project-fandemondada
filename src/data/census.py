import pandas as pd

def load_urban_frac_df(path, filename):
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