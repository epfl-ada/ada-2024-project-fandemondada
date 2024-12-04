import os
from src.data.load_data import load_data

def tar_gz_to_csv(load_path, save_path, load_text=False):
    """extracts tar.gz archives in given folder and saves it to the save_path with 
    subfolders for RateBeer, BeerAdvocate and MatchedBeerData

    Args:
        load_path (string): path where the .tar.gz files are located
        save_path (string): where to save extracted data
        load_text (bool, optional): If the text reviews should also be extracted. Takes much longer. Defaults to False.

    Returns:
        dict[pd.df]: dictionnary with all the df extracted
    """
    data_sets = load_data(load_path, bool_load_txt=load_text)
    ratebeer_path = 'RateBeer'
    beeradvocate_path = 'BeerAdvocate'
    matched_path = 'MatchedBeerData'

    for data in data_sets.keys():
        path = save_path
        if "BeerAdvocate" in data:
           path = os.path.join(save_path, beeradvocate_path)
        elif "Rate" in data:
            path = os.path.join(save_path, ratebeer_path)
        elif "matched" in data:
            path = os.path.join(save_path, matched_path)
        else:   # in case some other tar.gz file was in the folder
            path = os.path.join(save_path, "Other")
        if not os.path.exists(path):
            os.makedirs(path)
        
        csv_path = os.path.join(path, data)
        if not os.path.exists(csv_path): #check if files already exist
            data_sets[data].to_csv(csv_path)

    return data_sets