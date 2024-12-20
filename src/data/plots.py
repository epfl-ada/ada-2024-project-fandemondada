from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
from src.data.state_counts import get_counts_for_state_matrix, get_state_adjacency_matrix
import seaborn as sns
import plotly.graph_objects as go
import math

def plot_provenance(
        ratings_breweries_merged, 
        states, 
        top_k=10, 
        sort_option="local_count",
        ascending=False, 
        width=0.8, 
        as_ratio=True, 
        figsize=(12, 8), 
        colors=None
    ):
    """
    Plots the top-k states review provenances (local, national or foreign) according to the sort option as a stacked graph. 
    If as_ratio is true normalizes the counts.
    """
    state_adj_matrix = get_state_adjacency_matrix(ratings_breweries_merged, states, as_ratio=as_ratio, drop_world=False)
    us_counts_df = get_counts_for_state_matrix(state_adj_matrix)
    us_counts_df = us_counts_df.sort_values(by=sort_option, ascending=ascending).head(top_k)
    
    # Put the metric we are sorting by underneath so it look prettier
    categories = list(us_counts_df.columns)
    categories.remove(sort_option)
    categories.insert(0, sort_option)

    fig, ax = plt.subplots(figsize=figsize)
    
    bottom = np.zeros(len(us_counts_df))
    for idx, category in enumerate(categories):
        p = ax.bar(
            us_counts_df.index,
            us_counts_df[category],
            width=width,
            bottom=bottom,
            label=category.replace('_', ' ').replace('count', 'reviews').title(),
            color=colors[category],
        )
        barlabels = ax.bar_label(p, label_type='center', color='white', fmt='{:.2f}' if as_ratio else "{:.0f}")
        bottom += us_counts_df[category].values
    ax.legend(ncols=len(categories),
            loc='lower right' if as_ratio and not ascending else 'upper right', fontsize='medium')
    return fig, ax


def plot_state_matrix_as_heatmap(adj_matrix, title, xlabel, ylabel, ax=None):
    """
    Plots the state adjencency matrix as a heatmap.
    """
    if ax:
        sns.heatmap(adj_matrix, cmap='inferno', ax=ax, cbar=False)
        ax.set_title(f"{title}")
    else:
        plt.figure(figsize=(12, 10))
        sns.heatmap(adj_matrix, cmap='inferno') 
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.show()

def create_yearly_heatmap_gif(ratings_breweries_merged, states, save_file):
    """
    Creates a gif with the yearly evolution of the state reviews
    """
    def get_yearly_reviews(ratings_breweries_merged):
        reviews_by_year = ratings_breweries_merged.groupby(pd.to_datetime(ratings_breweries_merged["date"]).dt.year)
        return reviews_by_year
    
    yearly_reviews = {group: group_df for group, group_df in get_yearly_reviews(ratings_breweries_merged)}
    frame2year = {i: group for i, group in enumerate(yearly_reviews.keys())}
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.tight_layout()

    def update(frame):
        year = frame2year[frame]
        data = yearly_reviews[year]
        ax.clear()
        matrix = get_state_adjacency_matrix(data, states, as_ratio=True) 
        plot_state_matrix_as_heatmap(matrix, title=f'State Adjacency Matrix {year}', xlabel='Brewery State', ylabel='User State', ax=ax)
        fig.tight_layout()
        plt.close(fig)

    anim = FuncAnimation(fig, update, frames=len(frame2year), repeat=True)  
    anim.save(save_file, writer="pillow", fps=2) 

def plot_monthly_country_counts(
        monthly_country_counts, 
        title,
        xlabel,
        ylabel,
        date_steps=5, 
        colors=None
    ):
    """
    Plot the monthly summed local, national and foreign country counts for america
    """
    legends = [column.replace("_", " ").title() for column in list(monthly_country_counts.columns)]
    ax = monthly_country_counts.plot(kind='bar', stacked=True, figsize=(15,8), width=1.0, color=colors)
    ax.legend(legends,
                loc='lower right' , fontsize='medium')


    ticks = ax.get_xticks()
    labels = [tick.get_text() for tick in ax.get_xticklabels()]

    step = date_steps
    ax.set_xticks(ticks[::step])
    ax.set_xticklabels(labels[::step], rotation=45)

    plt.xticks(rotation=45)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.show()

