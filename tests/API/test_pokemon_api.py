import requests
import pytest

URL='https://api.pokemonbattle.ru/v2'
TOKEN='c11d6ec26c7f618fc5471769114ec6ce'
TRAINER_ID='28596'
HEADER={
    'Content-Type': 'application/json', 
    'trainer_token':TOKEN
}

def test_trainer_name():
    response=requests.get(url=f'{URL}/trainers/', params={'trainer_id':TRAINER_ID})
    assert response.json()['data'][0]['trainer_name'] == "Петрович"
def test_status_code():
    response=requests.get(url=f'{URL}/trainers/')
    assert response.status_code==200