from models import LocalDetails, FileList
from peewee import *
import string, random

class TableHandler() :
    
    # DB reference
    _db = ""
    
    # List of tables
    table_list = {
        'local_details' : LocalDetails,
        'file_list' : FileList
    }
    
    # Auth token
    auth_token = ''

    #Set up constructor
    def __init__(self) :
        self._db = SqliteDatabase("local_details.db")
        self.set_up_tables()
        self.set_auth_token()


    # Set up the tables
    def set_up_tables(self) :
        all_tables = self._db.get_tables()
        for t in self.table_list : 
            if t not in all_tables :
                self.table_list[t].create_table()

    # Sets the auth token
    def set_auth_token(self) : 
        temp_token = self.generate_token("AUTH_TOKEN")
        auth_details, created = LocalDetails.get_or_create(attribute="auth_token",defaults={'value': temp_token})
        self.auth_token = auth_details.value

    # Generates the auth token
    def generate_token(self, type) :
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase

        all = lower + upper
        length = 8
        
        if type == "AUTH_TOKEN" : 
            digits = string.digits
            symbols = string.punctuation
            all += digits + symbols
            length = 12

        return "".join(random.sample(all, length))

    # Creates a file entry
    def insert_file_upload(self, f_path) :
        uid = self.generate_token("DB_UNIQUE_ID")
        FileList.create(filepath=f_path, unique_id=uid)
        return uid

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

    # Delete a particular file by id
    def delete_by_id(self, id) :
        FileList.delete().where(unique_id=id)