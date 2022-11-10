from os import environ
from sqlalchemy import create_engine

dbhost = environ.get('DBHOST')
dbname = environ.get('DBNAME')
dbuser = environ.get('DBUSER')
dbpass = environ.get('DBPASS')

engine = create_engine(f'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}')


def executeQuery(query):
    try:
        connection = engine.connect()
        results = connection.execute(query).fetchall()
        return {
            'status': True,
            'data': results,
        }
    except Exception as err:
        return {
            'status': False,
            'error': err,
        }
