import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')\
        or 'postgresql://store_app_user:YY1rD2206FzTU0sVxemLSUO4TDMpbDaR@dpg-cg0kalpmbg589agoauv0-a.oregon-postgres.render.com/store_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_DIR = 'app/static'
    UPLOADS_DIR = 'app/static/uploads'