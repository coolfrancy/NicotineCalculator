import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Connect to the PostgreSQL database
def connect_to_db():
    try:
        # Get database URL from environment variable
        DATABASE_URL = os.environ.get('DATABASE_URL')
        
        # Heroku's DATABASE_URL starts with "postgres://" but psycopg2 expects "postgresql://"
        if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f'Error connecting to db {e}')
        if conn:
            conn.close()
        return None
if __name__=='__main__':
    connect_to_db()