from os import environ
from sqlalchemy import create_engine
import psycopg2

dbhost = environ.get('DBHOST')
dbname = environ.get('DBNAME')
dbuser = environ.get('DBUSER')
dbpass = environ.get('DBPASS')

engine = create_engine(f'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}')


def executeQuery(query, params=(None,)):
    try:

        conn = psycopg2.connect(
            host=dbhost,
            database=dbname,
            user=dbuser,
            password=dbpass)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, params)
        result = cur.fetchall()

        result_dict = []
        for row in result:
            result_dict.append(dict(row))

        return {
            'status': True,
            'data': result_dict,
        }
    except Exception as err:
        return {
            'status': False,
            'error': err,
        }

    # try:
    #     connection = engine.connect()
    #     results = connection.execute(query, params).fetchall()
    #     return {
    #         'status': True,
    #         'data': results,
    #     }
    # except Exception as err:
    #     return {
    #         'status': False,
    #         'error': err,
    #     }
