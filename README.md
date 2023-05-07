# excel-databases
A desktop application to transform local *.xls*, *.xlsx*, *.parquet* and *.csv* files into databases, with API connectivity.

## How It works
Step 1 : Upload a file to the GUI.  
Step 2 : Wait until file is uploaded successfully.  
Step 3 : Done. You can now connect with the file using an API, and local changes made on the file will reflect on the API.

## Roadmap
1. **Retrieve unique identifier for each machine.**
- Avoid storing anything locally, store all on a remote database.

2. **Create API for fetching data**
- Create an API to allow data-fetching from the local file.

3. **Monitor local file for changes**
- If local file is deleted, or removed, delete instance from database.
