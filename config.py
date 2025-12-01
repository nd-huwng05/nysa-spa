from datetime import timedelta

DEBUG = False
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = "secret"
SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost:3306/spadb?charset=utf8mb4"


JWT_SECRET_KEY = "jwt_secret"
JWT_TOKEN_LOCATION = ["cookies"]
JWT_COOKIE_CSRF_PROTECT = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/refresh'