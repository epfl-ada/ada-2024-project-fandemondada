import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import tarfile
import io
import tqdm
import csv
import gzip
import shutil
from datetime import datetime

def load_data(path, bool_load_txt = False):
    """
    Get data from compressed files
    inputs:
        - path: path to the folder containing the compressed files
        - load_txt: boolean, if True, load the txt files
    outputs:
        - data: dictionary containing the dataframes
    """
    data = {}
    for folder in os.listdir(path):
        if folder.endswith('.tar.gz'):
            list_tar_files = tarfile.open(path + folder, 'r:gz')
            
            for file in list_tar_files:
                
                if file.name.endswith(".csv"):
                    f = list_tar_files.extractfile(file)
                    data[folder[:-7] + "_" + file.name] = pd.read_csv(f)
                
                if file.name.endswith(".txt.gz") and bool_load_txt:
                    newpath = "temp/" 
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    list_tar_files.extract(file, path=newpath)
                    load_txt(newpath + "/" + file.name)
                    data[folder[:-7] + "_" + file.name[:-7] + ".csv"] = pd.read_csv(newpath + "/" + file.name[:-7] + ".csv")
            
            if bool_load_txt:
                shutil.rmtree(newpath)
    return data

def load_txt(file_path):
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

        file = csv.writer(open(file_path[:-7] + ".csv", 'w'))
        file.writerow(reviews[0].keys())
        for review in tqdm.tqdm(reviews):
            file.writerow(review.values())

def load_data_from_csv(path):
    """
    Load data from .csv files
    Inputs: path to the data files
    Outputs: dictionaries containing the dataframes BeerAdvocate, RateBeer and Matched
    """
    data_ba = {}
    data_rb = {}
    data_matched = {}
    for folder in os.listdir(path):
        if 'BeerAdvocate' in folder:
            for file in os.listdir(path + folder):
                if file.endswith(".csv"):
                    data_ba[file] = pd.read_csv(path + folder + "/" + file)
        if 'RateBeer' in folder:
            for file in os.listdir(path + folder):
                if file.endswith(".csv"):
                    data_rb[file] = pd.read_csv(path + folder + "/" + file)
        if 'Matched' in folder:
            for file in os.listdir(path + folder):
                if file.endswith(".csv"):
                    data_matched[file] = pd.read_csv(path + folder + "/" + file)
                    
    return data_ba, data_rb, data_matched

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