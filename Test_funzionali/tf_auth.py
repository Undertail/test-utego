import pytest
import json
import requests

fileenviroment_json=open("enviroments.json")
base_urls=json.load(fileenviroment_json)
fileAuth_json = open("auth.json")
global auth
auth=json.load(fileAuth_json)
global error401
error401=401
global check200
check200=200
global enviroment



@pytest.mark.test
class test_tfAuth:

    """Questa classe permette di testare tutti i servizi di tipo Auth forniti da Utego
    """
    def set_enviroment(type: str):

        """Questo metodo permette di impostare il tipo di enviroment in cui si vuole operare 

        Args:
            type (str): Variabile che indica il tipo scelto
        """        
        global enviroment
        enviroment=type
        
    @pytest.mark.timeout(6)
    def test_auth_passwordEncrypt_normal_user():

        """Questo test permette di varificare che un normal user non sia autorizzato a criptare una password 
        Se la response della request contiene come status code 401 allora il test è passato 
       """
        payload = json.dumps(auth["passwordEncrypt"]["payload"])
        headers1=auth["passwordEncrypt"]["headers"]
        responseT = requests.request("POST",base_urls[enviroment]["baseUrl"]+auth["passwordEncrypt"]["endpoint"] , headers=headers1, data=payload)            
        assert responseT.status_code == error401

    #---------------TF_Auth_1---------------#
    @pytest.mark.timeout(5)
    def test_auth_register_normal_user():

        """
        Questo test verifica che un utente di tipo normal non possa effettuare la registrazione di un nuovo utente
        """        
        payload = auth["register"]["payload"]
        headers1=auth["register"]["headers"]
        responseT = requests.request("POST",base_urls[enviroment]["baseUrl"]+auth["register"]["endpoint"],headers=headers1, data=payload)
        assert responseT.status_code == error401

    #---------------TF_Auth_3---------------#
    @pytest.mark.test
    def test_auth_and_invalidate():

        """Questo test verifica che l'utente effettui correttamente login e logout
        """ 
        #Viene fatto il login
        payloadLogin = json.dumps(base_urls[enviroment]["keys"]) 
        headersLogin=auth["login"]["headers"]
        responseLogin = requests.request("POST",base_urls[enviroment]["baseUrl"]+auth["login"]["endpoint"], headers=headersLogin, data=payloadLogin)
        #Viene fatto l'invalidate
        payloadInvalidate=json.dumps(auth["invalidate"]["payload"])
        auth["invalidate"]["headers"]["Authorization"]=auth["invalidate"]["headers"]["Authorization"]+responseLogin.json()["accessToken"]
        headersInvalidate=auth["invalidate"]["headers"]
        responseInvalidate = requests.request("POST",base_urls[enviroment]["baseUrl"]+auth["invalidate"]["endpoint"], headers=headersInvalidate, data=payloadInvalidate)
        assert responseInvalidate.status_code == check200
        assert type(responseInvalidate.json()["invalidatedForClient"]) is int and responseInvalidate.json()["invalidatedForClient"]>=0

    #---------------TF_Auth_2---------------#

    @pytest.mark.test
    def test_auth_login():

        """
        Questo test verifica che l'autenticazione da parte dell'utente avvenga con successo

        Returns:
            json: Restituisce la response necessaria ad ottenere tutti i token utili per i test successivi
        """     
        payloadLogin = json.dumps(base_urls[enviroment]["keys"]) 
        headersLogin=auth["login"]["headers"]
        responseLogin = requests.request("POST",base_urls[enviroment]["baseUrl"]+auth["login"]["endpoint"], headers=headersLogin, data=payloadLogin)
        assert responseLogin.status_code == check200
        assert responseLogin.json()["accessToken"]!=""
        assert responseLogin.json()["tokenType"]!=""
        assert responseLogin.json()["refreshToken"]!=""
        return responseLogin

    @pytest.mark.test
    def test_auth_refresh(responseLogin):
        
        """Questo test verifica che avvenga con successo la funzionalità di refresh token

        Args:
            responseLogin (json): response generata dal metodo test_auth_login che contiene i vari token utili per poter proseguire con il test

        """        
        auth["refresh"]["payload"]["token"]=responseLogin.json()["refreshToken"]
        #Viene fatto il refresh
        payloadRefresh=json.dumps(auth["refresh"]["payload"])
        auth["refresh"]["headers"]["Authorization"]=auth["refresh"]["headers"]["Authorization"]+responseLogin.json()["accessToken"]
        headersRefresh=auth["refresh"]["headers"]
        responseRefresh = requests.request("POST",base_urls[enviroment]["baseUrl"]+auth["refresh"]["endpoint"], headers=headersRefresh, data=payloadRefresh)        
        checkElementInresponseRefresh=json.dumps(responseRefresh.json())
        

        assert all(
            [
                "accessToken" in checkElementInresponseRefresh,
                "tokenType" in checkElementInresponseRefresh,
                "refreshToken" in checkElementInresponseRefresh,
            ]
        )
        
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