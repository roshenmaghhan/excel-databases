from models import FileList, FileLogging
from peewee import *
import string, random
import utils.remote_db_handler as rh
import os, time
import pandas as pd
import uuid

class TableHandler() :
    
    # DB reference
    _db = ""
    
    # List of tables
    table_list = {
        'file_list' : FileList,
        'file_logging' : FileLogging,
    }
    
    # Auth token
    auth_token = ''

    #Set up constructor
    def __init__(self) :
        self._db = SqliteDatabase("local_details.db")
        self.set_up_tables()
        self.set_auth_token()

    # Stores timestamp of the file
    @classmethod
    def insert_file_timestamp(self, file_id, file_path) :
        file_time = os.stat(file_path).st_ctime
        FileLogging.create(file_id=file_id, filepath=file_path, file_update_time=file_time)

    # Creates a file entry
    @classmethod
    def insert_file_upload(self, f_path) :
        uid = self.generate_token(self, type="DB_UNIQUE_ID")
        FileList.create(filepath=f_path, unique_id=uid)
        return uid

    # Delete a particular file by id
    @classmethod
    def delete_by_id(self, id) :
        FileList.delete().where(unique_id=id)

    # Set up the tables
    def set_up_tables(self) :
        all_tables = self._db.get_tables()
        for t in self.table_list : 
            if t not in all_tables :
                self.table_list[t].create_table()

    # Sets the auth token
    def set_auth_token(self) : 
        temp_token = self.generate_token("AUTH_TOKEN")
        device_id = self.get_device_id()
        auth_token = rh.RemoteDB.insert_device_token(device_id=device_id, auth_token=temp_token)
        self.auth_token = auth_token

    # Generates the auth token
    def generate_token(self, type) :
        lower = string.ascii_lowercase

        all = lower
        length = 8

        if type == "AUTH_TOKEN" : 
            length = 12
            digits = string.digits
            all += digits

        res_uid = "".join(random.sample(all, length))
        r = rh.RemoteDB.is_table_exists(table_name=res_uid)

        while r : 
            res_uid = "".join(random.sample(all, length))
            r = rh.RemoteDB.is_table_exists(table_name=res_uid)

        return res_uid

    # Get file uploads
    def get_file_uploads(self) :
        res = {}
        q = FileList.select()
        for i in q : 
            res[i.filepath] = i.unique_id
        return res

    # Delete all records of file_list table
    def delete_file_uploads(self) :
        FileList.delete().execute()

    # Gets the Device ID
    def get_device_id(self) : 
        return uuid.UUID(int=uuid.getnode())
