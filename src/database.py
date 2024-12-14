# Database class handles interactions with the MongoDB database, including user 
# management and score tracking.

from dotenv import load_dotenv  # Importing load_dotenv to load environment variables from a .env file
import os  # Importing os to interact with the operating system
from pymongo import MongoClient  # Importing MongoClient to interact with MongoDB
import bcrypt  # Importing bcrypt for password hashing

class Database():
    def __init__(self):
        load_dotenv()  # Load environment variables from a .env file
        self.mongo_uri = os.getenv("MONGO_URI")  # Get the MongoDB URI from environment variables
        self.client = MongoClient(self.mongo_uri)  # Create a MongoDB client
        self.db = self.client.get_database("db1")  # Get the database named "db1"
        self.users_collection = self.db.get_collection('users')  # Get the "users" collection from the database

    def check_user(self, username):
        user = self.users_collection.find_one({"username": username})
            
        if user:
            return True
        else:
            return False
        
    def add_user(self, username):
        """Adds a new user to the database."""
        self.users_collection.insert_one({
            "username": username,
        })

        print("User added successfully!")

    def add_score(self, username, score):
        """Updates the score of an existing user in the database."""
        self.users_collection.update_one(
            {"username": username},
            {"$set": {"score": score}}
        )

        print("Score added successfully!")

    def get_score(self, username):
        """Retrieves the score of a user from the database."""
        user = self.users_collection.find_one({"username": username})
        return user.get('score')
    
    def get_dict_of_all_scores_and_users(self):
        """Returns a dictionary of all users and their scores."""
        users = self.users_collection.find({})
        scores = {}
        for user in users:
            scores[user.get('username')] = user.get('score')
            if user.get('score') is None:
                scores[user.get('username')] = 0
        return scores