def get_countries_code():
    """ Generates a dictionnary with all countries code
    Output:
        - code: a dictionnary with all countries code
    """

    # get all locations code
    code = {'Alabama': 'AL',
            'Alaska': 'AK',
            'Arizona': 'AZ',
            'Arkansas': 'AR',
            'California': 'CA',
            'Colorado': 'CO',
            'Connecticut': 'CT',
            'Delaware': 'DE',
            'District of Columbia': 'DC',
            'Florida': 'FL',
            'Georgia': 'GA',
            'Hawaii': 'HI',
            'Idaho': 'ID',
            'Illinois': 'IL',
            'Indiana': 'IN',
            'Iowa': 'IA',
            'Kansas': 'KS',
            'Kentucky': 'KY',
            'Louisiana': 'LA',
            'Maine': 'ME',
            'Maryland': 'MD',
            'Massachusetts': 'MA',
            'Michigan': 'MI',
            'Minnesota': 'MN',
            'Mississippi': 'MS',
            'Missouri': 'MO',
            'Montana': 'MT',
            'Nebraska': 'NE',
            'Nevada': 'NV',
            'New Hampshire': 'NH',
            'New Jersey': 'NJ',
            'New Mexico': 'NM',
            'New York': 'NY',
            'North Carolina': 'NC',
            'North Dakota': 'ND',
            'Ohio': 'OH',
            'Oklahoma': 'OK',
            'Oregon': 'OR',
            'Pennsylvania': 'PA',
            'Rhode Island': 'RI',
            'South Carolina': 'SC',
            'South Dakota': 'SD',
            'Tennessee': 'TN',
            'Texas': 'TX',
            'Utah': 'UT',
            'Vermont': 'VT',
            'Virginia': 'VA',
            'Washington': 'WA',
            'West Virginia': 'WV',
            'Wisconsin': 'WI',
            'Wyoming': 'WY'}

    # source of the file "all.csv" with all the country codes: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv
    countries = pd.read_csv("data/clean/all.csv")
    dict_distances = countries.set_index('name')['alpha-3'].to_dict()
    code.update(dict_distances)
    return code

def generate_choropleth_map(dataframe, code, column_to_plot, plot_title, legend):
    """ Generates an interactive choropleth map of the world and the US States
    Input:
        - dataframe: a pandas dataframe with the data that we want to plot
        - code: a dictionnary with all countries code
        - column to plot: the name of the column with the data we want to plot
        - plot_title: the title of the plot
        - legend: the legend of the plot
    """
    dataframe["Code"] = dataframe['location'].map(code)
    countries = dataframe["Code"]
    values = dataframe[column_to_plot]

    choropleth = go.Choropleth(
        locations=countries,         
        z=values,                   
        locationmode='ISO-3', 
        colorscale='plasma',        
        colorbar_title=legend,  
        hoverinfo="location+z",
    )

    choropleth2 = go.Choropleth(
        locations=countries,         
        z=values,                    
        locationmode='USA-states', 
        colorscale='plasma',         
        colorbar_title=legend,  
        hoverinfo="location+z",
    )

    layout = go.Layout(
        title=plot_title,
        geo=dict(
            showland=True,            
            landcolor="white",        
            projection_type="natural earth",  
            showcountries=True,   
            countrycolor="Black",  
        ),
    )

    fig = go.Figure(data=[choropleth, choropleth2], layout=layout)
    fig.show()


def plot_breweries_evolution(cum_brew):
    fig, ax = plt.subplots(1, 1)
    cum_brew.plot(y= ['cumulative_US', 'cumulative_World'], ax=ax, label=['US', 'World'])
    ax.set_xlabel('Time')

    ax.legend()

    ax2 = ax.twinx()  # instantiate a second Axes that shares the same x-axis
    cum_brew.plot(y= ['frac'], ax=ax2, color='g')
    ax2.set_ylabel('Fraction of US breweries', color='g')  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor='g')

    ax.set_ylabel("Number of breweries")

    plt.show()

