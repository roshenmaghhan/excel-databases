import sqlite3
from peewee import *

'''
Local details for the table
'''
class LocalDetails(Model) :
    attribute = TextField()
    value = TextField()
    class Meta : 
        database = SqliteDatabase("local_details.db")
        db_table = 'local_details'

'''
Uploaded file details
'''
class FileList(Model) :
    filepath = TextField()
    unique_id = TextField()
    class Meta :
        database = SqliteDatabase("local_details.db")
        db_table = 'file_list'

