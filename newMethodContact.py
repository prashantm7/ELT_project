
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
import requests


# imports



userMap = {

    'nitisha70701':  {
                "name": "Nitisha Chawla",
                "id": "270924000000263001",
                "email": "nitisha@exportgenius.in"
            },

    'priyanka':{
                "name": "Priyanka Gupta",
                "id": "270924000000298009",
                "email": "priyanka@exportgenius.in"
        },
        
    'hemlata04':{
                "name": "Hemlata Sharma",
                "id": "270924000000298003",
                "email": "hemlata@exportgenius.in"
        },
    'shakim.k':{
                "name": "Shakim Khan",
                "id": "270924000000263003",
                "email": "shakim@exportgenius.in"
        },
    'tarun07':{
                "name": "Tarun Pandey",
                "id": "270924000000298011",
                "email": "tarun@exportgenius.in"
        },
    'haleema_kahaf':{
                "name": "Haleema Kahaf",
                "id": "270924000000298001",
                "email": "haleema@exportgenius.in"
        },
    'krati':{
                "name": "Krati Jain",
                "id": "270924000000298005",
                "email": "krati@exportgenius.in"
        },  
    'priya267':{
                "name": "Priya Chauhan",
                "id": "270924000000298007",
                "email": "priya@exportgenius.in"
        }, 
    'rajat_gupta':{
                "name": "Rajat Gupta",
                "id": "270924000000217001",
                "email": "info@exportgenius.in"
        },

    
            
}
   
# -------------------------------- api calls refresh token and push

accessTokenFile = 'accessToken.json'
def refreshToken():

    url = "https://accounts.zoho.in/oauth/v2/token?"
    print("->refreshing the access tokens")
    logging.info(" -> refreshing tokens at {} ".format(ctime()))

    print("1. without thread ")
    # at every 25 seconds thread runs
    logging.info(" writing refresh token request response at {} ".format(ctime()))
#    timer = threading.Timer(25, refreshToken) # # Call `refreshTokens` in 25 seconds.
#    timer.start()
    print("3. make api calls \n make changes in accessToken.json")
    files=[]
    headers = {}
    print("1. creating payload for refresh request")

    payloadRefresh={
     'client_id': "1000.UCYPYQ50YXV3010I5QA6LXH0TCB3WN",
     'client_secret': "da610c19c559e2af6761d4a8f08b26835ff22916b8",
     'refresh_token':"1000.c54db4c707229db6cebd9dcd02a4b8a4.6fa6717a7bbce2bba6d6c600a6b03b7f",
     'grant_type': 'refresh_token'
     }
    print(payloadRefresh,'\n...\n...\n')
    refreshResponse = requests.request("POST", url, headers=headers, data=payloadRefresh, files=files)
    print("\t 3.1 response to refresh token request : \n")
    print("response : ---- \n\n",refreshResponse,'\n\n')
    print("4. writing response to accessToken.json ")
    logging.info("\n --------------------------------------------------- \n")
    logging.info("\n --------- response to refresh request ---------------- \n{}".format(refreshResponse.text))
    logging.info("\n --------------------------------------------------- \n")

    with open(accessTokenFile,'w') as refresh:
        refresh.write(refreshResponse.text)
    print("-done-")
    print('\\/'*25)
    
''' function to push data '''

'''
sending json.dumps({"data":list_of_records})
'''
def pushInto(moduleName , payload):
    url = "https://www.zohoapis.in/crm/v2/"

    # will return responseGenerated
    # logging.info("|| calling api to insert {} at {} ||".format(moduleName,time.ctime()))
    '''
        add try except here later
    '''
#    print(">make request")
#    print(">write request response to log")
#    print(">reading accessToken.json")
    accessTokenFile = "accessToken.json"
    with open(accessTokenFile,'r') as client:
        tokens = json.load(client)

    accessToken = tokens['access_token']
    url_module = url+moduleName
    print("url used to make api calls ->",url_module)
    headers = {
        'Authorization': 'Bearer '+accessToken,
        'Content-Type': 'application/json',
        }
    response = requests.request("POST", url_module, headers=headers, data=payload)
    # print(response.text)
    # responseText = ''
    # responseText = line+"\n -- reponse recieved at {} -- \n {} ".format(time.ctime(),response.text)+line
    # logging.info(responseText)
    return response




# ------------------------------------------------------------------



# logging

