import pytest
import json
import requests
import random


fileSca_json=open("SCA.json")
global sca
sca=json.load(fileSca_json)

fileAuth_json = open("auth.json")
global auth
auth=json.load(fileAuth_json)

fileBanks_json = open("banks.json")
global banks
banks=json.load(fileBanks_json)

global adapterName
global error401
error401=401
global check200
check200=200
global check500
check500=500
global check201
check201=201
accessToken=""
banksIds=[]
bankId=""
mode=0
accountIdBank=0
accountIdCard=0
fileEnviroment_json=open("enviroments.json")
base_urls=json.load(fileEnviroment_json)
custom_error_message="Gateway Timeout"
fileUsers_json=open("users.json")
users=json.load(fileUsers_json)

userId=0
"""
Il seguete test permette ad un utente NORMALE di criptare una password
non essendo autorizzato dovrebbe dare errore 401
"""  
#---------------TF_Auth_1---------------#
@pytest.mark.timeout(6)
def test_auth_passwordEncrypt_normal_user(ambiente):
    payload = json.dumps(auth["passwordEncrypt"]["payload"])
    headers1=auth["passwordEncrypt"]["headers"]
    responseT = requests.request("POST",base_urls[ambiente]["baseUrl"]+auth["passwordEncrypt"]["endpoint"] , headers=headers1, data=payload)            
    assert responseT.status_code == error401
   
    
"""
Il seguete test permette ad un utente di accedere ad un account 
"""  
#---------------TF_Auth_1---------------#
@pytest.mark.timeout(5)
def test_auth_register_normal_user(ambiente):
    payload = auth["register"]["payload"]
    headers1=auth["register"]["headers"]
    responseT = requests.request("POST",base_urls[ambiente]["baseUrl"]+auth["register"]["endpoint"],headers=headers1, data=payload)
    assert responseT.status_code == error401
    

"""
Il seguete test simula un utente NORMALE mentre:
1. esegue il login
2. chiede il refresh del token
3. chiede il logout
"""  
#---------------TF_Auth_3---------------#
@pytest.mark.test
def test_auth_and_invalidate(ambiente):
    #Viene fatto il login
    payloadLogin = json.dumps(base_urls[ambiente]["keys"]) 
    headersLogin=auth["login"]["headers"]
    responseLogin = requests.request("POST",base_urls[ambiente]["baseUrl"]+auth["login"]["endpoint"], headers=headersLogin, data=payloadLogin)
    #Viene fatto l'invalidate
    payloadInvalidate=json.dumps(auth["invalidate"]["payload"])
    auth["invalidate"]["headers"]["Authorization"]=auth["invalidate"]["headers"]["Authorization"]+responseLogin.json()["accessToken"]
    headersInvalidate=auth["invalidate"]["headers"]
    responseInvalidate = requests.request("POST",base_urls[ambiente]["baseUrl"]+auth["invalidate"]["endpoint"], headers=headersInvalidate, data=payloadInvalidate)
    assert responseInvalidate.status_code == check200
    assert type(responseInvalidate.json()["invalidatedForClient"]) is int and responseInvalidate.json()["invalidatedForClient"]>=0

#---------------TF_Auth_2---------------#

@pytest.mark.test
def test_auth_login_and_refresh_normal_user(ambiente):
    #Viene fatto il login
    payloadLogin = json.dumps(base_urls[ambiente]["keys"]) 
    headersLogin=auth["login"]["headers"]
    responseLogin = requests.request("POST",base_urls[ambiente]["baseUrl"]+auth["login"]["endpoint"], headers=headersLogin, data=payloadLogin)
    
    auth["refresh"]["payload"]["token"]=responseLogin.json()["refreshToken"]
    #Viene fatto il refresh
    payloadRefresh=json.dumps(auth["refresh"]["payload"])
    auth["refresh"]["headers"]["Authorization"]=auth["refresh"]["headers"]["Authorization"]+responseLogin.json()["accessToken"]
    headersRefresh=auth["refresh"]["headers"]
    responseRefresh = requests.request("POST",base_urls[ambiente]["baseUrl"]+auth["refresh"]["endpoint"], headers=headersRefresh, data=payloadRefresh)
    global accessToken
    accessToken=responseRefresh.json()["accessToken"] #Salviamo la variabile access toke che ci tornerà utile per i successivi test
    checkElementInresponseRefresh=json.dumps(responseRefresh.json())
    assert responseLogin.status_code == check200 
    assert all(
        [
            "accessToken" in checkElementInresponseRefresh,
            "tokenType" in checkElementInresponseRefresh,
            "refreshToken" in checkElementInresponseRefresh,
        ]
    )
    assert responseLogin.json()["accessToken"]!=""
    assert responseLogin.json()["tokenType"]!=""
    assert responseLogin.json()["refreshToken"]!=""
    assert responseRefresh.status_code == check200
    assert all(
        [
            "accessToken" in json.dumps(responseRefresh.json()),
            "tokenType" in json.dumps(responseRefresh.json()),
            "refreshToken" in json.dumps(responseRefresh.json()),
        ]
    )
    assert responseRefresh.json()["accessToken"]!=""
    assert responseRefresh.json()["tokenType"]!=""
    assert responseRefresh.json()["refreshToken"]!=""

    
    """
    1.Il seguete test permette a un Utnete Normale di ricevere una lista di tutte le info delle banche
    2.successivamente verranno salvati tutti gli id di tutte banche trovate 
    3.verrà poi scelto un id a caso tra quelli memorizzati e si usera per invocare le info della banca a cui si riferisce
    """  
    #---------------TF_Banks_1---------------#
