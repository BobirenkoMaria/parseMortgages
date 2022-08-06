import traceback
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import json
from logger_config import logger


HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36', 'accept': '*/*'}

info = []
mortgage = None
id_mortgage = 0


def set_headers():
    global HEADERS
    user_agent = ''

    with open('User-agents.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
        user_agent = text[random.randint(0, 44)]['id']

    HEADERS = {'user-agent': user_agent, 'accept': '*/*'}


def set_info(name, interestRate, term, initial, maxAmount):
    global id_mortgage

    info.append({
        'id': int(id_mortgage),
        'name': str(name),
        'interestRate': float(interestRate),
        'term': int(term),
        'initial': int(initial),
        'maxAmount': int(maxAmount),
    })
    id_mortgage += 1


def get_html(url, params=None):
    try:
        r = requests.get(url, headers=HEADERS, params=params)
    except requests.exceptions.ConnectionError:
        return None
    return r


def get_url():
    url = ''

    if mortgage == 1:
        url = 'https://www.sberbank.ru/ru/person/credits/home/buying_project?tab=usl'
    elif mortgage == 2:
        url = 'https://www.sberbank.ru/ru/person/credits/home/mil?tab=usl'
    elif mortgage == 3:
        url = 'https://www.sberbank.ru/ru/person/credits/home/gos_2020?tab=usl'
    elif mortgage == 4:
        url = 'https://www.sberbank.ru/ru/person/credits/home/buying_complete_house_daln?tab=usl'
    elif mortgage == 5:
        url = 'https://www.sberbank.ru/ru/person/credits/home/family?tab=usl'
    elif mortgage == 6:
        url = 'https://domclick.ru/ipoteka/programs/it-workers'
    return url


def parse(num):
    global mortgage

    try:
        mortgage = num
        URL = get_url()

        #set_headers()

        if mortgage == 0:
            return info

        html = get_html_with_driver(URL)
        get_content(html)
    except Exception:
        logger.error(traceback.format_exc())

    return info


def parser(URL):
    html = None

    while html == None:
        html = get_html(URL)
        try:
            if html.status_code == 200:
                get_content(html.text)

        except AttributeError:
            print('Connection refused')


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    if mortgage == 1:
        info_card = soup.find('div', class_='kit-col kit-col_xs_12 kit-col_lg_6 kit-col_xs-bottom_10 kit-col_lg-bottom_0 product-teaser-full-width__wrapper-feature')
        info_cards = info_card.find_all('h3', class_='kit-heading kit-heading_s')

        interestRate = soup.find('table', class_='cke_show_border t-table_borderless')
        interestRate = interestRate.find_all('td')
        interestRate = interestRate[-1].get_text()[:-1].replace(',', '.')

        term = info_cards[1].get_text()
        term = term.split()[1]
        initial = soup.find_all('div', class_='kit-text kit-text_s terms-description__text')
        initial = initial[4].get_text()
        initial = initial.split()[1][:-1]

        maxAmount = info_cards[2].get_text().split()[0]

        set_info('Обычная ипотека/Новостройка', interestRate, term, initial, maxAmount)

    elif mortgage == 2:
        info_card = soup.find('div',
                              class_='kit-col kit-col_xs_12 kit-col_lg_6 kit-col_xs-bottom_10 kit-col_lg-bottom_0 product-teaser-full-width__wrapper-feature')
        info_cards = info_card.find_all('h3', class_='kit-heading kit-heading_s')

        interestRate = soup.find_all('div', class_='bp-container h-accordion h-accordion_opened h-accordion-padding_top_extra')
        interestRate = interestRate[1].find('div', class_='kit-text kit-text_s terms-description__text')
        interestRate = interestRate.get_text().split()[0][:-1].replace(',', '.')

        term = info_cards[1].get_text()
        term = term.split()[1]
        initial = info_cards[0].get_text().split()[1][:-2].replace(',', '.')

        maxAmount = info_cards[2].get_text().split()[0]

        set_info('Военная ипотека', interestRate, term, initial, maxAmount)

    elif mortgage == 3:
        info_card = soup.find('div',
                              class_='kit-col kit-col_xs_12 kit-col_lg_6 kit-col_xs-bottom_10 kit-col_lg-bottom_0 product-teaser-full-width__wrapper-feature')
        info_cards = info_card.find_all('h3', class_='kit-heading kit-heading_s')

        interestRate = soup.find_all('div', class_='bp-area bd-bdDrop --area h-accordion__content')
        interestRate = interestRate[1].find('div', class_='rt-content')
        interestRate = interestRate.find_all('tr')
        interestRate = interestRate[1].find_all('td')
        interestRate = interestRate[1].get_text()[:-1].replace(',', '.')

        term = info_cards[1].get_text()
        term = term.split()[1]
        initial = info_cards[0].get_text().split()[1][:-2].replace(',', '.')

        maxAmount = info_cards[2].get_text().split()[0]

        set_info('Льготная ипотека/Господдержка', interestRate, term, initial, maxAmount)

    elif mortgage == 4:
        info_card = soup.find('div',
                              class_='kit-col kit-col_xs_12 kit-col_lg_6 kit-col_xs-bottom_10 kit-col_lg-bottom_0 product-teaser-full-width__wrapper-feature')
        info_cards = info_card.find_all('h3', class_='kit-heading kit-heading_s')

        interestRate = soup.find_all('div', class_='kit-text kit-text_s terms-description__text')
        interestRate = interestRate[17].get_text()[:-2].replace(',', '.')

        term = info_cards[1].get_text()
        term = term.split()[1]
        initial = info_cards[0].get_text().split()[1][:-2].replace(',', '.')

        maxAmount = info_cards[2].get_text().split()[0]

        set_info('Дальневосточная ипотека', interestRate, term, initial, maxAmount)

    elif mortgage == 5:
        info_card = soup.find('ul',
                              class_='kitt-list kitt-list_ul')
        info_cards = info_card.find_all('li', class_='kitt-list-item kitt-list-item_ul')

        interestRate = soup.find_all('div', class_='bp-container h-accordion h-accordion-padding_top_extra')
        interestRate = interestRate[1].find('div', class_='kitt-padding kitt-padding_top_none kitt-padding_bottom_none')
        interestRate = interestRate.find('tr')
        interestRate = interestRate.find_all('td')[1]
        interestRate = interestRate.get_text()[:-1].replace(',', '.')

        term = info_cards[1].get_text()
        term = term.split()[-2]
        initial = info_cards[0].get_text().split()[-1][:-1].replace(',', '.')

        maxAmount = info_cards[2].get_text().split()[-3]

        set_info('Семейная ипотека', interestRate, term, initial, maxAmount)

    elif mortgage == 6:
        interestRate = soup.find('span', class_='badge-1F8c8 badge--isThemeDark-3s48O').get_text()
        info_card = soup.find_all('div', class_='creditConditionsValue-3gf_G')


def get_html_with_driver(url):
    #option = webdriver.ChromeOptions()
    #option.add_experimental_option("excludeSwitches", ["enable-automation"])
    #option.add_experimental_option('useAutomationExtension', False)

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1280,800")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    html = None

    driver.get(url=url)
    time.sleep(1000)
    while True:
        try:
            html = driver.page_source
            break
        except Exception as ex:
            logger.error(ex)
            checking_cycle()
            time.sleep(1)

    driver.close()
    driver.quit()

    return html


def checking_cycle():
    global cycle_times
    cycle_times += 1

    if cycle_times >= 10:
        parse(0)
