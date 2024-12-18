from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
from src.data.state_counts import get_counts_for_state_matrix, get_state_adjacency_matrix
import seaborn as sns

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