import pandas as pd
from pymongo import MongoClient
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.netflix_recommendation

# Charger les données des films et des utilisateurs
movies = pd.DataFrame(list(db.movies.find()))

# Vérifier les colonnes du DataFrame
print(movies.columns)

# Vérifiez si les colonnes nécessaires existent dans votre dataset
required_columns = ['Title', 'IMDb Score']
for col in required_columns:
    if col not in movies.columns:
        raise ValueError(f"Column {col} is missing from the dataset")

# Encoder les titres des films
movie_encoder = LabelEncoder()
movies['movie_id'] = movie_encoder.fit_transform(movies['Title'])

# Créer les embeddings pour les films
movie_input = Input(shape=(1,))
movie_embedding = Embedding(len(movie_encoder.classes_), 50)(movie_input)
movie_vec = Flatten()(movie_embedding)

# Ajouter une couche dense pour la prédiction de la note
dense = Dense(1)(movie_vec)

# Créer le modèle
model = Model(inputs=movie_input, outputs=dense)
model.compile(optimizer=Adam(), loss='mean_squared_error')

# Entraîner le modèle
ratings = movies['IMDb Score']
model.fit(movies['movie_id'], ratings, epochs=5, verbose=1)

# Sauvegarder le modèle
model.save('recommendation_model.h5')
print("Model trained and saved as recommendation_model.h5")
