import requests
import pytest

URL='https://api.pokemonbattle.ru/v2'
TOKEN='c11d6ec26c7f618fc5471769114ec6ce'
TRAINER_ID='28596'
HEADER={
    'Content-Type': 'application/json', 
    'trainer_token':TOKEN
}
response_p=requests.get(url=f'{URL}/pokemons/', params={'trainer_id':TRAINER_ID})
#print (response_p. text)
print (response_p.json() ['data'][0]['photo_id'])