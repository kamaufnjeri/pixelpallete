import os

"""path to save database"""
basedir = os.path.abspath(os.path.dirname(__file__))


"""class for app configurations"""
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "I'm_just_guessing"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
