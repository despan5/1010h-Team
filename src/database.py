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

    def add_user(self):
        username = input("Enter username: ")  # Prompt the user to enter a username
        password = input("Enter password: ")  # Prompt the user to enter a password
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hash the password using bcrypt
        self.users_collection.insert_one({
            "username": username,
            "hashed_password": hashed.decode('utf-8')  # Store the hashed password in the database
        })

    def login_user(self):
        username = input("Enter username: ")  # Prompt the user to enter a username
        password = input("Enter password: ")  # Prompt the user to enter a password
        
        user = self.users_collection.find_one({"username": username})  # Find the user in the database by username

        if user and bcrypt.checkpw(password.encode('utf-8'), user['hashed_password'].encode('utf-8')):  # Check if the password matches
            print("Login successful!")  # Print success message if the password matches
        else:
            print("Invalid username or password")  # Print error message if the username or password is incorrect