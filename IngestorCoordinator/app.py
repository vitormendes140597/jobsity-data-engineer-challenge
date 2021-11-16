import os, sys
sys.path.append( (os.path.abspath(os.path.join(os.path.dirname(__file__))) + '/notification/'))

from flask import Flask, Response, request
from config import *
from database import create_all_tables, delete_all_tables, load_into_table
from datetime import datetime

import json
import psycopg2

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/setup')
def setup_postgres():
    try:
        conn = psycopg2.connect(f"dbname='postgres' user='{POSTGRES_DB_USER}' host='{POSTGRES_DB_HOST}' password='{POSTGRES_DB_PWD}'")
        create_all_tables(conn)
    except Exception as e:
        return Response(json.dumps({"message": e}, status=200))
    finally:
        if conn:
            conn.close()

    return Response(json.dumps({"message": "Setup was finished successfully"}), status=200)

@app.route('/reset')
def reset():
    try:
        conn = psycopg2.connect(f"dbname='postgres' user='{POSTGRES_DB_USER}' host='{POSTGRES_DB_HOST}' password='{POSTGRES_DB_PWD}'")
        cur = conn.cursor()
        delete_all_tables(conn)
    except Exception as e:
        return Response(json.dumps({"message": e}, status=200))
    finally:
        if conn:
            conn.close()
    
    return Response(json.dumps({"message":"Environment was deleted Succesfully."}), status=200)


@app.route('/ingest')
def ingest():
    path = request.args.get('path', type=str)
    if path is None:
        path = INGESTION_FILE_PATH
    
    try:    
        conn = psycopg2.connect(f"dbname='postgres' user='{POSTGRES_DB_USER}' host='{POSTGRES_DB_HOST}' password='{POSTGRES_DB_PWD}'")
        load_into_table(conn,path)
        print("Finished Loading into Table at " + str(datetime.now()))
    except Exception as e:
        return Response(json.dumps({"message": e}, status=200))
    finally:
        conn.close()
    
    return Response(json.dumps({"message":"Data Ingested successfully"}), status=200)


if __name__ == "__main__":
    app.run('0.0.0.0')