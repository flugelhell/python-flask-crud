from os import environ
from sqlalchemy import create_engine
# import psycopg2

dbhost = environ.get('DBHOST')
dbname = environ.get('DBNAME')
dbuser = environ.get('DBUSER')
dbpass = environ.get('DBPASS')

engine = create_engine(f'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}')


def executeQuery(query, params):
    # try:

    #     conn = psycopg2.connect(
    #         host=dbhost,
    #         database=dbname,
    #         user=dbuser,
    #         password=dbpass)
    #     cur = conn.cursor()
    #     cur.execute(query, params)
    #     result = cur.fetchall()
    #     return {
    #         'status': True,
    #         'data': result,
    #     }
    # except Exception as err:
    #     return {
    #         'status': False,
    #         'error': err,
    #     }

    try:
        connection = engine.connect()
        results = connection.execute(query, params).fetchall()
        return {
            'status': True,
            'data': results,
        }
    except Exception as err:
        return {
            'status': False,
            'error': err,
        }
