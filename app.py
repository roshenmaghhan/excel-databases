from flask import Flask
from flask import request
import os
from peewee import *
import psycopg2
from utils.remote_db_handler import RemoteDB as rh
from flask import json
from models import Auth

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
db = PostgresqlDatabase(os.environ["POSTGRES_DB"], 
                    user=os.environ["POSTGRES_USER"], 
                    password=os.environ["POSTGRES_PASSWORD"],
                    host=os.environ["POSTGRES_HOST"], 
                    port=os.environ["POSTGRES_PORT"])

'''
Main endpoint API
'''

@app.route("/")
def main() : 
    table_id = request.args.get('table_id')
    auth_token = request.args.get('token')

    # Checks if required parameters exists
    if (not table_id) or (not auth_token): 
        response = {400 : "table_id and token parameters are needed."}
        return app.response_class(response=json.dumps(response), status=400, mimetype='application/json')

    # Check if table exists
    if table_id not in db.get_tables() : 
        response = {404 : "table_id does not exist."}
        return app.response_class(response=json.dumps(response), status=404, mimetype='application/json')

    # Check if table and auth token match : Err 404
    is_exists = Auth.select().where(Auth.table_id==table_id, Auth.auth_token==auth_token)
    if len(is_exists) == 0 : 
        response = {401 : "Unauthorized. table_id and token doesn't match."}
        return app.response_class(response=json.dumps(response), status=401, mimetype='application/json')

    # Return all rows from the table
    res = db.execute_sql(f'SELECT * FROM {table_id};')
    data = [{column[0]: value for column, value in zip(res.description, row)} for row in res.fetchall()]
    response = app.response_class(response=json.dumps(data), status=200, mimetype='application/json')
    return response