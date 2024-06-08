from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = os.environ.get("DATABASE_PORT")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DATABASE = os.environ.get("REDIS_DATABASE")

SECRET_PHRASE = os.environ.get("SECRET_PHRASE")
SECRET_KEY = os.environ.get("SECRET_KEY")

SSL_CERT_FILE_PATH = os.environ.get("SSL_CERT_FILE_PATH")
SSL_KEY_FILE_PATH = os.environ.get("SSL_KEY_FILE_PATH")
