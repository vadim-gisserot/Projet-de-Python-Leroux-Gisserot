import glob
import gzip
import requests

import pandas as pd
import geopandas as gpd
from tqdm import tqdm


# Fonction pour télécharger et lire un fichier CSV depuis un URL
def read_csv_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Decompress the content
        df = pd.read_csv(url, compression='gzip', sep=';', encoding='utf-8')
        return df
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")
        return None


# Fonction pour télécharger les données météo par département
def load_department_data(
    department_id,
    relevant_columns=["DEPARTMENT_ID", "NUM_POSTE", "NOM_USUEL", "LAT", "LON", "AAAAMMJJHH","RR1", "T"],
    base_url_prefix="https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/HOR/H_",
    base_url_suffix="_latest-2023-2024.csv.gz",
):
    url = f"{base_url_prefix}{department_id}{base_url_suffix}"
    df = read_csv_from_url(url)
    
    if df is not None:
        # Add a new column for department number
        df["DEPARTMENT_ID"] = department_id

    return df[relevant_columns]


# Function pour sauvegarder les données dans un dossier
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
    # On formatte les dates pour les utiliser ultérieurement dans les graphes
    df[date] = pd.to_datetime(df[date], format="%Y%m%d%H")

    return df


# Fonction pour créer un dataframe propre ne contenant qu'une seule station
def station_au_hasard(x, df1):
    
    df2 = df1[df1["NOM_USUEL"] == x]
    # On ne conserve que les colonnes d'intéret
    df2 = df2[["AAAAMMJJHH", "RR1", "T"]]
    # On crée une copie pour éviter les intéractions avec le dataframe de base
    df2 = df2.copy()
    # On se débarrasse des valeurs manquantes
    df2 = df2.dropna(subset=['RR1', 'T'])

    return df2


# Fonction pour importer la base de données fluviales
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