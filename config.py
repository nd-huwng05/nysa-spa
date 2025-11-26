DEBUG = False
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = "secret"
SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost:3306/spasql?charset=utf8mb4"