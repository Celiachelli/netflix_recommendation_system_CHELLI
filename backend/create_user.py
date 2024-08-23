from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client.netflix_recommendation

def create_user(first_name, last_name, email, password, genre):
    hashed_password = generate_password_hash(password)
    user_id = db.users.insert_one({
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'password': hashed_password,
        'genre': genre
    }).inserted_id
    print(f"User created with id: {user_id}")

# Example usage
create_user('Test', 'User', 'test@user.com', 'password', 'Comedy')
