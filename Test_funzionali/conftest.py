import pytest
import json
def pytest_addoption(parser):
    file3_json=open("enviroments.json")
    env=json.load(file3_json)
    nomi = list(env.keys())    
    parser.addoption("--ambiente", action="store", type=str, default="Preprod", help="Ambiente di testing",choices=nomi)

@pytest.fixture
def ambiente(request):

    return request.config.getoption("--ambiente")