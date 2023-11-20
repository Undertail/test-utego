import pytest
import json
import requests
import random

global error401
error401=401
global check200
check200=200
fileEnviroment_json=open("enviroments.json")
base_urls=json.load(fileEnviroment_json)
banksIds=[]
bankId=""
fileBanks_json = open("banks.json")
global banks
banks=json.load(fileBanks_json)
global enviroment
global accessToken

class test_tfBank:
    """Questa classe permette di testare tutti i servizi relativi alla sezione Banks
    """    
    def set_enviroment(type):
        """Questo metodo permette di impostare il tipo di enviroment in cui si intende operare

        Args:
            type (str): Tipo di enviroment selezionato
        """        
        global enviroment
        enviroment=type
    def set_access_token(token: str):
        global accessToken
        accessToken=token
    #---------------TF_Banks_1---------------#
    @pytest.mark.test
    def test_banks_and_banks_bankid():
        """Questo metodo permette di controllare che i metodi che restituiscano la lista delle banche e l'ottenimento delle informazioni di una banca inserendo il suo ID siano testati

        Returns:
            int: Id della banca selezionato casualmente che servirà per i test successivi
        """        
        payload1 = json.dumps(banks["banks"]["payload"])
        
        banks["banks"]["headers"]["Authorization"]= banks["banks"]["headers"]["Authorization"]+accessToken
        headers1=banks["banks"]["headers"]
        responseBs = requests.request("GET",base_urls[enviroment]["baseUrl"]+banks["endpoint"], headers=headers1, data=payload1)



        data = responseBs.json()["result"]
        responseBsJson=responseBs.json()


    
        # Writing to sample.json
        with open("responseGetBanks.json", "w") as outfile:
            outfile.write(json.dumps(responseBsJson))


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
        responseB = requests.request("GET",base_urls[enviroment]["baseUrl"]+endpoint, headers=headersBankId, data=payload1)
        data = responseB.json()
        global adapterName
        adapterName=data["adapterName"]
        print(data)
        
        assert responseBs.status_code == check200
        assert responseB.status_code == check200
        return bankId