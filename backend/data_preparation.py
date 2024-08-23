import pandas as pd
from pymongo import MongoClient

# Charger le fichier CSV avec l'encodage correct
data = pd.read_csv('../data/NetflixDataset.csv', encoding='ISO-8859-1')  # Remplacez 'ISO-8859-1' par l'encodage correct

# Nettoyer les données (par exemple, supprimer les valeurs manquantes)
data.dropna(inplace=True)

# Transformer les données si nécessaire (par exemple, convertir les dates en format datetime)
if 'date' in data.columns:
    data['date'] = pd.to_datetime(data['date'])

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.netflix_recommendation
collection = db.movies

# Insérer les données dans MongoDB
collection.insert_many(data.to_dict('records'))

print("Data loaded into MongoDB.")
