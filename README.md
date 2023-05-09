# excel-databases
A desktop application to transform local *.xls*, *.xlsx*, *.parquet* and *.csv* files into remote databases, with built-in API connectivity.

## How It works
Step 1 : Upload a file to the GUI.  
Step 2 : Wait until file is uploaded successfully.  
Step 3 : Done. You can now connect with the file using an API, and local changes made on the file will reflect on the API.

## Roadmap
1. **Retrieve unique identifier for each machine.**
- Avoid storing anything locally, store all on a remote database.

2. **Create API for fetching data**
- In remote db, add local token and tables into auth table.
- Create an API to allow data-fetching from the local file.

3. **Monitor local file for changes**
- ~~Add a local table to monitor for last changes made on a file~~
- If local file is updated, update the table, then update the file's table
    - Update table based on new columns, or new data. (Avoid re-creating table)
- If local file is deleted, or removed, delete instance from database.

4. **General Changes**
- Avoid using global local_database_handler
- Change auth token to be only text and numbers

## Error Handling
- If file can't be read.