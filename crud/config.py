# from os.path import join, dirname
# from dotenv import load_dotenv
# dotenv_path = join(dirname(__file__), '.env')  # Path to .env file
# load_dotenv(dotenv_path)

from os import environ 

DEBUG = environ.get('DEBUG')
ENV = environ.get('ENV')
SECRET_KEY = environ.get('SECRET_KEY')
