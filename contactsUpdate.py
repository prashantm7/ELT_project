import mysql.connector
from mysql.connector import Error
from datetime import date, time, datetime


print("trying to insert a record to database contacts table")
'''
INSERT INTO contacts (owner , firstName, lastName, modifiedBy ,country)
VALUES ('Nitisha','Cardinal2', 'Stavanger2', 'nitisha70701' ,'IN');

'''

# insertQuery = "INSERT INTO contacts (owner , firstName, lastName, modifiedBy ,country) VALUES ('{}','{}','{}','{}','IN')"

# 
# Update single record now
sql_update_query = """Update contacts set firstName = 'ChangedNow' where id = 5"""
# cursor.execute(sql_update_query)
# connection.commit()
# print("Record Updated successfully ")


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='put_DB_name',
                                         user='root', 
                                         password='')
    print('\n\n--connection successful--\n\n')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        print("update statement : ",sql_update_query)
        cursor = connection.cursor()
        updateResult = cursor.execute(sql_update_query)
        print("result : ",updateResult)
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