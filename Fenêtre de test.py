import requests
from geopy.geocoders import Nominatim

# Création d'une fonction qui trouve la latitude et la longitude d'une ville à partir de son nom.
def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="station_locator")
    location = geolocator.geocode(city_name)
    
    if location:
        print(f"Coordonnées de {city_name} : Latitude = {location.latitude}, Longitude = {location.longitude}")
        return location.latitude, location.longitude
    else:
        print(f"Impossible de trouver la géolocalisation pour {city_name}.")
        return None, None

# Création d'une fonction qui trouve les stations hydrométriques priche d'uen lat et d'une long données
def get_station_by_coordinates(lat, lon):

    # URL de l'API Hubeau pour les stations hydrométriques
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/referentiel/stations"
    
    # Paramètres de la requête : rechercher par latitude et longitude
    params = {
        "lat": lat,
        "lon": lon,
        "size": 10  # Limiter le nombre de résultats
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Vérifie si la requête a réussi
        stations_data = response.json().get("data", [])
        
        if stations_data:
            print(f"\nStations proches de ({lat}, {lon}) :")
            for station in stations_data:
                print(f"Code Station : {station['code_station']}, Nom : {station['libelle_station']}")
            return stations_data
        else:
            print(f"Aucune station trouvée près de ({lat}, {lon}).")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return []

# Étape 1 : Demander le nom de la commune
commune = input("Entrez le nom de la commune : ")

# Étape 2 : Obtenir les coordonnées GPS de la commune
latitude, longitude = get_coordinates(commune)

if latitude and longitude:
    # Étape 3 : Trouver les stations hydrométriques proches de ces coordonnées
    get_station_by_coordinates(latitude, longitude)

