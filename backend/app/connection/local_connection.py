
import psycopg2
import os
from dotenv import load_dotenv 


load_dotenv()  

#DB_NAME=hurricanes
#DB_USER=Postgres
#DB_PASSWORD=matthew02
#DB_HOST=localhost  
#DB_PORT=5432




def get_db_connection():
    try:
        
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None



if get_db_connection():
    print('Connected successfully')
else:
    print('Error connecting.')



