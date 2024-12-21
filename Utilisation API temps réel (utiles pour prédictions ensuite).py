from datetime import datetime, timedelta
from urllib.request import Request, urlopen
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt



# Création de l'URL d'accès à l'API en fonction des paramètres ci-dessus
url = "https://hubeau.eaufrance.fr/api/v1/ecoulement/observations?format=json&code_departement=88&libelle_cours_eau=Moselle&date_observation_min=2021-01-01&size=20"
# Récupération des donnéesen csv et conversaion en dataframe
with urlopen(url) as response:
    df = pd.read_csv(response, sep=';')

print(df)


# Réalisation d'un graphique sur le débit à Paris
# Conversion des dates en datetime
df["date_obs"] = pd.to_datetime(df["date_obs"])
# Conversion des débits en m3/s
df["resultat_obs"] = df["resultat_obs"]/1000

fig, ax = plt.subplots(figsize=(12, 6), facecolor='w')

ax.plot(df.date_obs, df.resultat_obs)

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
plt.savefig('Débit de la Seine à Paris-Austerlitz.png')
