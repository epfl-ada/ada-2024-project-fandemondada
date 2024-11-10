import os
from src.data.load_data import load_data

def tar_gz_to_csv(load_path, save_path, load_text=False):
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
        if not os.path.exists(path):
            os.makedirs(path)
        data_sets[data].to_csv(os.path.join(path, data))

    return data_sets