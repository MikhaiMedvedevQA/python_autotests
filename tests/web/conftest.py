# файл фикстур для настройки и запуска браузера
import requests
import pytest

#from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from common.conf import Cfg

@pytest.fixture(scope="function") # обязательное устовие для подключения фикстуры
def browser(): # НАЗВАНИЕ ФИКСТУРЫ
    '''
    Basic fixture
    '''
    # настраиваем параметры запуска браузера
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") # disabling sandbox
    # chrome_options.add_argument("start-maximized") # open browser in maximazed mode
    chrome_options.add_argument("--dasable-infobars") # disabling infobars
    chrome_options.add_argument("--disable-extensions") # disabling extensions
    chrome_options.add_argument("--disable-gpu") # applicable to windows os only
    chrome_options.add_argument("--disable-dev-shm-usage") #overcome limited resource problem
    chrome_options.add_argument("--headless") # "безголовый режим"
    # определяем переменную
    service = Service()
    # создаем объект driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    #возращаем объект из фикстуры для использования его в тестах
    yield driver 
    # все что идет далее можно посмотреть в Teardown Allure
    # можо сохранять скриншоты, видео, подчищать БД, сохранить/удалить логи
    driver.quit() # закрывает браузер при любом исходе теста

@pytest.fixture(scope="function")
def knockout(): 
    """
    Knockout all pokemons
    """
    # готовим тестовое окружение для проведения тестов
    # в хедер записываем обязательные параметры
    header = {'Content-Type':'application/json','trainer_token': Cfg.TRAINER_TOKEN}
    # запрашиваем список всех покемонов тренера
    pokemons = requests.get(url=f'{Cfg.API_URL}/pokemons', params={"trainer_id": Cfg.TRAINER_ID},
                            headers=header, timeout=3)
    # если data в json = true
    if 'data' in pokemons.json():
    # то перебираем всех покемонов,
        for pokemon in pokemons.json()['data']:
    # находим кто живой (status !=0)
            if pokemon['status'] != 0:
    # и отправляем его в нокаут --> POST
                requests.post(url=f'{Cfg.API_URL}/pokemons/knockout', headers=header,
                              json={"pokemon_id": pokemon['id']}, timeout=3)