def plot_breweries_per_state(brew_dic):
    num_states = len(brew_dic)
    cols = 5
    rows = math.ceil(num_states / cols)

    fig, axs = plt.subplots(rows, cols, figsize=(20, 4 * rows))
    axs = axs.flatten()

    for i, (state, df) in enumerate(brew_dic.items()):
        #monthly_avg = df.groupby('year_month')['distance'].mean()
        df.plot(drawstyle="steps", y= ['cumulative'], ax=axs[i], linestyle='-')
        axs[i].set_title(f"{state}")
        axs[i].set_xlabel("Year")
        axs[i].set_ylabel("Number of breweries")
        axs[i].tick_params(axis='x', rotation=45)

        ax2 = axs[i].twinx()  # instantiate a second Axes that shares the same x-axis
        df.plot(y= ['count'], ax=ax2, color='g')
        ax2.set_ylabel('New in that period', color='g')  # we already handled the x-label with ax1
        ax2.tick_params(axis='y', labelcolor='g')


    plt.tight_layout()
    plt.show()

def plot_distance_per_state(user_state_dic, new_brew_state_dic):
    num_states = len(user_state_dic)
    cols = 5
    rows = math.ceil(num_states / cols)

    fig, axs = plt.subplots(rows, cols, figsize=(20, 4 * rows))
    axs = axs.flatten()

    for i, (state, df) in enumerate(user_state_dic.items()):
        monthly_avg = df.groupby('year_month')['distance'].mean()
        monthly_avg.plot(ax=axs[i], linestyle='-')
        axs[i].set_title(f"{state}")
        axs[i].set_xlabel("Year")
        axs[i].set_ylabel("Average Distance (km)")
        axs[i].tick_params(axis='x', rotation=45)

        ax2 = axs[i].twinx()
        # new brweries in that state
        new_brew_state_dic[state].plot(drawstyle="steps", y=['cumulative'], ax=ax2, linestyle='-', color='g')
        ax2.set_ylabel('Number of breweries', color='g')  # we already handled the x-label with ax1
        ax2.tick_params(axis='y', labelcolor='g')

    plt.tight_layout()
    plt.show()

def plot_average_distance_year(usa_ratings_merged):
    usa_ratings_merged['year'] = usa_ratings_merged['year_month'].dt.year
    average_distance_per_year = usa_ratings_merged.groupby('year')['distance'].mean()
    average_distance_per_year = average_distance_per_year[average_distance_per_year.index >= 2000] #only take data after 2000 (too few points before)

    plt.plot(average_distance_per_year.index, average_distance_per_year)
    plt.title('Average Distance traveled by rated beers')
    plt.xlabel('Year')
    plt.ylabel('Average Distance (km)')
    plt.xticks(ticks=range(2000, average_distance_per_year.index.max() + 1), rotation=45)
    plt.show()

def plot_distance_and_data(usa_ratings_merged, add_data, column_name, label):
    usa_ratings_merged['year'] = usa_ratings_merged['year_month'].dt.year
    average_distance_per_year = usa_ratings_merged.groupby('year')['distance'].mean()
    average_distance_per_year = average_distance_per_year[average_distance_per_year.index >= 2000] #only take data after 2000 (too few points before)

    plt.plot(average_distance_per_year.index, average_distance_per_year)
    plt.title('Average Distance traveled by rated beers')
    plt.xlabel('Year')
    plt.ylabel('Average Distance (km)')
    plt.xticks(ticks=range(2000, average_distance_per_year.index.max() + 1), rotation=45)

    new_ax = plt.gca().twinx()
    new_ax.plot(add_data['year'], add_data[column_name], color='r')
    new_ax.set_ylabel(label, color='r')
    new_ax.tick_params(axis='y', labelcolor='r')

    plt.show()