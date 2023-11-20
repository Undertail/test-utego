from tf_auth import test_tfAuth
from tf_bank import test_tfBank
from tf_user import test_tfUser
from tf_SCA import test_tfSCA
import pytest
import json
global accessToken
global bankId
global userId

def test_main_auth():
    test_tfAuth.set_enviroment("preprod")
    test_tfAuth.test_auth_passwordEncrypt_normal_user()
    test_tfAuth.test_auth_register_normal_user()
    test_tfAuth.test_auth_and_invalidate()
    response=test_tfAuth.test_auth_login()
    test_tfAuth.test_auth_refresh(response)
    

def test_main_bank():
    test_tfBank.set_enviroment("preprod")
    response=test_tfAuth.test_auth_login()
    test_tfBank.set_access_token(response.json()["accessToken"])
    global bankId
    bankId=test_tfBank.test_banks_and_banks_bankid()

def test_main_user():
    test_tfUser.set_enviroment("preprod")
    response=test_tfAuth.test_auth_login()
    test_tfUser.set_access_token(response.json()["accessToken"])
    test_tfUser.set_bank_id(bankId)
    global userId
    userId=test_tfUser.test_users_TF_2()

def test_main_sca():
    response=test_tfAuth.test_auth_login()
    test_tfSCA.set_access_token(response.json()["accessToken"])
    test_tfSCA.set_enviroment("preprod")
    test_tfSCA.set_user_id(userId)
    test_tfSCA.test_Sca()