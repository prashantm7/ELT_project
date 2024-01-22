1. PROJECT TITLE
    ELT Process: SQL Database to JSON File to Zoho CRM

2. Extract Data from SQL Database
    Establish a connection to your SQL database using the appropriate library or tool.
    Execute SQL queries to retrieve payroll data from the database.
    Fetch and format the data as required

3. Transform Data to JSON
    Transform the extracted data into JSON format. This can be achieved using programming languages like Python, utilizing the json library.

4. Store JSON Data in a Folder
    Utilize file I/O operations using python programming language to save the JSON data as a file in a specific folder on local or network drive

5. Push Data to Zoho CRM
    Set up a Zoho CRM account and generate API keys.
    Develop an HTTP request to send the JSON data to Zoho CRM using a programming language with HTTP request capabilities, such as Python with the requests library.
    Authenticate the API request using the generated API keys.

6. Handle Responses and Errors
    Implement error handling to address potential issues when interacting with Zoho CRM, such as authentication errors, network issues, or data format errors.
    Process the response from Zoho CRM to ensure that the data was successfully pushed.

7. Usage
    To implement this ELT process, follow these steps:

    Retrieve and transform payroll data from your SQL database.
    Save the transformed data as a JSON file in a designated local folder.
    Set up the integration with Zoho CRM using API keys and the appropriate API endpoint.
    Execute the push process to send the JSON data to Zoho CRM.

8.  Dependencies
    SQL Database Access (e.g., Microsoft SQL Server, MySQL)
    Programming Language (e.g., Python)
    Libraries (e.g., pyodbc for database access, json for JSON formatting, requests for API requests)
    Zoho CRM Account and API Keys

Contributing
If you have improvements or suggestions for this ELT process, feel free to contribute by creating issues or pull requests in this repository.




Files and utility :
Generating Payload
syncScript_v2.py -  File is extracting and load the data i.e. payroll of relative data is converted into JSON files.
token.txt  - API file conatain the key

Pushing data into ZOHO crm
contactsUpdate.py  - Contacts data push into Zoho crm
Module/leadsWithOnwers.py  - Push Leads data into Zoho crm

Pushing data into relative owner ID of Zoho portal
custom-get-leads.ipynb

More files.....
