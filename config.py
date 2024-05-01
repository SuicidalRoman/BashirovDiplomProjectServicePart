from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_HOST=os.environ.get("DATABASE_HOST")
DATABASE_PORT=os.environ.get("DATABASE_PORT")
DATABASE_USER=os.environ.get("DATABASE_USER")
DATABASE_PASSWORD=os.environ.get("DATABASE_PASSWORD")
DATABASE_NAME=os.environ.get("DATABASE_NAME")
