# Système d'Aide à la Décision Multicritère (TOPSIS)

Cette application web interactive est un outil d'aide à la décision (SAD) qui utilise 
l'algorithme mathématique MIN-MAX (Maxmin) et TOPSIS (Technique pour le classement des préférences par 
similarité à la solution idéale). Elle a été créée en Python en utilisant les 
bibliothèques Streamlit et Plotly.

Elle offre à l'utilisateur la possibilité de représenter un problème compliqué, 
d'ajouter ses propres critères en temps réel, de modifier l'importance des différents 
facteurs avec des curseurs, et de recevoir immédiatement une classification précise 
des options, présentée à travers des graphiques de décision sophistiqués.

## Fonctionnalités Principales

L'application s'articule autour de cinq piliers fonctionnels conçus pour offrir 
une expérience utilisateur fluide et une rigueur analytique maximale :

| Module | Description | Impact Décisionnel |
| :--- | :--- | :--- |
| **Modélisation Dynamique** | Configuration à la volée des dimensions de la matrice : critères (<kbd>2</kbd> à <kbd>10</kbd>) et alternatives (<kbd>2</kbd> à <kbd>15</kbd>). | Flexibilité totale face au problème traité. |
| **Orientation des Objectifs** | Prise en compte asymétrique des variables à **Maximiser** (ex: ROI, gains) ou à **Minimiser** (ex: Coûts, Risques, Délais). | Traduction fidèle de la réalité métier. |
| **Pondération Vectorielle** | Ajustement des poids via une matrice de curseurs (*sliders*) avec calcul temps réel de la somme relative (Somme = <kbd>1.0</kbd>). | Cohérence mathématique transparente. |
| **Formulaire Agile** | Matrice d'entrée adaptative générée dynamiquement selon la configuration des dimensions. | Saisie rapide et exempte d'erreurs de structure. |


## Analyses Visuelles et Cockpit Décisionnel

Une fois le moteur d'optimisation exécuté, l'interface génère instantanément trois niveaux de lecture complémentaires :

* **Livrable Stratégique**
    Une boîte de recommandation à haut contraste isole immédiatement l'alternative optimale avec son score d'adéquation précis. Un tableau de classement trié par rang vient appuyer cette conclusion.
* **Profils Multidimensionnels (Analyse Comparative)**
    Un diagramme Radar (*Spider Chart*) superpose les performances normalisées de chaque projet. Cela permet au décideur de repérer instantanément les forces et les faiblesses structurelles de chaque option.
* **Décomposition de la Performance (Analyse de Contribution)**
    Un graphique à barres empilées illustre la part exacte de responsabilité de chaque critère dans le score final, justifiant mathématiquement le gain ou la perte de rang d'un projet.


## Architecture des Fichiers

```Plaintext
├── app.py              # Code source principal de l'application (Interface & Algorithme)
├── README.md           # Documentation du projet (ce fichier)
└── venv/               # Environnement virtuel Python
```

## Prérequis et Installation

1. Cloner ou créer le répertoire du projet

```bash
git clone https://github.com/joshue-agape/Decision-Support-System.git
```

2. Installer les dépendances

```bash
pip install -r requirements.txt
```

3. Lancement de l'application

```bash
streamlit run app.py
```