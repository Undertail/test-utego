# transaction_value.py
import json
import uuid
import requests
import pandas as pd


df=pd.read_json('TOKEN_REQUEST.json')
print(df)

class TranscationValue:
    # variabili usate per generare il token
    def __init__(self, n: int):
        if n == 0:
            file_json = open("TOKEN_REQUEST.json")
            dat = json.load(file_json)
            self.urlToken = dat["urlToken"]
            self.payloadToken = dat["payloadToken"]
            self.headersToken =dat["headersToken"]
            self.post =dat["post"]
            self.tag_acces_token =dat["tag_acces_token"]
            self.urlsca1 =dat["urlsca1"]
            self.requestID = ""
            self.payloadSCA1 =json.dumps(dat["payloadSCA1"])
            self.paymentId = ""
            self.token = ""
            self.linkSCA1 = ""
            self.linkSCA2 = ""


    def givToken(self):
        # ("-------------------------------------------------------------------------------------------")
        # ("TOKEN GEN")
        # "-------------------------------------------------------------------------------------------")
        responseT = requests.request(self.post, self.urlToken, headers=self.headersToken, data=self.payloadToken,
                                     cert=(
                                         "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_public.crt",
                                         "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_pkcs8.key"))
        self.token = responseT.json()[self.tag_acces_token]


    def givLinkSCA1(self):
        # ("-------------------------------------------------------------------------------------------")
        # ("TRANSAZIONE---sca1")
        # ("-------------------------------------------------------------------------------------------")
        self.requestID = str(uuid.uuid4)
        file_json = open("SCA1.json")
        dat = json.load(file_json)
        dat["headers1"]["authorization"]= dat["headers1"]["authorization"]+self.token
        dat["headers1"]["x-request-id"]=self.requestID
        headers1 = dat["headers1"]
        response = requests.request(self.post, self.urlsca1, headers=headers1, data=self.payloadSCA1, cert=(
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_public.crt",
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_pkcs8.key"))
        print(response)
        self.paymentId = response.json()["paymentId"]
   
        self.responseSca1=str(response.json())
        self.linkSCA1 = response.json()['_links']['scaRedirect']["href"]


    def getResponseStatusSCA(self):
        # ("_-------------------------------------------------------------------------------------------")
        # ("GET STATUS")
        # ("_-------------------------------------------------------------------------------------------")
        file_json = open("GET_STATUS.json")
        dat = json.load(file_json)
        urlS = dat["urlS"] + self.paymentId + dat["status"]
        payload =dat["payload"]
        dat["headers2"]["authorization"]= dat["headers2"]["authorization"]+self.token
        dat["headers2"]["x-request-id"]=self.requestID
        headers2 = dat["headers2"]
        responseS = requests.request("GET", urlS, headers=headers2, data=payload, cert=(
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_public.crt",
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_pkcs8.key"))
        
        self.linkSCA2 = str(responseS.json()["_links"]["scaRedirect"]["href"])
        return str(responseS.json())
     
    def getResponseStatusSCAFinal(self):
        # ("_-------------------------------------------------------------------------------------------")
        # ("GET STATUS")
        # ("_-------------------------------------------------------------------------------------------")
        file_json = open("GET_STATUS.json")
        dat = json.load(file_json)
        urlS = dat["urlS"] + self.paymentId + dat["status"]
        payload =dat["payload"]
        dat["headers2"]["authorization"]= dat["headers2"]["authorization"]+self.token
        dat["headers2"]["x-request-id"]=self.requestID
        headers2 = dat["headers2"]
        responseS = requests.request("GET", urlS, headers=headers2, data=payload, cert=(
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_public.crt",
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_pkcs8.key"))
    
        return str(responseS.json()['scaStatus'])

       