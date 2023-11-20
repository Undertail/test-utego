# transaction_value.py
import json
import uuid
import requests


class TranscationValue:
    # variabili usate per generare il token
    def __init__(self, n: int):
        if n == 0:
            self.urlToken = "https://sbxcbiglobeopenbankingapigateway.nexi.it/auth/oauth/v2/token"
            self.payloadToken = 'grant_type=client_credentials&scope=sandbox&client_id=cb42c0cf-27a4-4f57-90b1-0b369aa7b97e&client_secret=3853283b-f05c-4f39-a740-92c6fee88227'
            self.headersToken = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            self.post = "POST"
            self.tag_acces_token = "access_token"
            self.urlsca1 = (
                "https://sbxcbiglobeopenbankingapigateway.nexi.it/platform/enabler/psd2orchestrator/pis/2.3.2/payments/sepa"
                "-credit-transfers")
            self.requestID = ""
            self.payloadSCA1 = json.dumps({
                "endToEndId": "9999999999999999999999",
                "instructedAmount": {
                    "amount": "10.00",
                    "currency": "EUR"
                },
                "creditorName": "Test Creditor CBI single payment",
                "requestedExecutionDate": "2024-09-19",
                "remittanceInformationUnstructured": "Payment description",
                "transactionType": "remote_transaction",
                "creditorAccount": {
                    "iban": "IT23Q0300203280736225314924",
                    "currency": "EUR"
                }
            })
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
        headers1 = {
            'Content-Type': 'application/json',
            'TPP-Redirect-URI': 'https://localhost.loc/94.89.163.149?status=OK',
            'TPP-NOK-Redirect-URI': 'https://localhost.loc/94.89.163.149 ?status=KO',
            'TPP-Redirect-Preferred': 'true',
            'authorization': 'Bearer ' + self.token,
            'x-request-id': self.requestID,
            'date': 'Mon, 18 Sep 2023 12:3:11 +0200',
            'aspsp-code': '05034',
            'aspsp-product-code': 'IBP01',
            'psu-ip-address': '127.0.0.1'
        }
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
        urlS = "https://sbxcbiglobeopenbankingapigateway.nexi.it/platform/enabler/psd2orchestrator/pis/2.3.2/payments/sepa-credit-transfers/" + self.paymentId + "/status"
       
        payload = ""
        headers2 = {
            'authorization': 'Bearer ' + self.token,
            'x-request-id': self.requestID,
            'date': 'Mon, 18 Sep 2023 12:55:40 +0200',
            'aspsp-code': '05034'
        }
        responseS = requests.request("GET", urlS, headers=headers2, data=payload, cert=(
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_public.crt",
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_pkcs8.key"))
        
        self.linkSCA2 = str(responseS.json()["_links"]["scaRedirect"]["href"])
        return str(responseS.json())
     
    def getResponseStatusSCAFinal(self):
        # ("_-------------------------------------------------------------------------------------------")
        # ("GET STATUS")
        # ("_-------------------------------------------------------------------------------------------")
        urlS = "https://sbxcbiglobeopenbankingapigateway.nexi.it/platform/enabler/psd2orchestrator/pis/2.3.2/payments/sepa-credit-transfers/" + self.paymentId + "/status"
       
        payload = ""
        headersS = {
            'authorization': 'Bearer ' + self.token,
            'x-request-id': self.requestID,
            'date': 'Mon, 18 Sep 2023 12:55:40 +0200',
            'aspsp-code': '05034'
        }
        responseS = requests.request("GET", urlS, headers=headersS, data=payload, cert=(
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_public.crt",
            "C:/Users/Utente/Desktop/tirocinio/CBI_Certificato/CBI_pkcs8.key"))
    
        return str(responseS.json()['scaStatus'])

       