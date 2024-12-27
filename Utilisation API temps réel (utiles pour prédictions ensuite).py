from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt



#Stations à télécharger
station = "H308000101"
club_lié = clubs_hydro_meteo[clubs_hydro_meteo['NUM_NHS'] == station]

#Période : les 10 derniers jours
debut = (datetime.now()-timedelta(30)).isoformat() 

url_API = "https://hubeau.eaufrance.fr/api/v1/hydrometrie/observations_tr.csv"
url = url_API+ f"?code_entite={station}&grandeur_hydro=Q&size=10000&date_debut_obs={debut}"

# Récupération des donnéesen csv et conversaion en dataframe
with urlopen(url) as response:
    debit_jours_precdents = pd.read_csv(response, sep=';')

# Sélectionner les colonnes nécessaires
print(debit_jours_precdents.columns)
debit_jours_precdents = debit_jours_precdents[['code_station', 'resultat_obs', 'date_obs']]
print(debit_jours_precdents)


# Réalisation d'un graphique sur le débit des 30 derniers jours dans la station prise en compte
# Conversion des dates en datetime
debit_jours_precdents["date_obs"] = pd.to_datetime(debit_jours_precdents["date_obs"])
# Conversion des débits en m3/s
debit_jours_precdents["resultat_obs"] = debit_jours_precdents["resultat_obs"]/1000

fig, ax = plt.subplots(figsize=(12, 6), facecolor='w')

ax.plot(debit_jours_precdents.date_obs, debit_jours_precdents.resultat_obs)

# Affichage du cadrillage
ax.grid(True, alpha=0.5)

# Mise en forme de l'axe des x
days = mdates.DayLocator()
ax.xaxis.set_major_locator(days)
day_fmt = mdates.DateFormatter('%d/%m')
ax.xaxis.set_major_formatter(day_fmt)

# Nom des axes
ax.set_ylabel("Débit (m3/s)")
ax.set_xlabel("Date")

plt.show()
plt.savefig('Débit de la Seine pour le club {club_lié}')
