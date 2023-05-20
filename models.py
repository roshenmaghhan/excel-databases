import sqlite3
import os
from peewee import *
from dotenv import load_dotenv

load_dotenv()

'''
Uploaded file details (Local Table)
'''
class FileList(Model) :
    filepath = TextField()
    unique_id = TextField()
    class Meta :
        database = SqliteDatabase("local_details.db")
        db_table = 'file_list'

'''
Stores timestamps of saved files (Local Table)
'''
class FileLogging(Model) :
    file_id = TextField()
    filepath = TextField()
    file_update_time = TextField()
    class Meta : 
        database = SqliteDatabase("local_details.db")
        db_table = 'file_logging'

'''
Creates Auth table (Remote Table)
'''
class Auth(Model) : 
    table_id = TextField()
    auth_token = TextField()
    class Meta : 
        database = PostgresqlDatabase(os.environ["POSTGRES_DB"], 
                    user=os.environ["POSTGRES_USER"], 
                    password=os.environ["POSTGRES_PASSWORD"],
                    host=os.environ["POSTGRES_HOST"], 
                    port=os.environ["POSTGRES_PORT"])
        db_table = 'auth_table'

'''
Creates an entry of unique devices, as well as their tokens
'''
class DeviceID(Model) : 
    device_id = TextField()
    auth_token = TextField()
    class Meta : 
        database = PostgresqlDatabase(os.environ["POSTGRES_DB"], 
                    user=os.environ["POSTGRES_USER"], 
                    password=os.environ["POSTGRES_PASSWORD"],
                    host=os.environ["POSTGRES_HOST"], 
                    port=os.environ["POSTGRES_PORT"])
        db_table = 'device_id'