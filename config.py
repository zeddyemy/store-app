import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'postgresql://postgres:zeddy@localhost:5432/shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_DIR = 'app/static'
    UPLOADS_DIR = 'app/static/uploads'