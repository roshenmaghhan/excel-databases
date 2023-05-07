import pandas as pd
import numpy as np
from peewee import *
import os
from dotenv import load_dotenv

load_dotenv()

class RemoteDB() :
    database_choice = ''
    table_name = ''
    table_json = ''
    file = ''

    model = None
    df = None

    '''
    Constructor
    '''
    def __init__(self, table_name="", file="") :
        self.init_db_conn()
        self.table_name = table_name
        self.file = file 
        self.table_json = self.create_table_dict()
        
        if self.table_name not in self.database_choice.get_tables() : 
            self.model = self.table_operation(operation="CREATE_TABLE")
        else : 
            self.model = self.table_operation(operation="GET_TABLE")
    
    @classmethod
    def is_table_exists(self, table_name='') :
        self.init_db_conn(self)
        return table_name in self.database_choice.get_tables()

    '''
    Initialize database connection
    '''
    def init_db_conn(self) :
        self.database_choice = PostgresqlDatabase(os.environ["POSTGRES_DB"], 
                                                  user=os.environ["POSTGRES_USER"], 
                                                  password=os.environ["POSTGRES_PASSWORD"],
                                                  host=os.environ["POSTGRES_HOST"], 
                                                  port=5432)
        self.database_choice.connect()


    '''
    Creates the table's dictionary
    '''
    def create_table_dict(self) : 
        res = {}
        res['table_name'] = self.table_name
        res['columns'] = []
        self.df = self.get_df_by_type(self.file) #DONE: Read excels, parquet and csv

        for c in self.df.columns : 
            obj = {}
            obj['field_name'] = c
            obj['field_type'] = str(self.df[c].dtype)
            res["columns"].append(obj)

        self.table_json = res
        return res
    
    '''
    Performs either a build, or retrieval, of table object

    Operations : 
    1. CREATE_TABLE -> Creates the table
    2. GET_TABLE -> Returns the table object
    '''
    def table_operation(self, operation="CREATE_TABLE") : 
        attrs = {'__tablename__': self.table_name}
        for column in self.table_json['columns']:
            attrs[column['field_name']] = self.get_field_type( column['field_type'] )
        dynamic_model = type(self.table_name, (Model,), attrs)
        dynamic_model.bind(self.database_choice)

        if operation == "CREATE_TABLE" : 
            dynamic_model.create_table()

        return dynamic_model

    '''
    Gets the field type
    '''
    def get_field_type(self, f_type) : 
        if "int" in f_type : 
            return IntegerField(null=True)
        elif "float" in f_type : 
            return DoubleField(null=True) #TODO: Check if it preserves the float values
        
        return TextField(null=True)

    '''
    Populates the table based on data file
    '''
    def populate_table(self) :
        try : 
            df = self.df.copy() # Make a copy

            for c in df.columns : 
                if df[c].dtype == "object" :
                    df[c] = df[c].astype(str)

            df = df.replace({np.nan: None})

            rows = df.to_dict(orient="records")
            self.model.insert_many(rows).execute()
            return True
        except : 
            return False # If issue encountered, return False
    
    '''
    Deletes the entire content of the table
    '''
    def delete_contents(self) : 
        self.model.delete().execute()

    '''
    Delete the entire table from database
    '''
    def delete_table(self) : 
        self.database_choice.drop_tables((self.model))

    '''
    Returns df depending on file extension
    '''
    def get_df_by_type(self, file) :
        filename, ext = os.path.splitext(file)

        if ext == '.parquet' : 
            return pd.read_parquet(file)
        elif ext == '.csv' : 
            return pd.read_csv(file)
        elif ext == '.xls' or ext == '.xslx' : 
            return pd.read_excel(file)