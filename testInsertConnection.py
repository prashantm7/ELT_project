import mysql.connector
from mysql.connector import Error
from datetime import date, time, datetime


print("trying to insert a record to database contacts table")
'''
INSERT INTO contacts (owner , firstName, lastName, modifiedBy ,country)
VALUES ('Nitisha','Cardinal2', 'Stavanger2', 'nitisha70701' ,'IN');

'''

insertQuery = "INSERT INTO contacts (owner , firstName, lastName, modifiedBy ,country) VALUES ('{}','{}','{}','{}','IN')"




try:
    connection = mysql.connector.connect(host='localhost',
                                         database='export_genius_test',
                                         user='root',
                                         password='')
    print('\n\n--connection successful--\n\n')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        myInsertQuery = insertQuery.format('aasda','s2s','d2sadw','qweqwdasdw')
        print("insert statement : ",myInsertQuery)
        cursor = connection.cursor()
        insertResult = cursor.execute(myInsertQuery)
        print("result : ",insertResult)
        # commit the changes
        connection.commit()
        print('done')

except Error as e:
    print("\n\nError while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")