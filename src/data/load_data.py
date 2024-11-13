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
