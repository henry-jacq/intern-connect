import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASS'),
)

my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS internconnect")
my_cursor.execute("USE internconnect")

my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
    print(db[0])