@pytest.mark.test
def test_banks_and_banks_bankid(ambiente):
    payload1 = json.dumps(banks["banks"]["payload"])
    
    banks["banks"]["headers"]["Authorization"]= banks["banks"]["headers"]["Authorization"]+accessToken
    headers1=banks["banks"]["headers"]
    responseBs = requests.request("GET",base_urls[ambiente]["baseUrl"]+banks["endpoint"], headers=headers1, data=payload1)

    data = responseBs.json()["result"]
    global banksIds
    for bank in data:
     banksIds.append(bank["id"])

    c=len(banksIds)
    i=random.randrange(0, c)

    #aggiorna l'endpoint dell'url con l'id della banca
    global bankId
    bankId=str(banksIds[i])
    endpoint=banks["endpoint"]+"/"+bankId
    headersBankId=banks["banks"]["headers"]
    responseB = requests.request("GET",base_urls[ambiente]["baseUrl"]+endpoint, headers=headersBankId, data=payload1)
    data = responseB.json()
    global adapterName
    adapterName=data["adapterName"]
    print(data)
    
    assert responseBs.status_code == check200
    assert responseB.status_code == check200

 #---------------TF_Users_1---------------#

@pytest.mark.test
def test_users_TF_2(ambiente):
    #ABBIAMO CREATO L'UTENTE
    payloadCu=users["users"]["payload"]
    users["users"]["headers"]["Authorization"]=users["users"]["headers"]["Authorization"]+accessToken
    headersCu=users["users"]["headers"]
    responseCU = requests.request("POST",base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"],headers=headersCu, data=payloadCu)
    userId=responseCU.json()["id"]
    print("_------------------------CREATO UTENTE ------------------------------")
    #CREATE BANK ACCOUNT TYPE BANK ACCOUNT

    #REMINDER

    #NBBBBBB RICORDATI DI CAMBIARE l'8 IN str(bankId)
    # 
    #REMINDER sostituire ad 1 str(bankId)
    urlBa=base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["usersUserIdBanksBankId"]["endpoint"]+"/"+str(bankId)
    payloadBa=json.dumps(users["usersUserIdBanksBankId"]["payloadBankAccount"])
    users["usersUserIdBanksBankId"]["headers"]["Authorization"]=users["usersUserIdBanksBankId"]["headers"]["Authorization"]+accessToken
    headersBa=users["usersUserIdBanksBankId"]["headers"]
    responseBa=requests.request("POST",urlBa,headers=headersBa,data=payloadBa)
    print("--------------------------CREATO BANK ACCOUNT----------------------------------")
    #CREATE BANK ACCOUNT TYPE CARD ACCOUNT
    payloadCa=json.dumps(users["usersUserIdBanksBankId"]["payloadCardAccount"])
    responseCa=requests.request("POST",urlBa,headers=headersBa,data=payloadCa)
    print(payloadBa)
    print(payloadCa)
    print("------------------------------------------------------------------")
    print("---------------------------CREATO CARD ACCOUNT-------------------------------")
    global accountIdBank
    accountIdBank=responseBa.json()["accountId"]
    global accountIdCard
    accountIdCard=responseCa.json()["accountId"]
    print(accountIdBank)
    print(accountIdCard)
    #GET BANK ACCOUNT FOR USER:
    urlGetBank=base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["usersUserIdBanksBankId"]["endpoint"]
    users["getBankAccount"]["headers"]["Authorization"]=users["getBankAccount"]["headers"]["Authorization"]+accessToken
    headersGetBank=users["getBankAccount"]["headers"]
    payloadGetBank=users["getBankAccount"]["payload"]
    responseGetBank=requests.request("GET",urlGetBank,headers=headersGetBank,data=payloadGetBank)
    data=responseGetBank.json()
    print(data)

    #CREATE TRANSACTION
    urlTransation=base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["usersUserIdBanksBankId"]["endpoint"]+"/"+str(bankId)+users["createTransaction"]["endpoint"]
    
    users["createTransaction"]["headers"]["Authorization"]=users["createTransaction"]["headers"]["Authorization"]+accessToken
    headersCreateTransaction=users["createTransaction"]["headers"]
    payloadCreateTransaction=json.dumps(users["createTransaction"]["payload"])
    responseCreateTransaction=requests.request("POST",urlTransation,headers=headersCreateTransaction,data=payloadCreateTransaction)

    #GET TRANSACTIONS 

    #for single user single banks
    users["getTransaction"]["headers"]["Authorization"]=users["getTransaction"]["headers"]["Authorization"]+accessToken
    headersSingleUserBank=users["getTransaction"]["headers"]
    payloadSingleUserBank=users["getTransaction"]["payload"]
    responseSingleUserBank=requests.request("GET",urlTransation,headers=headersSingleUserBank,data=payloadSingleUserBank)
    
    #for a User
    urlAllTransaction= base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["createTransaction"]["endpoint"]
    headersForUser=users["getTransaction"]["headers"]
    payloadForUser=users["getTransaction"]["payload"]
    responseForUser=requests.request("GET",urlAllTransaction,headers=headersForUser,data=payloadForUser)

    #for single user single account
    urlSingleUserSingleAccountBank= base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["accounts"]+"/"+str(accountIdBank)+users["createTransaction"]["endpoint"]
    headersSingleUserSingleAccount=users["getTransaction"]["headers"]
    payloadSingleUserSingleAccount=users["getTransaction"]["payload"]
    responseSingleUserSingleAccountBank=requests.request("GET",urlSingleUserSingleAccountBank,headers=headersSingleUserSingleAccount,data=payloadSingleUserSingleAccount)
   
    urlSingleUserSingleAccountCard= base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["accounts"]+"/"+str(accountIdCard)+users["createTransaction"]["endpoint"]
    responseSingleUserSingleAccountCard=requests.request("GET",urlSingleUserSingleAccountCard,headers=headersSingleUserSingleAccount,data=payloadSingleUserSingleAccount)
    
    #SCA conflit 
   
   
   
    #START SCA
    urlStartSCA=base_urls[ambiente]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+banks["endpoint"]+"/"+str(bankId)+sca["endpoint"]
    payloadStartSca=json.dumps(sca["Adapters"][str(adapterName)])

    sca["headers"]["Authorization"]=sca["headers"]["Authorization"]+accessToken
    headersStartSca=sca["headers"]
    responseStartSca=requests.request("POST",urlStartSCA,headers=headersStartSca,data=payloadStartSca)



    #status SCA



    #REFRESH in SCA status OK



    checkElementInResponseCu=json.dumps(responseCU.json())
    assert responseCU.status_code==check201
    assert all([
        "id"in checkElementInResponseCu,
        "clientId" in checkElementInResponseCu,
        "createdTimestamp" in checkElementInResponseCu,
        "updatedTimestamp" in checkElementInResponseCu,
        "isDeleted" in checkElementInResponseCu,
        "createdBy" in checkElementInResponseCu,
        "updatedBy" in checkElementInResponseCu,
    ])

    
    assert responseBa.status_code==check200 
    assert "accountId" in json.dumps(responseBa.json())
    assert responseCa.status_code==check200 
    assert "accountId" in json.dumps(responseCa.json())
    assert responseGetBank.status_code==check200
    assert responseCreateTransaction.status_code==check200
    assert "id" in json.dumps(responseCreateTransaction.json())
    assert responseSingleUserBank.status_code == check200
    assert responseForUser.status_code == check200
    assert responseSingleUserSingleAccountBank.status_code==check200
    assert responseSingleUserSingleAccountCard.status_code==check200
    assert responseStartSca.status_code==check500

    