# ADOMC — Système d'Aide à la Décision Multicritère
### Approche Min-Max (Analyse du Regret)

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Présentation

**ADOMC** est une application web interactive permettant d’analyser et de comparer plusieurs alternatives selon plusieurs critères, en utilisant une approche robuste basée sur la **minimisation du regret maximal (Min-Max)**.

 L’objectif : **prendre des décisions fiables même dans les pires scénarios.**

---

## Pourquoi utiliser ADOMC ?

Contrairement aux méthodes classiques qui maximisent la performance moyenne, ADOMC :

- Sécurise la décision face à l’incertitude
- Identifie les risques critiques (critères bloquants)
- Minimise les mauvaises surprises
- Fournit une analyse visuelle claire et immédiate

---

## Méthode utilisée : Min-Max (Regret)

### Principe

Pour chaque alternative :

1. Normalisation des performances
2. Calcul du regret par critère
3. Identification du pire regret
4. Sélection de l’alternative avec le regret minimal

### Formule clé

```
Regret = poids × (1 - performance normalisée)
Score Min-Max = max(regrets)
```

 **Meilleur choix = score le plus faible**

---

## Fonctionnalités

### Configuration
- Nombre de critères : 2 à 10
- Nombre d’alternatives : 2 à 15
- Choix : Maximiser / Minimiser

### Pondération
- Sliders interactifs
- Normalisation automatique des poids

### Saisie des données
- Tableau dynamique
- Valeurs personnalisables

---

## Visualisations

### Recommandation automatique
- Meilleure alternative
- Score Min-Max
- Critère bloquant

### Classement
- Ordre de robustesse
- Lecture intuitive du risque

### Radar (Spider Chart)
- Comparaison globale des performances

### Barres empilées
- Contribution des critères au regret

---

## Structure du projet

```
├── app.py              # Application principale
├── README.md           # Documentation
├── requirements.txt    # Dépendances
└── venv/               # Environnement virtuel (optionnel)
```

---

## Installation

```bash
git clone https://github.com/joshue-agape/Decision-Support-System.git
cd Decision-Support-System
pip install -r requirements.txt
```

---

## Lancement

```bash
streamlit run app.py
```

Puis ouvrir dans le navigateur :

```
http://localhost:8501
```

---

## Cas d’usage

- Sélection de projets d’investissement
- Décisions stratégiques
- Analyse de risques
- Comparaison de solutions techniques
- Études académiques

---

## Philosophie

> “Minimiser le pire scénario pour garantir une décision robuste.”

---

## Améliorations futures

- Ajout de méthodes multicritères (AHP, TOPSIS, ELECTRE)
- Export PDF / Excel
- Sauvegarde des scénarios
- Analyse de sensibilité des poids
- Interface multi-utilisateurs

---

## Licence

Ce projet est sous licence MIT — libre d’utilisation et de modification.

---

 N'hésite pas à contribuer ou à améliorer le projet !
