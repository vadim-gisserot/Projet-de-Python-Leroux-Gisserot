#Importation des packages necessaires
import warnings
import matplotlib.pyplot as plt
import pandas as pd

# Fonction pour calculer des corrélations entre variables
def correlation1(df, var, start, end, step):

    # On restreint les messages d'erreur "inutiles" (sur la performance des calculs)
    warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
    
    for lag in range(start, end, step):  # Tester de 1 à 25 heures de décalage
        df[f"{var}_lag_{lag}"] = df[var].shift(lag)
        print(f"Corrélation avec {var} décalé de {lag} heure(s) :", df["debit"].corr(df[f"{var}_lag_{lag}"]))


# Fonction pour calculer des corrélations entre variables avec différentes fenêtres
def correlation2(df, column, target, periods):
    correlations = []
    for hours in periods:
        # Calcul de la somme de la colonne avec un décalage et une fenêtre donnée
        df[f"{column}_sum_{hours}h"] = df[column].shift(1).rolling(window=hours, min_periods=1).sum()
        # Calcul de la corrélation avec la cible
        corr = df[target].corr(df[f"{column}_sum_{hours}h"])
        correlations.append((hours, corr))
    return correlations


# Fonction pour faire un graphique des corrélations
def plot_correlations(correlations, title):
    windows = [window for window, _ in correlations]  # Extraire les fenêtres
    corrs = [corr for _, corr in correlations]       # Extraire les corrélations

    plt.figure(figsize=(10, 6))
    plt.plot(windows, corrs, marker="o", linestyle="-", color="b", label="Corrélation")
    plt.title(title, fontsize=14)
    plt.xlabel("Fenêtre horaire (h))", fontsize=12)
    plt.ylabel("Corrélation", fontsize=12)
    plt.xticks(ticks=windows, labels=[f"{w//24}j" if w % 24 == 0 else f"{w}h" for w in windows], rotation=45)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()


# Fonction pour créer les variables explicatives
def create_features(df):
    
    warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

    # Moyennes des 3 dernières semaines
    rolling_window = 4 * 7 * 24  # 4 semaines en heures
    df["RR1_sum_4w"] = df.groupby("Club")["RR1"].transform(lambda x: x.shift(24).rolling(rolling_window, min_periods=1).sum())
    df["T_mean_4w"] = df.groupby("Club")["T"].transform(lambda x: x.shift(24).rolling(rolling_window, min_periods=1).mean())
    df["debit_mean_1d"] = df.groupby("Club")["debit"].transform(lambda x: x.shift(24).rolling(24, min_periods=1).mean())
    return df
