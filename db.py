import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection_str = os.getenv("DATABASE_URL")

def get_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        print(f"Errorconnecting to database: {e}")
        return None
    
def init_database():
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        with open("schema.sql", "r") as f:
            schema = f.read()
            
        cursor.execute(schema)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
init_database()