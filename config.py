from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = "secret"

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "nysadb")

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

JWT_SECRET_KEY = "jwt_secret"
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_CSRF_PROTECT = False
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/refresh'
