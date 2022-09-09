from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.environ.get('postgres')
DATABASE_NAME_2 = os.environ.get('postgres')
DATABASE_PORT = os.environ.get('5432')
DATABASE_OWNER = os.environ.get('postgres')
DATABASE_PASSWORD = os.environ.get(' ')