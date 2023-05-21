# excel-databases
Spreadsheet and table-based documents are still being used for many purposes, and acts as a database for those who are non-technical or lack the knowledge of SQL. To bridge the gap between technical and non-technical people, excel-databases was created, to turn any local spreadsheet (*.xls*, *.xlsx*, *.parquet* and *.csv*) into a database, with an API.

TLDR; A desktop application to transform local *.xls*, *.xlsx*, *.parquet* and *.csv* files into remote databases, with built-in API connectivity.

## Example Use-cases
- You need to digitalize the data of a CSV file, which is edited frequently on another person's machine.
- Your team in Europe are making adjustments in the data on an excel file, and your team in Asia needs to work with the data concurrently.
- Your parents use excel spreadsheets to track their expenditure, and rather than having multiple copies of the spreadsheet each week in your device, you could use the API to view the changes.


## DEMO
[![final9f7e37d50282a9f9.gif](https://s12.gifyu.com/images/final9f7e37d50282a9f9.gif)](https://gifyu.com/image/Sn10M)

## How It works
Step 1 : Upload a file to the GUI.  
Step 2 : Wait until file is uploaded successfully.  
Step 3 : Done. You can now connect with the file using its API, and every time you save changes locally made on the file, it will reflect on the API.


## Set Up
Step 1 : Clone this repo.<br>
Step 2 : ```cd``` into the repo's directory. (E.g ```cd excel-databases``` ) <br>
Step 3 : Create a virtual environment. (```python3 -m venv .venv ```) <br>
Step 4 : Install all requirements (```pip install -r requirements.txt```) <br>
Step 5 : Create a *.env* file, and populate it with the required values. ( Refer to *.env.example* ).<br>
Step 6 : Run the following command : ```Flask run``` <br>
Step 7 : Run the following command : ```python3 main.py```

## Connecting to API
Once the project is set up, and running, your API should be running on ```http://127.0.0.1:5000```. ( May vary depending on your server ). The API only requires 2 keys, the first, is your ```AUTH TOKEN```. Which would be displayed on the top of the program once executed, and the other is your ```table_id```. This id will be displayed next to the "UNIQUE ID" label, below the file name of the uploaded file.

To retrieve the data of your file, you can simply make a ```GET``` request like the following : <br>
```http://127.0.0.1:5000/?table_id=YOUR_TABLE_ID&token=YOUR_AUTH_TOKEN```