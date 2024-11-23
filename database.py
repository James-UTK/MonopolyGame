# Handles the database connection and provides functions to interact with the database (e.g., add players, fetch data).
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

def connect(print_message=False):
    # Establishes a connection to the PostgreSQL database using credentials from environment variables.

    try:
        # Establish connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        if print_message:
            print("Database connection successful!")
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None
