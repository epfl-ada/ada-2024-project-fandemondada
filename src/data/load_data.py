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
    Load data from compressed .tar.gz files
    Inputs:
        - path: path to the folder containing the compressed files
        - load_txt: boolean, if True, load the txt files
    Outputs:
        - data: dictionary containing the dataframes
    """
    temp_path =  "temp/" 
    data = {}

    # loop over all folder in path, open the .tar.gz
    for folder in os.listdir(path):
        if folder.endswith('.tar.gz'):
            list_tar_files = tarfile.open(path + folder, 'r:gz')
            
            # loop over all files in folder, load only the .csv and .txt.zip (if bool = True)
            for file in list_tar_files:
                
                # extract and load the .csv
                if file.name.endswith(".csv"):
                    f = list_tar_files.extractfile(file)
                    data[folder[:-7] + "_" + file.name] = pd.read_csv(f) # :-7 to remove extension from the name
                
                # extract and load the .txt.zip
                if file.name.endswith(".txt.gz") and bool_load_txt:
                    
                    # create a temporary folder to store the .csv created from .txt.zip
                    newpath = temp_path + folder[:-7] + "/" # :-7 to remove extension from the name
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)

                    list_tar_files.extract(file, path=newpath)
                    load_txt(newpath + "/" + file.name)
                    data[folder[:-7] + "_" + file.name[:-7] + ".csv"] = pd.read_csv(newpath + "/" + file.name[:-7] + ".csv") # :-7 to remove extension from the name

    # delete the temporary folder and everything in it
    if bool_load_txt:
        shutil.rmtree(temp_path)

    return data

def load_txt(file_path):
    """
    Create a pandas loadable .csv from .txt.zip files
    Inputs:
        - path: path to the folder containing the compressed files
    Outputs:
        - none
    """
    # open the .zip and convert the lines to string
    with gzip.open(file_path,'rb') as f:
        reviews = []
        review = {}
        
        for line in tqdm.tqdm(f):
            line = str(line)
           
           # load lines with content, remove lines with less than 5 characters
            if len(line.strip()) <= 5: 
                reviews.append(review)
                review = {}
            else:
                field_name, field_value = line.split(':', 1)
                review[field_name.strip()[2:]] = field_value.strip()[:-3] # 2: and :-3 to remove extension from the name

        # create a .csv and write the content
        file = csv.writer(open(file_path[:-7] + ".csv", 'w', encoding="utf-8")) # :-7 to remove extension from the name
        file.writerow(reviews[0].keys())
        for review in tqdm.tqdm(reviews):
            file.writerow(review.values())

