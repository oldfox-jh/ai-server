import psycopg2
import os

# chatbot db connection 가져오기
def get_chatbot_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
    except Exception as e:
        print(f"Error inserting data: {e}")

    return conn

