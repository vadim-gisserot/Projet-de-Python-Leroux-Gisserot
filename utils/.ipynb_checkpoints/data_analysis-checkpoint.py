import requests
import warnings

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.pyplot as plt

from cartopy.io import DownloadWarning


# Fonction pour créer une carte de France avec les figurés d'intérêt
def carte_figures(df1, df2):
   
    # On supprime les messages d'avertissement inutiles
    warnings.simplefilter("ignore", DownloadWarning)
    
    # On crée la carte avec cartopy
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.Mercator()})
    ax.set_extent([-3, 6, 47, 50.5], crs=ccrs.PlateCarree())
    
    # On ajoute les features de base
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAND, facecolor='white', linewidth=0.5)
    ax.add_feature(cfeature.OCEAN, facecolor='white')
    
    # On ajoute les cours d'eau (en bleu), les stations météo (en rouge),
    # les stations hydrométriques (en vert) et les clubs d'aviron (en noir)
    ax.add_geometries(df1.geometry, crs=ccrs.PlateCarree(), edgecolor='blue', facecolor='none', linewidth=0.5)
    ax.scatter(
        df2['LON'], df2['LAT'], color='red', marker='o', s=3, 
        transform=ccrs.PlateCarree(), label="Stations"
    )
    
    plt.show()


# Fonction pour tracer les différents graphiques
def trace_graphique(x, y, titre, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, linestyle="-", color="blue", label=f"{ylabel}")
    
    # Personnalisation du graphe
    plt.title(titre, fontsize=14)
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.xticks(rotation=45)  # Rotation des dates sur l'axe X pour plus de lisibilité
    plt.tight_layout()  # Ajuste les marges pour éviter que les textes soient coupés
    plt.show()