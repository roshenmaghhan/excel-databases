import sqlite3
import os
from peewee import *
from dotenv import load_dotenv

load_dotenv()

'''
Local details for the table (Local Table)
'''
class LocalDetails(Model) :
    attribute = TextField()
    value = TextField()
    class Meta : 
        database = SqliteDatabase("local_details.db")
        db_table = 'local_details'

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