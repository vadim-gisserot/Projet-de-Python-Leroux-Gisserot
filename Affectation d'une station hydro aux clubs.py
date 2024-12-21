import pandas as pd
import os
os.system("pip install geopy")
from geopy.geocoders import Nominatim
from scipy.spatial import distance

#Création du dataset clubs avirons

df_adresses_clubs = pd.read_csv('/home/onyxia/work/Projet-de-Python-Leroux-Gisserot/Datasets/adresses_clubs.csv', sep=';', header=0)

#CRéation d'un datawet restreint pour test et pour gérer les erreurs d'adresses (je suis sure que dans les 2 premières il n'y a pas d'erreur)
df_adresses_clubs = df_adresses_clubs.head(2)

#Modifcations à apporter dans le fichier CSV
remplacements = {"Île Lacroix ": "", "Chem.": "Chemin", " Rue Frédéric Ogerau" : "7 Impasse de la Chaussée","bis" : "", "2 Bd du Général Leclerc" : "82 Bd du Général Leclerc", "Complexe sportif de l'île du Pont":"Rue de l'île du Pont" }

# Appliquer les remplacements sur des colonnes spécifiques
colonnes_a_modifier = ["Adresse"]
df_adresses_clubs['Adresse'] = df_adresses_clubs[colonnes_a_modifier].replace(remplacements)

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="geoapi")

# Fonction pour récupérer les coordonnées
def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Erreur pour l'adresse {address}: {e}")
        return pd.Series([None, None])

# Appliquer la fonction à chaque adresse
df_adresses_clubs[['Latitude', 'Longitude']] = df_adresses_clubs['Adresse'].apply(get_coordinates)
print(df_adresses_clubs)


#Création du datasets stations hydrométriques
df_liste_stations = pd.read_csv('/home/onyxia/work/Projet-de-Python-Leroux-Gisserot/Datasets/liste-stations.csv', sep=';', header=0)

#Filtration du dataset pour ne garder que les stations hydrométriques encore en exploitation
df_liste_stations_filtered = df_liste_stations[df_liste_stations['dtfermeture'].isna()]
print(df_liste_stations_filtered.head())
df_liste_stations_clean  = df_liste_stations_filtered.drop(['typestation', 'dtmiseservice', 'dtfermeture'], axis=1)
print(df_liste_stations_clean)


# Fonction pour trouver la station la plus proche d'un club d'aviron donné
def find_nearest_station(lat, lon, stations):
    
    coords_station = stations[['latitude', 'longitude']].values
    coords_point = [lat, lon]
    
    # Calcul des distances
    distances = distance.cdist([coords_point], coords_station, metric='euclidean')
    
    # Trouver l'index de la station la plus proche
    nearest_idx = distances.argmin()
    
    # Retourner le 'cdentite' et 'lbstationhydro' de la station la plus proche
    return stations.iloc[nearest_idx]['cdentite'], stations.iloc[nearest_idx]['lbstationhydro']

# Ajout des colonnes d'identification de la station au DataFrame des adresses des clubs
def add_station_info_to_clubs(df_adresses_clubs, stations):
    # Appliquer la fonction à chaque ligne du DataFrame des adresses des clubs
    def get_station_info(row):
        return pd.Series(find_nearest_station(row['Latitude'], row['Longitude'], stations))
    
    # Appliquer la fonction à chaque ligne
    df_adresses_clubs[['cdentite', 'lbstationhydro']] = df_adresses_clubs.apply(get_station_info, axis=1)
    return df_adresses_clubs

# Appliquer la fonction et ajouter les colonnes
df_adresses_clubs = add_station_info_to_clubs(df_adresses_clubs, df_liste_stations_clean)

# Vérification que ca a bien fonctionné
print(df_adresses_clubs)
print(df_adresses_clubs['cdentite'])

#Voila les stations desquelles on doit télécharger l'historique des données hydro à la main