import pandas as pd
import os
os.system("pip install geopy")
from geopy.geocoders import Nominatim
from scipy.spatial import distance

#Création du dataset clubs avirons

df_adresses_clubs = pd.read_csv('/home/onyxia/work/Projet-de-Python-Leroux-Gisserot/Datasets/adresses_clubs.csv', sep=';', header=0)

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="geoapi", timeout=15)

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
    # Filtrer les stations dont le libellé contient le mot "Seine"
    stations = stations[stations['lbstationhydro'].str.contains('Seine', case=False, na=False)]
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

liste_stations_a_récupérer = []
for element in df_adresses_clubs['cdentite']:
    if element not in liste_stations_a_récupérer :
        liste_stations_a_récupérer.append(element)

#Voila les stations desquelles on doit télécharger l'historique des données hydro à la main
print("Les stations dont il faut récupérer les données dans les archives hydrométriques sont : " + ", ".join(liste_stations_a_récupérer))

#Cleaning des datasets et insertion dans un dictionnaire pour y avoir accès à tous en même temps
# Création de la liste des fichiers à traiter
liste_stations_a_récupérer 

# Liste contenant les fichiers CSV à traiter
fichiers_stations_hydro = []

#Path a utiliser : 
chemin_dossier = "/home/onyxia/work/Projet-de-Python-Leroux-Gisserot/Datasets/"

# Parcourir chaque numéro dans la liste
for station in liste_stations_a_récupérer:
    fichier = f"{chemin_dossier}{station}.csv"  # Construire le nom du fichier
    fichiers_stations_hydro.append(fichier)  # Ajouter le fichier à la liste

# Résultat final
print("Fichiers trouvés :", fichiers_stations_hydro)

# Dictionnaire pour stocker les DataFrames
dictionnaire_df_stations_hydro = {}


for fichier in fichiers_stations_hydro:
    # Lire le fichier
    df = pd.read_csv(fichier)
    
    # Supprimer les colonnes inutiles
    df = df.drop(columns=["Statut", "Qualification", "Méthode", "Continuité"], errors="ignore")
    print(df)
    # Convertir la colonne "Valeur (en m³/s)" en entier
    df["Valeur (en m³/s)"] = pd.to_numeric(df["Valeur (en m³/s)"].astype(str).str.replace(",", "").str.replace('"', ""), errors="coerce").fillna(0).astype(int)
    
    # Renommer dynamiquement le DataFrame
    nom_dataframe = f"df_débit_{fichier.split('.')[0]}"  # Supprime l'extension .csv du nom
    dictionnaire_df_stations_hydro[nom_dataframe] = df  # Stocker dans un dictionnaire

for nom, df in dictionnaire_df_stations_hydro.items():
    print(f"Les 5 premières lignes de {nom}:")
    print(df.head())  # Affiche les 5 premières lignes
    print()  # Ligne vide pour la lisibilité

#On a finalement un dictionnaire avec tous les dataframes des bases hydro à l'interieur, avec uniquement le débit par heure à chaque station.