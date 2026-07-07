from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

class Config:
    DEBUG = os.getenv('APP_ENV') == 'development'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)