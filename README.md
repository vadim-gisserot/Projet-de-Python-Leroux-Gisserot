# Projet-de-Python-Leroux-Gisserot
## Genèse
L'aviron est un sport nautique qui consiste à naviguer sur des cours d'eau à l'aide d'une embarcation propulsée par la force des jambes, du dos et des bras. Pratiqué aussi bien en compétition qu'en loisir, l'aviron compte près de 150 000 pratiquants en France. L'activité se déroule principalement sur des "bassins", terme désignant une zone précise d'une rivière, d'un fleuve ou d'un lac.

La pratique de l'aviron est fortement influencée par les conditions naturelles des cours d'eau, notamment le débit. Un débit trop élevé peut rendre le bassin dangereux en raison des courants forts, des vagues et des risques de submersion. Face à la dégradation des conditions de pratique au cours des 20 dernières années (épisodes de crues à Paris de janvier à mars 2024, tempête de grêlons et fortes précipitations à Vichy en 2019 lors des championnats de France), la Fédération Française d'Aviron s'est emparée du problème et a commencé à développer une application permettant de remonter les conditions des bassins (vents, crues, etc.).

Alors que cette application est encore en développement, nous avons eu l'idée de créer notre propre solution : un modèle de prédiction du débit pour les jours à venir.

## Coeur du projet
Ce projet vise à modéliser le débit des fleuves et rivières français dans les jours à venir. Pour cette modélisation, nous nous sommes appuyés sur l'étude des conditions climatiques, notamment les précipitations et la température, qui jouent un rôle majeur dans l'évolution du niveau de l'eau et du débit des rivières.

Les fluctuations du débit, causées par des phénomènes météorologiques ou saisonniers, impactent directement la sécurité et la performance des pratiquants. Par exemple, la pratique est déconseillée lors de pluies intenses et strictement interdite en extérieur lorsque le débit est trop puissant. C'est pourquoi la prévision du débit des rivières est essentielle pour adapter les entraînements et les compétitions aux conditions changeantes de l'eau, assurant ainsi la sécurité des athlètes et la qualité de leur pratique.

## Structure
Le dossier data contient toutes les données importées de sources extérieures, incluant les données météorologiques, hydrométriques et les adresses des clubs d'aviron.
Le dossier utils regroupe toutes les fonctions utilisées dans le notebook, triées selon les différentes parties du projet qu'elles viennent compléter.
Enfin le notebook compte-rendu de l’analyse contient l'analyse des données, la modélisation des variations du débit, ainsi qu'une prédiction du débit et une présentation de notre "application", avec et sans résultats.

Bonne lecture,

Tara Leroux et Vadim Gisserot