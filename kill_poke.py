import requests

URL='https://api.pokemonbattle-stage.ru/v2'
#TOKEN='c11d6ec26c7f618fc5471769114ec6ce'
TOKEN='30457eeab0852460084b203d77069813'
#TRAINER_ID='28596'
TRAINER_ID='2318'
HEADER={
    'Content-Type': 'application/json', 
    'trainer_token':TOKEN
}
body_pokemon_create={
    "name": "generate",
    "photo_id": -1
}
# делаем запрос всех покемонов тренера и записываем результат в переменную 
response_get=requests.get(url=f'{URL}/pokemons/', params={
                                                          'trainer_id':TRAINER_ID,
                                                          'status':1
                        })
# печать статуса ответа и JSON из боди ответа 
print(response_get.status_code)
print(response_get.text)
# условие: если ключ JSON status=success и второй ключ = Покемоны не найдены, то print
if (response_get.json()['status'])=="success" and (list(response_get.json().values())[1])=="Покемоны не найдены":
    print('Создай покемона')
else:
# присваиваем переменной значение id первого покемона из JSON
    my_poke= response_get.json()['data'][0]['id']
    print('JSON:', response_get.json()['data'])
    print('JSON:', my_poke)

# отправляем запрос на нокаут покемона, id берем из переменной
    response_kill=requests.post(url=f'{URL}/pokemons/knockout',headers=HEADER, json={"pokemon_id":my_poke})
    print('Status code:', response_kill.status_code)
    print('Response body:', response_kill.text)



'''
data = response_get.json()

if data.get('status') == "success":
    values = list(response_get.json().values())
    if len(values) > 1:
        second_value = list(response_get.json().values())[1]
        if second_value == "Покемоны не найдены":
            # Выполните необходимые действия
            print(second_value)
        else:
            # Обработка случая, когда значение не совпадает
            print("Значение не совпадает с ожидаемым.")
    else:
        print("В JSON недостаточно ключей.")
else:
    print("Статус не успешен.")
'''