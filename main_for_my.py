import requests

URL='https://api.pokemonbattle.ru/v2'
TOKEN='c11d6ec26c7f618fc5471769114ec6ce'
HEADER={
    'Content-Type': 'application/json', 
    'trainer_token':TOKEN
}
body_pokemon_create={
    "name": "generate",
    "photo_id": -1
}
'''body_pokemon_rename={
    "pokemon_id": "pokemon_id",
    "name": "mrGreen",
    "photo_id": 102
}'''

# создать покемона
response_create=requests.post(url=f'{URL}/pokemons/',headers=HEADER, json=body_pokemon_create)
#print(response_create.status_code)
print(response_create.text)
# записать в переменную id покемона
pok_id=response_create.json()['id']
#print('pokemon_id:', pok_id)
# переименовать покемона
response_rename=requests.put(url=f'{URL}/pokemons/',headers=HEADER, json={"pokemon_id": pok_id,
    "name": "mrGreen",
    "photo_id": 444})
#print(response_rename.status_code)
print(response_rename.text)
# добавить покемона в покеболл
response_add_pokeball=requests.post(url=f'{URL}/trainers/add_pokeball',headers=HEADER, json={"pokemon_id":pok_id})
#print(response_add_pokeball.status_code)
print(response_add_pokeball.text)
# запрос всех покемонов в покеболле
response_inpokeball_get=requests.get(url=f'{URL}/pokemons/', params={
                                                          'in_pokeball': 1,
                                                          
                                                            })
#print(response_inpokeball_get.text)
# выбрать соперника для боя и записать в переменную
alien_id=response_inpokeball_get.json()['data'][1]['id']
print ('Соперник id:', alien_id)
# провести битву
response_battle=requests.post(url=f'{URL}/battle', headers=HEADER, json={
                                                              "attacking_pokemon": pok_id,
                                                             "defending_pokemon": alien_id
                                                        })
print (response_battle.text)
'''
# отправить покемона в нокаут
response_kill=requests.post(url=f'{URL}/pokemons/knockout',headers=HEADER, json={"pokemon_id":pok_id})
print('Status code:', response_kill.status_code)
print('Response body:', response_kill.text)
'''