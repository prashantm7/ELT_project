
# for test connection to database


from datetime import date, datetime ,timedelta
import sys
from time import sleep
from time import ctime

import logging
from requests import request
import mysql.connector
from mysql.connector import Error
import json
import re

# imports



userMap = {

    'nitisha70701':  {
                "name": "Nitisha Chawla",
                "id": "348201000000231177",
                "email": "nitisha@exportgenius.in"
            }
            
}

def userOnwerMapFunction(username):
#    print('adding owners for user  : ',username)
    if username=='nitisha70701' or username=='Nitisha70701':
#        print('returned owner key item for nitisha')
        return userMap['nitisha70701']
    else:
        return None
    

# logging

now = datetime.now()
fileName = now.strftime('TEST_CONNECTION_%Y_%m_%d_%H_%M_%S')
logging.basicConfig(filename="logs\\testConnection"+fileName+"_LOGS.log", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

'''

        operations start from here -  first oauth then read data - while time passses check if condition to refresh token is acheived
'''
logging.info("-- operations started at {}  --".format(ctime()))

# client connection establishment and querying leads
queryLeads = "select * FROM leads"
# will output 100 leads to json then try api call from postman

leadsCounter = 0



# using offset
print('creating shards of huge amount of data\n')

sizeOfShard = 100
index = 0
counter = 0
lastIndex = 500
alpha = re.compile(r"[a-z|A-Z]|[!@#$%^&*/]")


leads = 'select * from leads'
#clients = 'select * from clients'
#conversation = 'select * from conversation'
#invoiceInfo = 'select * from invoice_info'
#invoiceItems = 'select * from invoice_items'


for i in range(index , lastIndex ,sizeOfShard):
    print('\n\n ------------- {} -------------- '.format(counter))

    # print('{} -> running for limit {},{}'.format(counter,i,sizeOfShard))
    # last name for leads cannot be more than 80 so just use local id
    print('{} ->  limit {} OFFSET {}'.format(counter,sizeOfShard , i))
    offSet = ' LIMIT {} OFFSET {} '.format(sizeOfShard,i)
    
    with mysql.connector.connect(host='',database='',user='',password='') as connectPointer:
        print('connected at ',ctime())
        with connectPointer.cursor() as aCursor:
            leadsQuery = leads+offSet
            print(' > query : ',leadsQuery)
#            print('running - ',query)
            aCursor.execute(leadsQuery)
            result = aCursor.fetchall()
            if not result:
                print('--> no leads fetched <--')
                logging.info('__________  no leads fetched  __________')
            else:            
                leadsFile = 'leads/leads_data_{}.json'.format(i)
                print(f' . .. writing to {leadsFile}')
                leadsCollList = []
                for rows in result:
                    leadsCollection = {}
                    leadsColl = {}
                    local_id = rows[0]
                    name = str(local_id)
                    client_id = rows[1]
                    lead_source = rows[2]
                    importance = rows[3]
                    added_on = str(rows[4])
                    user_id = rows[5]
                    requirement = rows[6]
                    report_type = rows[7]
                    time_from = rows[8] # check for null
                    time_to = rows[9] # check for null
                    open_price = rows[10]
                    close_price = rows[11]
                    status = rows[12]
                    causes = rows[13]
                    invoice_id = rows[-2]
                    temp = rows[-1]
                    
                    leadsColl['Name'] = name + ' - Lead'
                    leadsColl['local_id'] = local_id
                    leadsColl['client_id'] = client_id
                    leadsColl['Lead_Source'] = lead_source
                    leadsColl['source'] = lead_source

                    leadsColl['importance'] = importance
                    leadsColl['added_on'] = added_on.replace(' ','T') + '+05:30'
                    leadsColl['Created_Time'] = added_on.replace(' ','T') + '+05:30'
                    leadsColl['requirement'] = requirement
                    leadsColl['status'] = status
                    leadsColl['invoice_id'] = invoice_id
                    leadsColl['Last_Name'] = "(lead)" +  ' - ' +str(local_id)
                    leadsColl['user_id'] = user_id
                    
                    if time_from == None:
                        leadsColl['time_from'] = None
                    else:
                        leadsColl['time_from'] = str(time_from)
                    if time_to == None:
                        leadsColl['time_to'] = None
                    else:
                        leadsColl['time_to'] = str(time_from)      
                                       
                    leadsColl['opening_price'] = open_price
                    leadsColl['closing_price'] = close_price                    
                    leadsColl['report_type'] = report_type
                    leadsColl['temp'] = temp 
                    # owner assignment to leads                    
                    leadsColl['Owner'] = userOnwerMapFunction(user_id)
                    leadsCollList.append(leadsColl)
                print("{} leads payload created at {}".format(len(leadsCollList),ctime()))
                logging.info("{} leads payload created at {}".format(len(leadsCollList),ctime()))
                fileName = leadsFile

                with open(fileName,'w',encoding='utf-8') as leadJson:
                    leadJson.write(json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
            
                logging.info('________________ check file {}____________________________'.format(fileName))

    counter+=1

