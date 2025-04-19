import requests
import pytest

URL='https://api.pokemonbattle.ru/v2'
TOKEN='c11d6ec26c7f618fc5471769114ec6ce'
TRAINER_ID='28596'
HEADER={
    'Content-Type': 'application/json', 
    'trainer_token':TOKEN
}
# начало теста def -> проверка статуса ответа 
def test_status_code():
# переременной = запрос -> получить всех покемонов тренера (по квери-параметру = trainer.id )
    response=requests.get(url=f'{URL}/pokemons/', params={'trainer_id':TRAINER_ID})
# утверждаю, что ответ придет 200    
    assert response.status_code==200
# начало теста def -> проверка части JSON ответа
def test_part_of_response():
    response_get=requests.get(url=f'{URL}/pokemons/', params={'trainer_id':TRAINER_ID})
# утверждаю, что имя = mrGreen  
    assert response_get.json()['data'][0]['name']== 'mrGreen'
# параметризированный тест
# @ фикстура-функция =предусловие (ключ, значение=> [('x1', 'y1'),('x2', 'y2'), ....])
@pytest.mark.parametrize ('key,value',[('photo_id',444), ('name','mrGreen'), ('trainer_id',TRAINER_ID), ('id','295174')])
# начало теста ->получить всех покемонов тренера
def test_parametrize(key, value):
    response_parametrize=requests.get(url=f'{URL}/pokemons/', params={'trainer_id':TRAINER_ID})
# утверждаю,что в JSON data, в первом элементе массива ключ[key] = значению [value]   
    assert response_parametrize.json() ['data'][0][key] == value 