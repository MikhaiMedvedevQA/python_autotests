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

response_create=requests.post(url=f'{URL}/pokemons/',headers=HEADER, json=body_pokemon_create)
print(response_create.status_code)
print(response_create.text)

new_poke_id=response_create.json()['id']

response_rename=requests.put(url=f'{URL}/pokemons/',headers=HEADER, json={"pokemon_id": new_poke_id,
                                                                        "name": "mrGreen",
                                                                        "photo_id": 444
                                                                        })
print(response_rename.status_code)
print(response_rename.text)

response_add_pokeball=requests.post(url=f'{URL}/trainers/add_pokeball',headers=HEADER, json={"pokemon_id":new_poke_id})
print(response_add_pokeball.status_code)
print(response_add_pokeball.text)
