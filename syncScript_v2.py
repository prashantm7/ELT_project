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
from authentication import generateAccessTokens
from authentication import refreshTokens

from apiCall import pushInto
#
# pushInto(moduleName , payload):
# from apiCall import pushInto
#
global contactsCounter, convCounter , leadsCounter ,invoiceInfoCounter , dealsCounter
#global aDate , secondDate , counter

''' example date : 2015 07 08 '''


'''logging'''
# now = datetime.now()
now = datetime(2015,7,8,9,00)
print('testting for ',now)

fileName = now.strftime('%Y_%m_%d_%H_%M_%S')
logging.basicConfig(filename="logs\\version_3_syncScript_"+fileName+"_LOGS.log", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

'''

        operations start from here -  first oauth then read data - while time passses check if condition to refresh token is acheived
'''
logging.info("-- operations started at {}  --".format(ctime()))
#oauthResponse = generateAccessTokens()
logging.info('example without ouath with today date \n\n')
#logging.info(f"\n\n-- response recieved : \n {oauthResponse.text} \n\n -- at {ctime()}  --")

# print('\n\n\n\exiting now from test')
# sys.exit()

# /* testing with 2015 07 03*/
# /* testing with 2014 08 12*/


'''
    queries
'''
# queryClients = "select id,company_name,company_grade,phone_no,email,user_id,added_on FROM clients"
queryContacts = 'select * from contacts'

# queryConversation = "select s_n,with_email,user_id,added_on,msg,followup_on FROM conversation"
queryConversation = 'select * from conversation'

queryLeads = "select * FROM leads"
queryInvoiceInfo = "select * FROM invoice_info"
queryDeals = "select * FROM deals"

# info has Id not id but it is item[index=0]
alpha = re.compile(r"[a-z|A-Z]|[!@#$%^&*/]")
counter = 0
# after every 30 minutes i.e. counter%3==0 run refreshToken.py to refresh the accessToken
convCounter = 0
leadsCounter = 0
invoiceInfoCounter = 0
contactsCounter = 0
dealsCounter = 0

# -------------------------------------------------------------------------------------------------------------------------

''' date variables '''

#/* testing with 2015-07-04*/
# assuming scritp starts running on 2015 07 03 10 AM -  it will till 8pm 

# today = datetime.today()

aDate = datetime(2015,7,8,10,00)
# aDate = today 
#terminate  = datetime(2015,7,8,10,00)
terminate = aDate + timedelta(minutes = 600)


print('script will stop running at {}'.format(terminate.strftime('%Y-%m-%d %H:%M:%S')))
logging.info(' after 10 hours script will stop running at {}'.format(terminate.strftime('%Y-%m-%d %H:%M:%S')))
secondDate = aDate


#
# -------------------------------------------------------------------------------------------------------------------------
def userOnwerMapFunction(userName):
    if userName:
        print('-username associated-')
        return userName
    else:
        print('no username associated')
        return None

def updateTime():
    ''' timer '''
    global aDate , secondDate , counter

    counter+=1
    # d1 = aDate.strftime('%Y-%m-%d %H:%M:%S')
    # d2 = secondDate.strftime('%Y-%m-%d %H:%M:%S')
    # print("before update aDate = {} , secondDate = {}".format(d1,d2))
#    print('\n not waiting for 10 seconds\n')
#    time.sleep(60) # 60 seconds now -  for 10 minutes replace 60 with 60*10
#    await for 5 seconds - test
# - - - 600 seconds wait -- 10 minutes wait
# ------ original ---------
#    for i in range(600):
#        print('remaining seconds :  {}'.format(600-i))
#        sleep(1)
    for i in range(10):
        print('remaining seconds :  {}'.format(10-i))
        sleep(1)


    diff = secondDate + timedelta(minutes=10) 
    aDate = secondDate
    secondDate = diff
    print("now after update : aDate = {} , secondDate = {}".format( aDate.strftime('%Y-%m-%d %H:%M:%S') , secondDate.strftime('%Y-%m-%d %H:%M:%S')))
    return aDate , secondDate

''' refresh token every 40 minutes '''

'''
        script runs from 10:00 hrs to 20:00 hrs
        10 am to 8pm
'''
while aDate < terminate:
    # counter is incremented in updateTime function
    print('--in the loop--')
    print('waiting for 10 minutes ( seconds for example ) ')
    logging.info('--------------------- 10 minute wait ----------------------------')
#    time.sleep(2) # 2 seconds now
#     waiting for 1minute -------- test -------------
    timestamp1 , timestamp2 = updateTime()
    timeCond = " WHERE added_on between '{}' and '{}'".format(timestamp1, timestamp2)
    '''
        wait complete timestamps updated now check for refresh
    '''
    if counter%4==0:
        print("minutes passed = ",10*counter,'(counter = ',counter,')')
        logging.info('minutes passed = {} , counter = {} '.format(10*counter , counter))
        
        logging.info(" - - - - refreshing tokens at {} - - - - - ".format(ctime()))
        refreshResponse = refreshTokens()
        logging.info("-- response recieved : \n {}\n\n -- at {}  --".format(refreshResponse,ctime()))
    logging.info(' -> ___________ cycle {} started ______________ <- '.format(counter))

    print('condition no {} : {} '.format(counter,timeCond))
    logging.info('-> ->condition no {} : {} '.format(counter,timeCond))
    # everytime a new query is generated connect to db and perform operations
    # since keeping a connection alive is not good enough
    # not possible to keep alive the mysql connection
    with mysql.connector.connect() as connectPointer:
        print('-> connection established at timestamp = {}',timestamp2)
        logging.info(' --connection established at \'{}\' timestamp  : {} --'.format(ctime(),timestamp2))
        # clients
        with connectPointer.cursor() as aCursor:
            contactQuery = queryContacts+timeCond
            print('1. fetching contacts : ',contactQuery)
            logging.info('1. fetching contacts {}'.format(contactQuery))
            aCursor.execute(contactQuery)
            result = aCursor.fetchall()
            if not result:
                print('--> no contacts created in the last 10 minutes <--')
                logging.info('__________  no contacts created in the last 10 minutes  __________')

            else:
                clientCounter+=1
                leadsFile = 'contactsTEST/contacts_data_{}.json'.format(i)
                print(f' . .. writing to {leadsFile}')
                leadsCollList = []
                for rows in result:
                    leadsColl = {}
                    local_id = rows[0]
                    salutation = rows[2]
                    FirstName = rows[3]
                    LastName = rows[4]
                    AccountName = rows[5]
                    Csource = rows[6]
                    Lsource = rows[7]
                    Title = rows[8]
                    department = rows[9]
                    dob = rows[10]
                    user_id = rows[-15]
                    Owner = userOnwerMapFunction(user_id)
                    phone = rows[-13]
                    mobile = rows[-12]
                    HomePhone = rows[-11]
                    OtherPhone = rows[-10]
                    fax = rows[-9]
                    email = rows[-8]
                    sEmail = rows[-7]
                    if sEmail:
                        print('this record has secondary email ... : ',sEmail)
                    Address = rows[-6]
                    city = rows[-5]
                    state = rows[-4]
                    zip = rows[-3]
                    country = rows[-2]
                    
                    # since first name is not garaunteed to be present adding local id number as a safe flag
                    
                    leadsColl['Name'] = str(local_id) + ' - ' + FirstName
                    leadsColl['local_id'] = local_id
                    leadsColl['Email'] = email
                    leadsColl['Secondary_Email'] = sEmail
                    leadsColl['Phone'] = phone
                    leadsColl['Mobile'] = mobile
                    leadsColl['Other_Phone'] = OtherPhone
                    leadsColl['Home_Phone'] = HomePhone
                    leadsColl['Fax']= fax
                    leadsColl['Address'] = Address
                    leadsColl['Country'] = country
                    leadsColl['City'] = city
                    leadsColl['State'] = state
                    leadsColl['Zip'] = zip
                    leadsColl['Campaign'] = Csource
                    leadsColl['Lead_Source'] = Lsource                    
                    leadsColl['Title'] = Title
                    if len(AccountName)>2:
                        leadsColl['Account_Name'] = {
                            'name' : AccountName
                        }
                    else:
                        print("---no account name added to contact---")
                    leadsColl['First_Name'] = FirstName
                    leadsColl['Last_Name'] = LastName
                    leadsColl['Department'] = department
                    # owner assignment to contacts                    
                    leadsColl['Owner'] = Owner
                    leadsCollList.append(leadsColl)
                    
                print("{} leads payload created at {}".format(len(leadsCollList),ctime()))
                logging.info("{} leads payload created at {}".format(len(leadsCollList),ctime()))
                    
                fileName = 'payloadJsons\\contacts\\contact_'+str(contactsCounter)+'_temp.json'
                # payloadJsons\\clients_1_temp.json - read this payload to push
                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
                
                logging.info("\n\n{} clients crated \n\n".format(len(leadsCollList)))
                responseClient = pushInto('Contacts',json.dumps(
                    {"data":leadsCollList},indent=4,default=str,sort_keys=True
                    ))
                print('response to  clients api call : \n\n ',responseClient.text)
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(ctime(),responseClient.text)
                logging.info(responseText)
                fileNameR = 'syncResponse\\contacts\\contact_response_'+str(contactsCounter)+'_temp.json'
                # payloadJsons\\clients_1_temp.json - read this payload to push
                with open(fileNameR,'w',encoding='utf-8') as clientJson:
                    clientJson.write(responseClient.text)
                print('response in : ',fileNameR)
                logging.info(f'\n\n response in : {fileNameR} ')

    print('connection closed now')
    logging.info("------------------ connection closed at {} -----------------------".format(ctime()))
    print('\n\n\n ||| is the connection open : {} |||\n'.format(connectPointer.is_connected()))

    # ----------------------------- conversation ------------------------------------------------------------------
    with mysql.connector.connect() as connectPointer:
        print('-> connection established at timestamp = {}',timestamp2)
        logging.info(' --connection established at \'{}\' timestamp  : {} --'.format(ctime(),timestamp2))
        # conversations
        with connectPointer.cursor() as aCursor:
            print('2. fetching conversations')
            logging.info('2. fetching conversations')
            aCursor.execute(queryConversation+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no conversations created in the last 10 minutes <--')
                logging.info('__________  no conversations created in the last 10 minutes  __________')

            else:
                convCounter+=1
                conv_Collection_List = []
                for rows in result:
                    convCollection = {}
                    name = str(rows[0])
                    s_n = rows[0]
                    with_email = rows[1]
                    user_id = rows[2]
                    added_on = str(rows[3])
                    msg = rows[-1]
                    followup_on = str(rows[4])
                    
                    convCollection['Name'] = name
                    convCollection['added_on'] = added_on.replace(' ','T') + '+05:30'
                    convCollection['s_n'] = s_n
                    convCollection['msg'] = msg
                    convCollection['user_id'] = user_id
                    convCollection['with_email'] = with_email
                    convCollection['followup_on'] = followup_on.replace(' ','T') + '+05:30'
                    convCollection['Owner'] = userOnwerMapFunction(user_id)

                    conv_Collection_List.append(convCollection)
                    
                    del name
                    del s_n
                    del with_email
                    del user_id
                    del added_on
                    del msg
                    del followup_on
                fileName = 'payloadJsons\\conversation\\conversation_'+str(convCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":conv_Collection_List},indent=4,default=str,sort_keys=True
                        ))


                logging.info("\n\n{} conversations inserted \n\n".format(len(conv_Collection_List)))
                print('inserted conversations in ',fileName)
            
                logging.info('____________________________________________')
                logging.info("| caling api to push conversations |")
                responseConversation = pushInto('conversation',json.dumps(
                        {"data":conv_Collection_List},indent=4,default=str,sort_keys=True
                        ))
                # print('-'*50)
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(ctime(),responseConversation.text)
                logging.info(responseText)
                logging.info('____________________________________________')
                
                fileNameR = 'syncResponse\\conversation\\conversation_response_'+str(convCounter)+'_temp.json'
                # payloadJsons\\clients_1_temp.json - read this payload to push
                with open(fileNameR,'w',encoding='utf-8') as clientJson:
                    clientJson.write(responseConversation.text)
                print('response in : ',fileNameR)
                logging.info(f'\n\n response in : {fileNameR} ')

    print('connection closed now')
    logging.info("------------------ connection closed at {} -----------------------".format(ctime()))
    print('\n\n\n ||| is the connection open : {} |||\n'.format(connectPointer.is_connected()))

    # ------------------------------------------------- leads --------------------------------------------------------
    with mysql.connector.connect() as connectPointer:
        print('-> connection established at timestamp = {}',timestamp2)
        logging.info(' --connection established at \'{}\' timestamp  : {} --'.format(ctime(),timestamp2))
        # leads
        with connectPointer.cursor() as aCursor:
            print('3. fetching leads')
            logging.info('3. fetching leads')
            aCursor.execute(queryLeads+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no leads created in the last 10 minutes <--')
                logging.info('__________  no leads created in the last 10 minutes  __________')

            else:
                leadsCounter+=1

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


                   
                print("{} leads created".format(len(leadsCollList)))


                fileName = 'payloadJsons\\leads\\leads'+str(leadsCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
            
                logging.info('____________________________________________')
                logging.info("| caling api to push leads |")
                responseLeads = pushInto('Leads',json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
#                 print('-'*50)
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(ctime(),responseLeads.text)
                logging.info(responseText)
                logging.info('____________________________________________')
#            
#                
                logging.info("\n\n{} leads inserted \n\n".format(len(leadsCollList)))
                print('inserted leads in ',fileName)
                fileNameR = 'syncResponse\\leads\\leads_response_'+str(leadsCounter)+'_temp.json'
                # payloadJsons\\clients_1_temp.json - read this payload to push
                with open(fileNameR,'w',encoding='utf-8') as clientJson:
                    clientJson.write(responseLeads.text)
                print('response in : ',fileNameR)
                logging.info(f'\n\n response in : {fileNameR} ')


    print('connection closed now')
    logging.info("------------------ connection closed at {} -----------------------".format(ctime()))
    print('\n\n\n ||| is the connection open : {} |||\n',connectPointer.is_connected())

    # ------------------------------------------------------ invoice info ------------------------------------------------------------------
    with mysql.connector.connect() as connectPointer:
        print('-> connection established at timestamp = {}',timestamp2)
        logging.info(' --connection established at \'{}\' timestamp  : {} --'.format(ctime(),timestamp2))        
        # invoice info
        with connectPointer.cursor() as aCursor:
            print('4. fetching invoice info')
            logging.info('4. fetching invoice info')

            aCursor.execute(queryInvoiceInfo+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no invoice info created in the last 10 minutes <--')
                logging.info('__________  no invoice info created in the last 10 minutes  __________')
            else:
                invoiceInfoCounter+=1
                # payloads for invoice info ---------------------------------
                # Id,invoice_no,invoice_of,user_id,added_on,Email,payment_in,sale_rule,sale_amount 
                # ----------------------------------------------------------------  
                leadsCollList = []
                for rows in result:
                    local_id = rows[0]
                    invoiceNumber = rows[2]
                    subject = rows[3]
                    customerNo = rows[4]
                    invoiceDate = rows[5]
                    dueDate = rows[6]
                    accountName = rows[7]
                    contactName = rows[8]
                    status = rows[9]
                    createdBy = rows[10] #local_owner
                    bStreet = rows[12]
                    bCity = rows[13]
                    bState = rows[14]
                    bZip = rows[15]
                    bCountry = rows[16]
                    sStreet = rows[17]
                    sCity = rows[18]
                    sState = rows[19]
                    sZip = rows[20]
                    sCountry = rows[21]
                    pName = rows[-7]
                    quant = rows[-6]
                    uPrice = rows[-5]
                    lPrice = rows[-4]
                    total = rows[-3]
                    tAndC = rows[-2]
                    desc = rows[-1]
                    if uPrice:
                        print(f"at local id = {local_id} ---- amount : {uPrice}")
                        if re.match(r'^-?\d+(?:\.\d+)$', uPrice) is None:
                            print("Not a numeric figure for unit price at local id = ",local_id)
                            logging.info(f"Not a numeric figure for unit price at local id = {local_id}")
                            uPrice = None
                        else:
                            print('converted to float...')
                            uPrice = float(uPrice)      
                    if lPrice:
                        print(f"at local id = {local_id} ---- amount : {lPrice}")
                        if re.match(r'^-?\d+(?:\.\d+)$', lPrice) is None:
                            print("Not a numeric figure for list price at local id = ",local_id)
                            logging.info(f"Not a numeric figure for list price at local id = {local_id}")
                            lPrice = None
                        else:
                            print('converted to float...')
                            lPrice = float(lPrice)      
                    
                                      
                    leadsColl = {
                        "Name" : None,
                        "local_id": local_id,
                        "Product_Name": pName,
                        "Shiiping_Street": sStreet,
                        "Shipping_State": sState,
                        "Shipping_City": sCity,
                        "Shipping_Country": sCountry,
                        "Billing_Country": bCountry,
                        "Billing_Street": bStreet,
                        "Billing_Zip": bZip,
                        "Billing_State": bState,
                        "Billing_City": bCity,
                        "user_id": createdBy,
                        "contact_name": contactName,
                        "status": status,
                        "Description": desc,
                        "Terms_Conditions": tAndC,
                        "invoice_date": None,
                        "Due_Date": None,
                        "account_name": accountName,
                        "Quantity": quant,
                        "Invoice_Number": invoiceNumber,
                        "Subject": subject,
                        "Total": None,
                        "List_Price": uPrice,
                        "Unit_Price": lPrice
                    }

                    # for invoice number EG14474 check 11800 json
                    if total:
                        if ' ' in total:
                            total = total.replace(' ','')
                        print(f"\nat local id = {local_id} ---- amount : {total}")
                        if re.match(r'^-?\d+(?:\.\d+)$', total) is None:
                            print("Not a numeric figure for total at local id = ",local_id)
                            logging.info(f"Not a numeric figure for total at local id = {local_id}")
                        else:
                            print('converted to float...')
                            leadsColl['Total'] = float(total)
                    if dueDate:
                        print("\n1. type due date  :  ",type(dueDate),'due date',dueDate)
                        # leadsColl['Due_Date'] = 'T'.join(str(dueDate).split(' '))+"+05:30"
                        newDueDate = str(dueDate)+"T00:00:00+05:30"
                        print(">>>use : ", newDueDate,'\n\n')
                        leadsColl['Due_Date'] = newDueDate

                    else:
                        print(f'no due date assigned to deal with local id = {local_id}')
                        logging.info(f'no due date assigned to deal with local id = {local_id}')

                    if invoiceDate:
                        print("2. type invoiceDate : ",type(invoiceDate),invoiceDate)
                        leadsColl['invoice_date'] = 'T'.join(str(invoiceDate).split(' '))+"+05:30"
                    else:
                        print(f'no invoice date assigned to deal with local id = {local_id}')
                        logging.info(f'no invoice date assigned to deal with local id = {local_id}')

                    # since deal name includes duplicate adding local id 
                    # number as a safe flag
                    
                    if invoiceNumber:
                        print('added record for local id : ',local_id,'with invoice number as name = ',invoiceNumber)
                        leadsColl['Name'] = invoiceNumber
                    else:
                        print('added record for local id : ',local_id)
                        leadsColl['Name'] = str(local_id)

                    # leadsColl['Stage'] = stage
                    # leadsColl['Type'] = type
                    leadsColl['local_id'] = local_id
                    if len(accountName)>2:
                        leadsColl['Account_Name'] = {
                            'name' : accountName
                        }
                    else:
                        print("---no account name added to contact---")
                   
                    Owner = userOnwerMapFunction(createdBy)
                    leadsColl['Owner'] = Owner
                    leadsCollList.append(leadsColl)
                    
                print("{} invoice payload created at {}".format(len(leadsCollList),ctime()))
                logging.info("{} invoice payload created at {}".format(len(leadsCollList),ctime()))
                # --------------------------------------------- 
                fileName = 'payloadJsons\\invoiceInfo\\invoiceInfo'+str(invoiceInfoCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":invoiceInfoCollList},indent=4,default=str,sort_keys=True
                        ))

                logging.info('____________________________________________')
                logging.info("| caling api to push invoice info |")
                responseInvoiceInfo = pushInto('invoice_info',json.dumps(
                        {"data":invoiceInfoCollList},indent=4,default=str,sort_keys=True
                        ))
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(ctime(),responseInvoiceInfo.text)
                logging.info(responseText)
                logging.info('____________________________________________')                

                logging.info("\n\n{} invoice info inserted \n\n".format(len(invoiceInfoCollList)))
                print('inserted invoice info in ',fileName)

                
                fileNameR = 'syncResponse\\invoiceInfo\\invoiceInfo_response_'+str(invoiceInfoCounter)+'_temp.json'
                # payloadJsons\\clients_1_temp.json - read this payload to push
                with open(fileNameR,'w',encoding='utf-8') as clientJson:
                    clientJson.write(responseInvoiceInfo.text)
                print('response in : ',fileNameR)
                logging.info(f'\n\n response in : {fileNameR} ')



    print('connection closed now')
    print('\n\n\n ||| is the connection open : {} |||\n'.format(connectPointer.is_connected()))
    logging.info("------------------ connection closed at {} -----------------------".format(ctime()))
  
    # ------------------------------------------------------ deals ------------------------------------------------------------------
    with mysql.connector.connect() as connectPointer:
        print('-> connection established at timestamp = {}',timestamp2)
        logging.info(' --connection established at \'{}\' timestamp  : {} --'.format(ctime(),timestamp2))        
        # invoice info
        with connectPointer.cursor() as aCursor:
            print('5. fetching deals')
            logging.info('5. fetching deals')

            aCursor.execute(queryDeals+timeCond)
            result = aCursor.fetchall()
            if not result:
                print('--> no deals created in the last 10 minutes <--')
                logging.info('__________  no deals created in the last 10 minutes  __________')
            else:
                dealsCounter+=1
                leadsCollList = []
                for rows in result:
                    leadsColl = {}
                    local_id = rows[0]
                    # local id is S_N
                    local_owner = rows[1]
                    dealName = rows[2]
                    AccountName = rows[3]
                    type = rows[4]
                    lSource = rows[5]
                    cSource = rows[6]
                    local_contact_name = rows[7]
                    amount = rows[8]
                    if amount:
                        print(f"at local id = {local_id} ---- amount : {amount}")
                        if re.match(r'^-?\d+(?:\.\d+)$', amount) is None:
                            print("Not a numeric figure for amount at local id = ",local_id)
                            logging.info(f"Not a numeric figure for amount at local id = {local_id}")
                        else:
                            print('converted to float...')
                            leadsColl['Amount'] = float(amount)
                    closingDate = rows[9]
                    if closingDate:
                        leadsColl['Closing_Date'] = closingDate[:10]
                    else:
                        print(f'no closing date assigned to deal with local id = {local_id}')
                        logging.info(f'no closing date assigned to deal with local id = {local_id}')
                    stage = rows[10]
                    prob = rows[11]
                    expectedRev = rows[12]
                    user_id = rows[13] 
                    desc = rows[-2]

                    # since deal name includes duplicate adding local id 
                    # number as a safe flag
                    

                    leadsColl['Deal_Name'] = dealName + " - " + str(local_id)
                    leadsColl['Stage'] = stage
                    leadsColl['Type'] = type
                    leadsColl['local_id'] = local_id
                    leadsColl['Type'] = type
                    leadsColl['probability_local'] = prob
                    leadsColl['Lead_Source'] = lSource
                    leadsColl['Campaign_Source'] = cSource
                    if len(AccountName)>2:
                        leadsColl['Account_Name'] = {
                            'name' : AccountName
                        }
                    else:
                        print("---no account name added to contact---")
                    leadsColl['Description'] = desc
                    leadsColl['local_contact_name'] = local_contact_name
                    # owner assignment to contacts                    
                    Owner = userOnwerMapFunction(user_id)
                    leadsColl['Owner'] = Owner
                    leadsCollList.append(leadsColl)
                    
                print("{} deals payload created at {}".format(len(leadsCollList),ctime()))
                logging.info("{} deals payload created at {}".format(len(leadsCollList),ctime()))
                print("{} deals created".format(len(leadsCollList)))
                # ----------------------------------------------------------------  

                fileName = 'payloadJsons\\deals\\deal'+str(dealsCounter)+'_temp.json'

                with open(fileName,'w',encoding='utf-8') as clientJson:
                    clientJson.write(json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))

                logging.info('____________________________________________')
                logging.info("| caling api to push invoice items |")
                responseInvoiceInfo = pushInto('Deals',json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
                responseText = ''
                responseText = "\n -- reponse recieved at {} -- \n {} ".format(ctime(),responseInvoiceInfo.text)
                logging.info(responseText)
                logging.info('____________________________________________')                
                logging.info("\n\n{} deals inserted \n\n".format(len(leadsCollList)))
                print('inserted deals in ',fileName)
                
                fileNameR = 'syncResponse\\deals\\deals_response_'+str(dealsCounter)+'_temp.json'
                # payloadJsons\\clients_1_temp.json - read this payload to push
                with open(fileNameR,'w',encoding='utf-8') as clientJson:
                    clientJson.write(responseInvoiceInfo.text)
                print('response in : ',fileNameR)
                logging.info(f'\n\n response in : {fileNameR} ')


    print('connection closed now')
    print('\n\n\n ||| is the connection open : {} |||\n'.format(connectPointer.is_connected()))
    logging.info("------------------ connection closed at {} -----------------------".format(ctime()))

        

print('\ntotal:\n contacts {} ,\n conversations {} ,\n leads {},\n invoice info {},\n deals {}'.format(contactsCounter,convCounter,leadsCounter,invoiceInfoCounter,dealsCounter))
logging.info("-- operations closed at {}  --".format(ctime()))
logging.info('\ntotal:\n contacts {} ,\n conversations {} ,\n leads {},\n invoice info {},\n deals {}'.format(contactsCounter,convCounter,leadsCounter,invoiceInfoCounter,dealsCounter))
