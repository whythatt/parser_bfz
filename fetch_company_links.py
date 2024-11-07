import json
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Список городов
citys = [
    "Абакан",
    "Архангельск",
    "Астрахань",
    "Барнаул",
    "Белгород",
    "Бийск",
    "Благовещенск",
    "Братск",
    "Брянск",
    "Великий Новгород",
    "Владивосток",
    "Владикавказ",
    "Владимир",
    "Волгоград",
    "Вологда",
    "Воронеж",
    "Грозный",
    "Екатеринбург",
    "Иваново",
    "Ижевск",
    "Иркутск",
    "Казань",
    "Калининград",
    "Калуга",
    "Каменск-Уральский",
    "Кемерово",
    "Киров",
    "Комсомольск-на-Амуре",
    "Королев",
    "Кострома",
    "Краснодар",
    "Красноярск",
    "Курск",
    "Липецк",
    "Магнитогорск",
    "Махачкала",
    "Москва",
    "Мурманск",
    "Набережные Челны",  # Полное название
    "Нижний Новгород",  # Полное название
    "Новокузнецк",
    "Новороссийск",
    "Новосибирск",  # Исправлено с 'Ново ибирск'
    "Норильск",
    "Омск",
    "Орел",
    "Оренбург",
    "Пенза",
    "Первоуральск",
    "Пермь",
    "Прокопьевск",
    "Псков",
    "Ростов-на-Дону",  # Полное название
    "Рыбинск",
    "Рязань",  # Исправлено с 'Cамара' на 'Самара'
    "Самара",  # Исправлено
    "Санкт-Петербург",  # Полное название
    "Саратов",
    "Севастополь",  # Полное название
    "Северодвинск",
    "Симферополь",
    "Сочи",
    "Ставрополь",
    "Тамбов",
    "Тверь",
    "Тольяти",
    "Томск",
    "Тула",
    "Tюмень",
    "Улан-Удэ",
    "Ульяновск",
    "Уфа",
    "Хабаровск",
    "Чебоксары",
    "Челябинск",
    "Шахты",
    "Энгельс",
    "Южно-Сахалинск",
    "Якутск",
    "Ярославль",
]

# Настройка драйвера
driver = webdriver.Chrome()

all_company_links = {}

for city in citys[:5]:
    # Открытие Яндекс Карт
    driver.get("https://yandex.ru/maps")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".input__control"))
    )

    # Поиск по запросу
    search_box = driver.find_element(
        By.CSS_SELECTOR, ".input__control"
    )  # Найдите правильный ID элемента поиска
    search_box.clear()  # Очистка поля перед вводом
    search_box.send_keys(f"{city} банкротство юридических лиц")
    search_box.send_keys(Keys.RETURN)

    # time.sleep(5)  # Задержка для загрузки результатов

    # Прокрутка страницы до загрузки всех данных (можно адаптировать под ваши нужды)
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".scroll__container"))
    )

    # Прокрутка указанного блока до загрузки всех данных
    last_height = driver.execute_script(
        "return document.querySelector('.scroll__container').scrollHeight"
    )
    time.sleep(4)

    while True:
        elem = driver.find_element(By.CLASS_NAME, "scroll__container")
        elem.send_keys(Keys.END)
        time.sleep(4)
        new_height = driver.execute_script(
            "return document.querySelector('.scroll__container').scrollHeight"
        )
        if new_height == last_height:
            break

        last_height = new_height

    page_source = driver.page_source
    tree = etree.fromstring(page_source, etree.HTMLParser())

    all_links = tree.xpath('//a[@class="link-overlay"]/@href')

    company_links = ["https://yandex.ru" + link for link in all_links]

    # Добавляем ссылки в словарь под названием города
    all_company_links[city] = company_links

# Сохранение всех собранных данных в JSON файл
with open("company_links.json", "w", encoding="utf-8") as file:
    json.dump(all_company_links, file, indent=4, ensure_ascii=False)

# Закрытие драйвера
driver.quit()
