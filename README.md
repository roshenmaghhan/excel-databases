# excel-databases
A desktop application to transform local *.xls*, *.xlsx*, *.parquet* and *.csv* files into remote databases, with built-in API connectivity.

## How It works
Step 1 : Upload a file to the GUI.  
Step 2 : Wait until file is uploaded successfully.  
Step 3 : Done. You can now connect with the file using an API, and local changes made on the file will reflect on the API.

## Roadmap
- Add file versioning to check if : 
    - Columns are changed ( Name )
    - New columns are added
    - New row is inserted
    - Columns were deleted
    - Row is removed
    - Row is altered

## Error Handling
- If file can't be read.