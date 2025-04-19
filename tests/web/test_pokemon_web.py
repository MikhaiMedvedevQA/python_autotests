import requests
import pytest

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.conf import Cfg

URL='https://pokemonbattle-stage.ru/login'

# определяем CSS локаторы
class Locators:
    """
    Class for locators
    """
    EMAIL = '[class*="k_form_control"] [id="k_email"]'
    PASSWORD = '[class*="k_form_control"] [id="k_password"]'
    ENTER_BUTTON = '[class*="k_form_send_auth"]'
    TRAINER_ID = '[class="header_card_trainer_id_num"]'
    ALERT = '[class*="auth__error"]'
    POK_TOTAL_COUNT ='[class*="pokemons"] [class*="total-count"] '

# ------------- позитивный тест проверки авторизации ------------
# @pytest.mark.xfail (reason="Wait for fix bug #2445") # так помечают тест который не проходит
def test_positive_login(browser): # вставим в аргумент нашего теста фикстуру browser
    '''
    TRP-1 Positive login case -- это название теста в TMS
    '''
   
    # открываем URL - стр. логин и пароль
    browser.get(URL)
    # найдем на странице CSS селектор <class> поля ввода email -> class="MuiInputBase-input MuiOutlinedInput-input k_form_f_email css-1pk1fka"
    # и присвоим значение переменной 
    email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiInputBase-input MuiOutlinedInput-input k_form_f_email css-1pk1fka"]')
    # такой же результат при поиске по <id>
    # email_input = browser.find_element(by=By.CSS_SELECTOR, value='[id="k_email"]')
    # кликнем на это поле
    email_input.click()
    # введем адрес почты
    email_input.send_keys('2371diverse@indigobook.com')
    # находим так же селектор поля пароль по селектору iD
    # и присваиваем переменной
    password_input = browser.find_element(by=By.CSS_SELECTOR, value='[id="k_password"]')
    password_input.click()
    password_input.send_keys('123Qwe')
    # находим так же селектор кнопки ВОЙТИ по селектору class
    # и присваиваем переменной
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class="MuiButtonBase-root MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeLarge MuiButton-containedSizeLarge MuiButton-colorPrimary MuiButton-fullWidth style_1_popup_white_base_button_orange style_1_caption_14_500 k_form_send_auth css-cm2fpt"]')
    button.click() # кликаем и переходим на загланую страницу Покемонов!
    
    # Вводим условное ожидание на 10 сек проверять кажд. 2 сек пока URL не станет ... 
    WebDriverWait(browser,timeout=10,poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/'))
    
    # находим справа вверху на странице ID тренера 
    # и присваиваим переменной
    trainer_id = browser.find_element(by=By.CSS_SELECTOR, value='[class="header_card_trainer_id_num"]')
    
    # обработаем text в переменной trainer_id используя строковую функцию
    # в этом примере не используется 
    # text_id = trainer_id.text.replace('/n', ' ')
    
    # утверждаю, что 
    assert trainer_id.text == '2318', 'Unexpected trainer_id'
    # ести ID не совпадает, то "Неожиданый ID тренера"

# ------------------негативный тест проверки авторизации ----------------------
# определяем сценарии параметризации --> в переменной, как список кортежей --> VAR = [(...), (...), (...)]
CASES = [
    ('0', '', '', 'Введите почту'), # пустые оба поля
    # ('1', '2371diverseindigobook.com', '', 'Введите корректную почту'), # почта без @
    ('2', '2371diverse@indigobook.com', '123Qwr', 'Неверные логин или пароль'), # неверный пароль
    ('3', '2371diverse@indigobook', '123Qwe', 'Введите корректную почту'), # почта без домена
    ('4', '', '123Qwe', 'Введите почту'), # почта не указана
    ('5', '2371diverse@indigobook.com', '', 'Введите пароль') # пароль не указан
]
# задаем параметры параметризации, по которым будем прогонять тест
@pytest.mark.parametrize ('case_number, email, password, alerts', CASES)

# вставим в аргумент нашего теста фикстуру browser 
# и добавим сценарии параметризации
def test_negative_login(case_number, email, password, alerts, browser):
    '''
    TRP-2 Negative case
    '''
# добавляем логирование с помощь библиотеки loguru
    logger.info(f'CASE : {case_number}')

    # открываем URL - стр. логин и пароль
    browser.get(URL)
    # найдем на странице CSS селектор <class> поля ввода email
    #email_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_f_email"][id="k_email"]')
    # ищем CSS селектор по тайм-ауту, пока он не станет кликабельным
    email_input = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[class*="k_form_f_email"][id="k_email"]')))
    # такой же результат при поиске по <id>
    # кликнем на это поле
    email_input.click()
    # введем адрес почты из параметров параметризации
    email_input.send_keys(email)
    # находим так же селектор поля пароль по селектору iD
    # и присваиваем переменной
    password_input = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_f_pass"][id="k_password"]')
    password_input.click()
    password_input.send_keys(password)
    # находим так же селектор кнопки ВОЙТИ по селектору class
    # и присваиваем переменной
    button = browser.find_element(by=By.CSS_SELECTOR, value='[class*="k_form_send_auth"]')
    button.click() # кликаем Войти
    
    # WebDriverWait(browser,timeout=60,poll_frequency=2).until(EC.url_to_be('https://pokemonbattle-stage.ru/login/'))
    # находим на странице алерт Веведите корр.почту и Ведите пароль по селктору class*=...
    # alerts_messages =browser.find_element(by=By.CSS_SELECTOR, value='[class*="auth__error"]')
  
    alerts_messages = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[class*="auth__error"]')))
    '''
    -- Этот код уже не актуален в текущей версии, так как на странице
    определяется только один алерт --
    alerts_list = [] # новая переменная для списка алертов
    # цикл для записи элементов в список
    for element in alerts_messages:
        alerts_list.append(element.text)
    '''    
    # alerts_list = alerts_messages.text # новая переменная для списка алертов
    
    assert alerts_messages.text == alerts, 'Unexpected alerts in authentification form'

# ---------------- сквозной тест покемонов -----------------------------------
def test_chek_api(browser, knockout):
    '''
    TPR-3 Check API
    '''
    # вызываем фикстуру browser, загружаем стр. логина и пароля
    browser.get(url=URL)
    # ищем CSS селектор по тайм-ауту, пока он не станет кликабельным
    email_input = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, Locators.EMAIL)))
    email_input.click()
    # введем адрес почты
    email_input.send_keys(Cfg.VALID['email'])
    # вводим пароль
    password = browser.find_element(by=By.CSS_SELECTOR, value=Locators.PASSWORD)
    password.click()
    password.send_keys(Cfg.VALID['password'])
    # находим так же селектор кнопки ВОЙТИ
    enter_button = browser.find_element(by=By.CSS_SELECTOR, value=Locators.ENTER_BUTTON)
    enter_button.click()
    # ждем пока страница загрузиться
    WebDriverWait(browser, timeout=5, poll_frequency=1).until(EC.url_to_be(f'{Cfg.URL}/'))
    # ищем кнопку для перехода на страницу тренера (используем тайм-аут,
    # пока кнопка не станет кликабельной) и кликаем
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, Locators.TRAINER_ID))).click()
    # на странице тренера находим кнопку Pokemons №№ >
    poke = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[class*="pokemon_one_body_content_inner_pokemons"]')))
    # ?? через lambda x проверяем, что  у poke class не содержит 'feature-empty'??
    WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        lambda x: 'feature-empty' not in poke.get_attribute('class'))
    # записываем в переменную текущее кол-во покемонов
    pokemon_count_before = browser.find_element(by=By.CSS_SELECTOR, value=Locators.POK_TOTAL_COUNT)
    count_before = int(pokemon_count_before.text)
    # формируем боди запроса
    body_create = {
        "name": "Mr""generate",
        "photo_id": -1
    }
    # хэдер с токеном
    header = {'Content-Type':'application/json','trainer_token': Cfg.TRAINER_TOKEN}
    # запрос на создание покемона
    response_create = requests.post(url=f'{Cfg.API_URL}/pokemons', headers=header, json=body_create, timeout=3)
    # покемон создан код ответа 201
    assert response_create.status_code == 201, 'Unexpected response status_code'
    # обновляем страницу
    browser.refresh()
    # считываем текущее количество покемонов
    # записываем целое число в переменную
    pokemon_count_after=WebDriverWait(browser, timeout=5, poll_frequency=1).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, Locators.POK_TOTAL_COUNT)))
    count_after = int(pokemon_count_after.text)
    # утверждаю, что появился один покемон
    assert count_after - count_before == 1, 'Unexpected pokemons count'

    
