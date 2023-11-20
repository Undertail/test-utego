import pytest
import json
import requests

fileEnviroment_json=open("enviroments.json")
base_urls=json.load(fileEnviroment_json)
fileAuth_json = open("auth.json")
global auth
auth=json.load(fileAuth_json)
global error401
error401=401
global check200
check200=200
global check201
check201=201
global enviroment
global accessToken
fileUsers_json=open("users.json")
users=json.load(fileUsers_json)
global bankId

@pytest.mark.test
class test_tfUser:
    """Questa classe permette di testare tutte le funzionalità relative ai servizi user
    """
    def set_enviroment(type: str):
        """Questo metodo permette di selezionare il tipo di enviroment in cui operare

        Args:
            type (str): Tipo di enviroment scelto
        """        
        global enviroment
        enviroment=type
    def set_access_token(token: str):
        """Questo metodo permette di impostare l'access token necessario ai fini dell'autenticazione

        Args:
            token (str): Access Token dell'utente
        """        
        global accessToken
        accessToken=token
    def set_bank_id(id: int):
        """Questo metodo permette di impostare il bank id utile ai fini del testing

        Args:
            id (int): Bank Id su cui andremo ad effettuare tutte le operazioni
        """        
        global bankId
        bankId=id
    @pytest.mark.test
    def test_users_TF_2():
        """Il metodo permette di testare nel seguente ordine:
        -La creazione dell'utente
        -La creazione di un account di tipo Bank e Card
        -La creazione di una transaction
        -L'ottenimento di tutte le informazioni relative alla transaction e all'account
        """        
        #ABBIAMO CREATO L'UTENTE
        payloadCu=users["users"]["payload"]
        users["users"]["headers"]["Authorization"]=users["users"]["headers"]["Authorization"]+accessToken
        headersCu=users["users"]["headers"]
        responseCU = requests.request("POST",base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"],headers=headersCu, data=payloadCu)
        userId=responseCU.json()["id"]
        print("_------------------------CREATO UTENTE ------------------------------")
        #CREATE BANK ACCOUNT TYPE BANK ACCOUNT

        #REMINDER

        #NBBBBBB RICORDATI DI CAMBIARE l'8 IN str(bankId)
        # 
        #REMINDER sostituire ad 1 str(bankId)
        urlBa=base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["usersUserIdBanksBankId"]["endpoint"]+"/"+str(bankId)
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
        urlGetBank=base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["usersUserIdBanksBankId"]["endpoint"]
        users["getBankAccount"]["headers"]["Authorization"]=users["getBankAccount"]["headers"]["Authorization"]+accessToken
        headersGetBank=users["getBankAccount"]["headers"]
        payloadGetBank=users["getBankAccount"]["payload"]
        responseGetBank=requests.request("GET",urlGetBank,headers=headersGetBank,data=payloadGetBank)
        data=responseGetBank.json()
        print(data)

        #CREATE TRANSACTION
        urlTransation=base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["usersUserIdBanksBankId"]["endpoint"]+"/"+str(bankId)+users["createTransaction"]["endpoint"]
        
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
        urlAllTransaction= base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["createTransaction"]["endpoint"]
        headersForUser=users["getTransaction"]["headers"]
        payloadForUser=users["getTransaction"]["payload"]
        responseForUser=requests.request("GET",urlAllTransaction,headers=headersForUser,data=payloadForUser)

        #for single user single account
        urlSingleUserSingleAccountBank= base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["accounts"]+"/"+str(accountIdBank)+users["createTransaction"]["endpoint"]
        headersSingleUserSingleAccount=users["getTransaction"]["headers"]
        payloadSingleUserSingleAccount=users["getTransaction"]["payload"]
        responseSingleUserSingleAccountBank=requests.request("GET",urlSingleUserSingleAccountBank,headers=headersSingleUserSingleAccount,data=payloadSingleUserSingleAccount)
    
        urlSingleUserSingleAccountCard= base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["accounts"]+"/"+str(accountIdCard)+users["createTransaction"]["endpoint"]
        responseSingleUserSingleAccountCard=requests.request("GET",urlSingleUserSingleAccountCard,headers=headersSingleUserSingleAccount,data=payloadSingleUserSingleAccount)
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
        return userId