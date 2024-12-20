from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import ast


geolocator = Nominatim(user_agent="FanDeMondADA")


def compute_distance(first_place, second_place):
    """ Compute the distance between two locations using latitude and longitude
    Output:
        - distance: distance between two locations in km
    """
    distance = geodesic((first_place.latitude, first_place.longitude), (second_place.latitude, second_place.longitude)).km
    
    return distance 


def get_raw_locations():
    """ Get all dataframes containing useful locations
    Output:
        - list_df_with_locations: list of dataframes containing all possible useful locations 
    """
    ba_usa_users = pd.read_csv("data/clean/BeerAdvocate/usa_users.csv")
    rb_usa_users = pd.read_csv("data/clean/Ratebeer/usa_users.csv")
    ba_breweries = pd.read_csv("data/clean/BeerAdvocate/breweries.csv")
    rb_breweries = pd.read_csv("data/clean/Ratebeer/breweries.csv")

    list_df_with_locations = [ba_usa_users, rb_usa_users, ba_breweries, rb_breweries]
    return list_df_with_locations


def get_locations_coordinates(list_df_with_locations):
    """ Get the location's coordinates for all relevant locations
    Input:
        - list_df_with_locations: list of dataframes containing all possible useful locations
    Output:
        - dict_coordinates: a dictionnary with key a locations and value its address and coordinates
    """
    dict_coordinates = {}

    # get the coordinates of all locations
    for df in list_df_with_locations:
        for index, column in df.iterrows():

            if dict_coordinates.get(column["location"]) == None:
                try: 
                    dict_coordinates[column["location"]] = geolocator.geocode(column["location"])
                except:
                    print(column["location"])

    # to correct state of Washington interpreted as Washington DC
    dict_coordinates["United States, Washington"] = geolocator.geocode("Seattle")

    # Canada and UK sometimes statewise in raw files but sometimes handled as countries
    dict_coordinates["Canada"] = geolocator.geocode("Canada")
    dict_coordinates["United Kingdom"] = geolocator.geocode("United Kingdom")

    # USA sometimes as a country
    dict_coordinates["United States"] = geolocator.geocode("United States")

    # correct the template of the locations to match the ones of the other parts
    for key in list(dict_coordinates):

        if key.startswith("United States, "):
            dict_coordinates[key[15:]] = dict_coordinates[key]

        if key.startswith("Canada, "):
            dict_coordinates[key[8:]] = dict_coordinates[key]

        if key.startswith("United Kingdom, "):
            dict_coordinates[key[16:]] = dict_coordinates[key]
    
    return dict_coordinates


def get_distances(dict_coordinates, statewise_dict):
    """ Compute all distances between locations' pairs in the input dict
    Input:
        - dict_coordinates: a dictionnary with key a locations and value its address and coordinates
        - statewise_dict: a dictionnary of dataframes
    Output:
        - dict_distances: a dict with key a pair of locations and value the distance between them
    """
    dict_distances = {}

    for key in statewise_dict.keys():
        for index, column in statewise_dict[key].iterrows():

            if dict_distances.get((column["user_state"], column["brewery_state"])) == None:
                try:
                    distance = compute_distance(dict_coordinates[column["user_state"]], dict_coordinates[column["brewery_state"]])
                    dict_distances[column["user_state"], column["brewery_state"]] = distance
                    dict_distances[column["brewery_state"], column["user_state"]] = distance
                except:
                    print(column["user_state"])
                    print(column["brewery_state"])
                    print(index)
    
    return dict_distances


def compute_distances(statewise_dict):
    """ Generate a .csv with all distances between locations' pairs in the input dict
    Input:
        - statewise_dict: a dictionnary of dataframes
    """
    list_df_with_locations = get_raw_locations()
    dict_coordinates = get_locations_coordinates(list_df_with_locations)
    dict_distances = get_distances(dict_coordinates, statewise_dict)

    df_distance = pd.DataFrame()
    df_distance = df_distance.from_dict(dict_distances, orient="index")
    df_distance = df_distance.rename(columns={0: "distance"})
    df_distance = df_distance.reset_index()

    with open("data/clean/distances.csv", "w") as f:
        df_distance.to_csv(f, index=False)


def load_distances(clean_folder_path):
    """ Load the distances from a .csv file into a dict
    Input:
        - clean_folder_path: the path of the foler where all clean files are
    Output:
        - dict_distances: a dict with key a pair of locations and value the distance between them
    """
    df_distance = pd.read_csv(clean_folder_path + "/distances.csv")
    df_distance = df_distance.set_index("index")
    dict_distances = df_distance.to_dict("index")

    return dict_distances

def convert_dict_to_table(dict):
    """ Convert the distance dictionnary to a table
    Input:
        - dict: a dict with key a pair of locations and value the distance between them
    Output:
        - distance_table: a table containing distance between locations
    """

    # use ast to interpret the weird string as a tuple
    new_data = [(*ast.literal_eval(k), v['distance']) for k, v in dict.items()]
    df = pd.DataFrame(new_data, columns=["place1", "place2", "distance"])
    distance_table = df.pivot(index='place1', columns='place2', values='distance')
    distance_table = distance_table.combine_first(distance_table.T)
    # fill not needed distances with 0
    distance_table = distance_table.fillna(0)
    return distance_table


