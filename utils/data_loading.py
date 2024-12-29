#Importations des packages nécessaires aux fonctions créées

import glob
import gzip
import requests
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from scipy.spatial import distance
from tqdm import tqdm


# Fonction pour télécharger et lire un fichier CSV depuis un URL
def read_csv_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Dézippage du contenu pour passage au format CSV
        df = pd.read_csv(url, compression='gzip', sep=';', encoding='utf-8')
        return df
    else: #Gestion d'une éventuelle erreur d'accès à l'URL
        print(f"Echec du téléchargelent des données de {url}. Code d'erreur: {response.status_code}")
        return None


# Fonction pour télécharger les données météo par département, depuis le 1er janvier 2023 jusqu'à aujourd'hui
def load_department_data(
    department_id,
    relevant_columns=["DEPARTMENT_ID", "NUM_POSTE", "NOM_USUEL", "LAT", "LON", "AAAAMMJJHH","RR1", "T"],
    base_url_prefix="https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/HOR/H_",
    base_url_suffix="_latest-2023-2024.csv.gz",
):
    url = f"{base_url_prefix}{department_id}{base_url_suffix}"
    df = read_csv_from_url(url)
    
    if df is not None:
        # Ajout d'une colonne avec le numéro de département
        df["DEPARTMENT_ID"] = department_id

    return df[relevant_columns]


# Fonction pour sauvegarder les données dans un dossier commun
def load_and_save_all_department_data(
    department_ids,
    save_dir,
    relevant_columns=["DEPARTMENT_ID", "NUM_POSTE", "NOM_USUEL", "LAT", "LON", 
                      "AAAAMMJJHH", "RR1", "T"],
    base_url_prefix="https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/HOR/H_",
    base_url_suffix="_latest-2023-2024.csv.gz",
):
    for _id in tqdm(department_ids, desc="Loading data from internet and saving to disk"):
        df = load_department_data(_id, relevant_columns, base_url_prefix, base_url_suffix)
        df.to_csv(f"{save_dir}/{_id}.csv", index=False)


# Fonction pour concaténer les bases de données
def load_data_from_disk(data_dir):
    all_dfs = []
    for file_path in tqdm(glob.glob(f"{data_dir}/*.csv"), desc="Loading and concatenating data from disk"):
        all_dfs.append(pd.read_csv(file_path))
    return pd.concat(all_dfs)


# Fonction pour nettoyer et organiser le dataframe
def cleaning_and_organizing(df, columns, date):
    
    # On trie les lignes par les colonnes choisies
    df = df.sort_values(by=columns)
    # On formate les dates pour les utiliser ultérieurement dans les graphes
    df[date] = pd.to_datetime(df[date], format="%Y%m%d%H")

    return df


# Fonction pour trouver les coordonnées des clubs d'aviron à partir de leurs adresses
def get_coordinates(addresse):
    # Initialisation du geocoder
    geolocator = Nominatim(user_agent="geoapi", timeout=15)
    try:
        location = geolocator.geocode(addresse)
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Erreur pour l'adresse {addresse}: {e}")
        return pd.Series([None, None])


# Fonction pour importer la base des données fluviales
def import_geojson_from_url(geojson_url, geojson_file):
    response = requests.get(geojson_url)
    if response.status_code == 200:
        with open(geojson_file, "wb") as file:
            file.write(response.content)
    else:
        raise Exception("Impossible de télécharger le fichier GeoJSON")

    # on charge le fichier geojson avec geopandas et on retire les géométries invalides
    riv = gpd.read_file(geojson_file)
    riv = riv[riv.geometry.notnull()]

    return riv


# Fonction pour trouver la station la plus proche d'un club d'aviron donné
def find_nearest_station(lat, lon, stations, filter_keyboard) :
    # Filtrer les stations dont le libellé contient le mot "Seine" afin de ne capter que les débits le long de la Seine
    if filter_keyboard :
        stations = stations[stations['NOM_USUEL'].str.contains(filter_keyboard, case=False, na=False)]
    coords_station = stations[['LAT', 'LON']].values
    coords_point = [lat, lon]
    
    # Calcul des distances
    distances = distance.cdist([coords_point], coords_station, metric='euclidean')
    
    # Trouver l'index de la station la plus proche
    nearest_idx = distances.argmin()
    
    # Retourner le 'cdentite' et 'lbstationhydro' de la station la plus proche
    return stations.iloc[nearest_idx]['NUM_POSTE'], stations.iloc[nearest_idx]['NOM_USUEL']


# Ajout des colonnes d'identification de chaque station au DataFrame des adresses des clubs
def add_station_info_to_clubs(df_adresses_clubs, stations, filter_keyboard):
    # Appliquer la fonction à chaque ligne du DataFrame des adresses des clubs
    def get_station_info(row):
        return pd.Series(find_nearest_station(row['LAT'], row['LON'], stations, filter_keyboard))
    
    # Appliquer la fonction à chaque ligne
    df_adresses_clubs[['NUM_POSTE', 'NOM_USUEL']] = df_adresses_clubs.apply(get_station_info, axis=1)
    return df_adresses_clubs