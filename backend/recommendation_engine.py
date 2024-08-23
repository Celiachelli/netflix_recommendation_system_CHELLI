# backend/recommendation_engine.py

import pandas as pd
from pymongo import MongoClient
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Concatenate
from tensorflow.keras.optimizers import Adam

# Charger les données d'entraînement depuis MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.netflix_recommendation
movies_collection = db.movies
data = pd.DataFrame(list(movies_collection.find()))

# Préparer les données pour le modèle
user_ids = data['user_id'].values
item_ids = data['movie_id'].values
ratings = data['rating'].values

num_users = data['user_id'].nunique()
num_items = data['movie_id'].nunique()

# Construire le modèle
user_input = Input(shape=(1,), name='user_input')
item_input = Input(shape=(1,), name='item_input')

user_embedding = Embedding(input_dim=num_users, output_dim=50, name='user_embedding')(user_input)
item_embedding = Embedding(input_dim=num_items, output_dim=50, name='item_embedding')(item_input)

user_vector = Flatten()(user_embedding)
item_vector = Flatten()(item_embedding)

concat = Concatenate()([user_vector, item_vector])
dense_1 = Dense(128, activation='relu')(concat)
dense_2 = Dense(64, activation='relu')(dense_1)
output = Dense(1, activation='linear')(dense_2)

model = Model(inputs=[user_input, item_input], outputs=output)
model.compile(optimizer=Adam(lr=0.001), loss='mse')

# Entraîner le modèle
model.fit([user_ids, item_ids], ratings, epochs=5, batch_size=32)

# Sauvegarder le modèle
model.save('recommendation_model.h5')

print("Model trained and saved.")
