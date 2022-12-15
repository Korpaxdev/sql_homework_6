from os import getcwd, getenv
from os.path import join

from dotenv import load_dotenv

from classes.database import BooksDb

dotenv_path = join(getcwd(), '.env')
load_dotenv(dotenv_path)

DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_NAME = getenv('DB_NAME')
DB_HOST = getenv('DB_HOST')
DSN = f'postgresql://{DB_USER}:@{DB_HOST}:5432/{DB_NAME}'

db = BooksDb(DSN)
db.create_tables()
db.insert_data_from_json('data.json')
db.get_publisher_info()
