from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/netflix_recommendation"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'firstName' not in data or 'lastName' not in data or 'email' not in data or 'password' not in data or 'genre' not in data:
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user_id = mongo.db.users.insert_one({
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'email': data['email'],
        'password': hashed_password,
        'genre': data['genre']
    }).inserted_id

    return jsonify({"msg": "User created", "id": str(user_id)}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'email': data['email']})
    
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        return jsonify({"msg": "Login successful", "id": str(user['_id']), "genre": user['genre']}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = mongo.db.movies.find({'Series or Movie': 'Movie'}).limit(10)
    movie_list = []
    for movie in movies:
        movie_list.append({
            'title': movie['Title'],
            'genre': movie['Genre'],
            'image': movie['Image'],
            'summary': movie['Summary']
        })
    return jsonify({"movies": movie_list})

@app.route('/api/series', methods=['GET'])
def get_series():
    series = mongo.db.movies.find({'Series or Movie': 'Series'}).limit(10)
    series_list = []
    for serie in series:
        series_list.append({
            'title': serie['Title'],
            'genre': serie['Genre'],
            'image': serie['Image'],
            'summary': serie['Summary']
        })
    return jsonify({"series": series_list})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_id = data['user_id']
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    if user:
        genre = user['genre']
        recommendations = mongo.db.movies.find({"Genre": {"$regex": genre, "$options": "i"}}).limit(10)
        recommendation_list = [{
            "title": movie['Title'],
            "genre": movie['Genre'],
            "tags": movie.get('Tags', ''),
            "languages": movie.get('Languages', ''),
            "country_availability": movie.get('Country Availability', ''),
            "runtime": movie.get('Runtime', ''),
            "director": movie.get('Director', ''),
            "writer": movie.get('Writer', ''),
            "actors": movie.get('Actors', ''),
            "view_rating": movie.get('View Rating', ''),
            "imdb_score": movie.get('IMDb Score', ''),
            "awards_received": movie.get('Awards Received', ''),
            "awards_nominated_for": movie.get('Awards Nominated For', ''),
            "boxoffice": movie.get('Boxoffice', ''),
            "release_date": movie.get('Release Date', ''),
            "netflix_release_date": movie.get('Netflix Release Date', ''),
            "production_house": movie.get('Production House', ''),
            "summary": movie['Summary'],
            "netflix_link": movie.get('Netflix Link', ''),
            "image": movie['Image']
        } for movie in recommendations]
        return jsonify({"recommendations": recommendation_list})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)
