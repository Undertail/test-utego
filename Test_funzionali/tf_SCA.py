import pytest
import json
import requests

fileBanks_json=open("responseGetBanks.json")
bankList=json.load(fileBanks_json)

fileUsers_json=open("users.json")
users=json.load(fileUsers_json)
fileEnviroment_json=open("enviroments.json")
global base_urls
base_urls=json.load(fileEnviroment_json)
fileSCA_json = open("SCA.json")
global auth
SCA=json.load(fileSCA_json)
global error401
error401=401
global check200
check200=200
global check201
check201=201
global enviroment
global accessToken
global aurigaDictionary
global finecoDictionary
global cbiDictionary
global fabrickDictionary
global siaDictionary
global unicreditDictionary
global responseList


keyDictionary={
    "aspspCode":["05034"],
    "adapterName":["CBI"]
}
aurigaDictionary={
    "aspspCode":[""],
    "psuId":["INSERT_PSU_ID",".........."],
    "password":["INSERT_PASSWORD","........."],
    "redirectUri":"https://localhost.loc/94.89.163.149?status=OK",
    "nokRedirectUri":"https://localhost.loc/94.89.163.149?status=KO"
}
finecoDictionary={
    "aspspCode":[""],
    "psuId":["INSERT_PSU_ID",".........."],
}
cbiDictionary={
    "aspspCode":["05034"],
    "psuId":["li7AuHJ","...."],
    "productId":["IBP01","..."]
}
fabrickDictionary={
    "aspspCode":[""],
    "psuId":["INSERT_PSU_ID",".........."],
}
siaDictionary={
    "aspspCode":[""],
    "psuId":["INSERT_PSU_ID",".........."],
}
unicreditDictionary={
    "aspspCode":[""],
    "psuId":["INSERT_PSU_ID",".........."],
}

def buildPayload(bank: json):
        aspspAuriga=aurigaDictionary.get("aspspCode")
        psuIdAuriga=aurigaDictionary.get("psuId")
        pwAuriga=aurigaDictionary.get("Password")
        redirectUri=aurigaDictionary.get("redirectUri")
        nokRedirectUri=aurigaDictionary.get("nokRedirectUri")
        
        aspspCBI=cbiDictionary.get("aspspCode")
        psuIdCBI=cbiDictionary.get("psuId")
        productId=cbiDictionary.get("productId")
        
        if(bank["adapterName"]=="CBI"):
            index=aspspCBI.index(bank["aspspCode"])
            SCA["adapterList"][bank["adapterName"]]["payload"]["psuId"]=psuIdCBI[index]
            SCA["adapterList"][bank["adapterName"]]["payload"]["productId"]=productId[index]
            return  json.dumps(SCA["adapterList"][bank["adapterName"]]["payload"])
        elif(bank["adapterName"]=="Auriga"):
            index=aspspAuriga.index(bank["aspspCode"])
            SCA["adapterList"][bank["adpterName"]]["payload"]["psuId"]=psuIdAuriga[index]
            SCA["adapterList"][bank["adpterName"]]["payload"]["psuId"]=pwAuriga[index]
            SCA["adapterList"][bank["adpterName"]]["payload"]["redirectUri"]=redirectUri
            SCA["adapterList"][bank["adpterName"]]["payload"]["nokRedirectUri"]=nokRedirectUri
            return  json.dumps(SCA["adapterList"][bank["adapterName"]]["payload"])
            
        elif(bank["adapterName"]=="Fineco"):
            return  SCA["adapterList"][bank["adapterName"]]["payload"]
        elif(bank["adapterName"]=="Fabirck"):
            return  SCA["adapterList"][bank["adapterName"]]["payload"]
        elif(bank["adapterName"]=="SIA"):
            return  SCA["adapterList"][bank["adapterName"]]["payload"]

        elif(bank["adapterName"]=="Unicredit"):
            return  SCA["adapterList"][bank["adapterName"]]["payload"]

@pytest.mark.test
class test_tfSCA:
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
    def set_user_id(id: int):

        global userId
        userId=id
        
    
        #da finire costruzione payload e poi chiamare response e effetuare test
       
    def test_Sca():


        aspspsCodes=keyDictionary.get("aspspCode")
        adapterNames=keyDictionary.get("adapterName")

        print(aspspsCodes[0])
        print(adapterNames[0])
        print(bankList["count"])
        c=0
        for bank in bankList["result"]:
            for j in range(0, len(aspspsCodes)):
                if(str(bank["aspspCode"])==str(aspspsCodes[j])):
                    if(bank["adapterName"]==str(adapterNames[j])):
                        print("Entro nell'if dell adapter name")
                        data=bank
                        id=data["id"]
                        print("---data----")
                        print(data)
                        print("---id----")
                        print(id)
                        #si costruisce payload header e url E BOOM FINITO, ovviamente controllo per quanto riguarda i tipi di adapter del payload
                        urlSCA=base_urls[enviroment]["baseUrl"]+users["users"]["endpoint"]+"/"+str(userId)+users["usersUserIdBanksBankId"]["endpoint"]+"/"+str(id)+SCA["endpoint"]
                        SCA["headers"]["Authorization"]+=accessToken
                        headerSCA=SCA["headers"]
                        payloadSCA= buildPayload(data)
                        responseStartSca=requests.request("POST",urlSCA,headers=headerSCA,data=payloadSCA)
                        print(responseStartSca.json())
                        #controllo che l'aspspcode trovato sia presente nei dictionary
                        scaId=responseStartSca["scaId"]
                        #QUI TESTO lo stato della sca ottenuta
                      
                       
                            

        
        





