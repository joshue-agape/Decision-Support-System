# Système d'Aide à la Décision Multicritère : Approches TOPSIS & Min-Max 

Bienvenue dans cette application web interactive conçue pour simplifier la prise de décision face à des choix complexes. Ce système d'aide à la décision (SAD) combine deux approches mathématiques complémentaires : la méthode **Min-Max (Maximin)** pour les profils prudents axés sur la sécurité, et la méthode **TOPSIS** (*Technique for Order of Preference by Similarity to Ideal Solution*) pour une vision d'ensemble équilibrée. 

Développé en Python avec **Streamlit** et **Plotly**, cet outil permet de structurer un problème, d'ajuster l'importance de chaque critère en temps réel et de visualiser instantanément les meilleures options grâce à des graphiques clairs et interactifs. 

---

## Ce que fait l'application 

Pour vous aider à choisir la meilleure alternative, l'application s'appuie sur quatre étapes clés, pensées pour être à la fois simples et rigoureuses : 

| Ce que vous contrôlez | Comment ça marche | Ce que cela vous apporte |
| :--- | :--- | :--- |
| **Structure sur-mesure** | Ajustez instantanément le nombre de critères (<kbd>2</kbd> à <kbd>10</kbd>) et de projets (<kbd>2</kbd> à <kbd>15</kbd>). | L'outil s'adapte exactement à votre problème, sans compromis. |
| **Objectifs clairs** | Définissez ce qui doit être **Maximisé** (gains, ROI) ou **Minimisé** (coûts, risques, délais). | Les calculs respectent la réalité et les contraintes de votre métier. |
| **Poids visuels** | Réglez l'importance de chaque facteur avec des curseurs. Le système équilibre automatiquement le total à <kbd>1.0</kbd>. | Pas besoin de calculer de tête, la cohérence mathématique est transparente. |
| **Saisie intuitive** | Un tableau dynamique se génère tout seul pour vous laisser entrer vos données brutes. | Vous gagnez du temps et évitez les erreurs de saisie. |

---

## Analyse des résultats et cockpit décisionnel 

Dès que vous lancez le calcul, l'application traduit les calculs mathématiques en trois outils visuels simples à interpréter pour guider votre choix : 

* **Le verdict stratégique**
  Un encadré visuel met immédiatement en valeur le projet gagnant avec son score précis. Un tableau classe ensuite toutes les autres options du premier au dernier rang pour valider la conclusion.
* **Le profil des projets (Vue comparative)**
  Un graphique Radar (*Spider Chart*) superpose les performances de chaque alternative sur tous les critères en même temps. C'est le meilleur moyen de repérer d'un coup d'œil les points forts et les faiblesses de chaque option.
* **L'origine de la performance (Vue contribution)**
  Un graphique à barres empilées vous montre exactement quel critère a pesé le plus lourd dans le score final de chaque projet. Vous comprenez enfin *pourquoi* un projet est premier ou dernier.

---

## Organisation des fichiers

```text
├── app.py              # Code source principal de l'application (Interface & Algorithme)
├── README.md           # Documentation du projet (ce fichier)
└── venv/               # Environnement virtuel Python
```

## Installation et démarrage rapide  

1. Récupérer le projet  
Commencez par cloner le dépôt sur votre machine :  

```bash
git clone https://github.com/joshue-agape/Decision-Support-System.git
```

2. Installer les outils nécessaires  
Installez les bibliothèques indispensables au bon fonctionnement du simulateur :  

```bash
pip install -r requirements.txt
```

3. Lancer l'application  
Il ne vous reste plus qu'à démarrer l'interface locale dans votre navigateur :  

```bash
streamlit run app.py
```