now = datetime.now()
fileName = now.strftime('newMethod_%Y_%m_%d_%H_%M_%S')
logging.basicConfig(filename="logs\\Contacts_7_"+fileName+"LOGS.log", level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')



def userOnwerMapFunction(username):
    print('trying to add Owner for user  : ',username)
    userID = username.lower()
    if userID in userMap:
#        logging.info('mapped owner for user = {}'.format(userID))
        return userMap[userID]
    else:
#        print('\nnone returned')
#        print('-'*50)
        return None
 


'''

        operations start from here -  first oauth then read data - while time passses check if condition to refresh token is acheived
'''

# client connection establishment and querying leads
# will output 100 leads to json then try api call from postman

leadsCounter = 0



# using offset
print('creating shards of huge amount of data\n')

# limit 1 offset n --- one by one each record creation


sizeOfShard = 1

# connection broke at index 55

#index = 56
#index = 934
#index = 1566
index = 1597

counter = 0
lastIndex = 89125  
#97442lastIndex = 97500  #97442

#lastIndex = 500  #97442

alpha = re.compile(r"[a-z|A-Z]|[!@#$%^&*/]")


#leads = 'select * from leads'
contacts = 'select * from contacts'

#clients = 'select * from clients'
#conversation = 'select * from conversation'
#invoiceInfo = 'select * from invoice_info'
#invoiceItems = 'select * from invoice_items'


for i in range(index , lastIndex ,sizeOfShard):
    ''' using index +1 to skip 0 indexed record refreshing '''
    if (i+1)%200==0:
        print('refreshing tokens non threading call at index = {}'.format(i))
        refreshToken()
        logging.info(' _____________- refreshed at {}- ______________'.format(ctime()))
        sleep(5)

    print('\n\n ------------- {} -------------- '.format(counter))
    logging.info('\n\n ------------- cycle {} -------------- '.format(counter))
    # print('{} -> running for limit {},{}'.format(counter,i,sizeOfShard))
    # last name for leads cannot be more than 80 so just use local id
    print('{} ->  limit {} OFFSET {}'.format(counter,sizeOfShard , i))
    offSet = ' LIMIT {} OFFSET {} '.format(sizeOfShard,i)
    res = None
    with mysql.connector.connect(host='localhost',database='db_zoho_crm',user='root',password='mainhoonna') as connectPointer:
        print('connected at ',ctime())
        with connectPointer.cursor() as aCursor:
            leadsQuery = contacts+offSet
            print('\n\n >>> query : ',leadsQuery)
#            print('running - ',query)
            aCursor.execute(leadsQuery)
            result = aCursor.fetchall()
            local_id = None
            zohoID = None
            if not result:
                print('--> no contacts fetched <--')
                logging.info('__________  no contacts fetched  __________')
            else:            
                leadsFile = 'payloads//contacts//contacts_data_{}.json'.format(i)
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
                    
#                print("{} leads payload created at {}".format(len(leadsCollList),ctime()))
#                logging.info("{} leads payload created at {}".format(len(leadsCollList),ctime()))
                fileName = leadsFile
#
                with open(fileName,'w',encoding='utf-8') as leadJson:
                    leadJson.write(json.dumps(
                        {"data":leadsCollList},indent=4,default=str,sort_keys=True
                        ))
#            
                print(">payload created for contact #{}".format(local_id))
                logging.info(f">payload created for contact #{local_id}")                
                payloadPath = fileName
                responsePath = ''
                currPath = ''
                print(' ----------- making api call .. and parsing response for index = {} --------------'.format(i))
                
                print('now payloadPath : {}'.format(payloadPath))
                
                responsePath = 'responses\\contacts\\'+"contacts_response_{}.json".format(i)
                logging.info(f'--> payload #{i} :')
                
                print('making api request')
                logging.info(f'making api request for contact id = {local_id}')
            #    data = None
                currPath = payloadPath
                print('payload path : ',currPath)
                
                with open(currPath,'r') as clientPayload:
                    data = clientPayload.read()
                    
                print(">>paylaod for contacts : ",len(data))
                
                res = pushInto('Contacts',data)
                with open(responsePath,'w') as responseClient:
                    responseClient.write(res.text)
                print("\t---->>> response status code : ",res.status_code)
                if res.status_code==401:
                    print("stopping all operations at local id = {} , index = {}".format(local_id,i))
                    logging.info(f"stopping all operations at local id = {local_id} , index = {index}")
                    sys.exit()
                print('\t -> response in : {}'.format(responsePath))
                logging.info('\t -> response in : {}'.format(responsePath))
                
                if "SUCCESS" in res.text:
                    print('-'*20)
                    if res.status_code==200 or res.status_code == 201 or res.status_code==202:
#                        print('>adding zohoID to contacts column running update query<')
                        jsonRes = res.json()
                        zohoID = jsonRes['data'][0]['details']['id']
                        updateQuery = "Update contacts set zohoID = '{}' where id = {}".format(zohoID , local_id)
                        print("updating local record with its zoho record id \n\nupdate query :  -> ",updateQuery)
                        aCursor.execute(updateQuery)
                        connectPointer.commit()
                        logging.info(f'---- updated record #{local_id} with zohoID = {zohoID} ----')
                    print('-'*20)
                else:
                    print("..not inserted in crm..")
                    logging.info(f'---- record wth id = {local_id} not inserted in crm ----')
                    
    counter+=1
    print('------------------------------------------|wait for 1 second for refresh timeout|------------------------------------------')
    sleep(1)


print('contacts payload creation done\ntotal payloads created : ',counter)
logging.info('total contacts payloads created : {} operations closed at  {}'.format(counter,ctime()))
