import os

class Config:
    # -------------------- FLASK CONFIG --------------------
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_master.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------- JWT CONFIG --------------------
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') 
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 1 day

    # -------------------- CELERY CONFIG --------------------
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    
    # -------------------- MAIL CONFIG --------------------
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # your email
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # app password

    # -------------------- CACHING CONFIG --------------------
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CELERY_TIMEZONE = 'Asia/Kolkata'