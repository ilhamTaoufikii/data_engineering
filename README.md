# Medication Data Pipeline

Ce projet est un pipeline de données construit avec Flask et Pandas pour traiter des données sur les médicaments, provenant de fichiers CSV et JSON. L'objectif principal est de récupérer des informations sur les médicaments et leurs mentions dans des articles scientifiques (PubMed) et des essais cliniques (Clinical Trials), et de générer un fichier JSON avec les résultats

## Fonctionnalités

- **Chargement de fichiers locaux** : Le pipeline charge des fichiers CSV contenant des données sur les médicaments, PubMed et les essais cliniques, ainsi qu'un fichier JSON pour PubMed
- **Traitement des données** : Il analyse les données pour identifier les mentions des médicaments dans les titres des publications PubMed et des essais cliniques
- **Génération de fichier JSON** : Un fichier JSON est généré, contenant des informations sur les médicaments et leurs mentions dans les articles scientifiques
- **API Flask** : Le pipeline est exposé via une API Flask, permettant de lancer le traitement via un simple appel HTTP

## Prérequis

- **Python 3.7+**
- **Bibliothèques Python** :
  - Flask
  - Pandas
  - JSON
  - re
  - os
  - codecs
  - chardet
- **Système de fichiers local** pour stocker les fichiers CSV et JSON utilisés par l'application.

## Installation

1. Clonez ce repository :
   git clone https://github.com/ilhamTaoufikii/data_engineering.git
   cd data_engineering

## installez les dépendances
pip install -r requirements.txt

## Structure du projet
data_engineering/
├── dags/                                 # Répertoire pour les fichiers DAG d'Airflow
│   └── flask_medication_pipeline.py      # DAG pour orchestrer le pipeline
├── src/                                  # Répertoire source pour le code Python
│   ├── app.py                            # Application Flask pour exécuter le pipeline
│   ├── config.py                         # Stores configuration variables such as file paths
│   ├── pipeline.py                       # Contains functions to run the pipeline, data transformation 
│   ├── utils.py                          # includes utility functions to support repetitive tasks
│   ├── tmp/                              # Dossier pour stocker les fichiers de sortie JSON 
├── config/                               # Répertoire pour les fichiers de configuration
│   └── config.yaml                       # Configuration du pipeline (fichiers d'entrée, etc.)
├── data/                                 # Répertoire pour stocker des exemples de données (localement)
│   ├── drugs.csv
│   ├── pubmed.csv
│   ├── pubmed.json
│   └── clinical_trials.csv
├── Dockerfile                            # Fichier Docker pour construire l'image Cloud Run
├── .dockerignore                         # Fichier pour exclure certains fichiers de l'image
├── requirements.txt                      # Liste des dépendances Python
├── .gitignore                            # Fichier pour exclure les fichiers non suivis dans Git
├── README.md                             # Documentation du projet
└── LICENSE                               # Licence du projet

## Utilisation
Lancer l'application Flask localement
Exécutez l'application Flask avec la commande suivante : python app.py

L'application démarrera sur http://127.0.0.1:8080/run_pipeline par défaut
Si l'exécution est réussie, un message avec le chemin du fichier généré sera retourné :
{
  "message": "Pipeline executed successfully",
  "output_file": "tmp/medication_mentions.json"
}
Pour tester également la partie BONUS 
  •Extraire le nom du journal qui mentionne le plus de médicaments différents.
  •Pour un médicament donné, trouver l’ensemble des médicaments mentionnés par les mêmes journaux référencés par les publications scientifiques (PubMed) mais non les tests cliniques (Clinical Trials) 
Utilisez les liens suivants :
  http://127.0.0.1:8080/journal_with_most_unique_drugs
  http://127.0.0.1:8080/other_drugs_in_pubmed/aspirin (et choisissez le médicament que vous voulez)
## Gestion des erreurs
Si un fichier requis est introuvable, le pipeline renverra une erreur avec un message détaillant le problème
En cas de problème lors de la récupération des données ou du traitement des fichiers, un message d'erreur sera retourné à l'utilisateur

## Tests de l'API Flask app_test.py
Ce fichier contient les tests unitaires pour les routes de l'API Flask. Les tests vérifient la création des fichiers de sortie après l'exécution des différentes routes.
Pour Lancer les tests
python -m unittest app_test.py

## Améliorations futures
Ajouter la gestion des erreurs plus détaillée pour différents cas d'utilisation
Ajouter des tests unitaires pour chaque fonction
Optimiser les performances lors de l'analyse des grands fichiers CSV
stocker les fichiers de données dans le Google cloud storage par exemple





