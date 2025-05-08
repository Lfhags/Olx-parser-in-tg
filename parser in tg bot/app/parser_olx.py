from urllib import request
from numpy import info
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_unique_filename(base_name):
    counter = 1
    filename = f"{base_name}.xlsx"
    while os.path.exists(filename):
        filename = f"{base_name}{counter}.xlsx"
        counter += 1
    return filename

def parser_olx(url):
    info = []

    storage_number = 1

    base_link = 'https://www.olx.ua'
    link = url

    for storage_number in range(1):
        response = requests.get(f'{link}?page={storage_number}').text
        soup = BeautifulSoup(response, 'lxml')

        block = soup.find('div', class_="css-j0t2x2")
        all_announcement = block.find_all('div', class_ = 'css-l9drzq')

        for announcement in all_announcement:
            relative_link = announcement.find('a').get('href')
            announcement_link = base_link + relative_link

            price_element = announcement('p', class_ = 'css-uj7mm0')  # type: ignore
            price = price_element[0].get_text(strip=True)

            description_response = requests.get(announcement_link).text
            description_soup = BeautifulSoup(description_response, 'lxml')

            title_element = description_soup.find('h4', class_='css-10ofhqw')
            title = title_element.text.strip() if title_element else 'Без назви'
            
            description_element = description_soup.find('div', class_='css-19duwlz')
            description = description_element.text.strip() if description_element else 'Без опису'

            info.append({
                'Назва:': title,
                'Ціна:': price,
                'Опис:': description,
                'Посилання на товар:': announcement_link
            })

            print("_ _ _ _ _ _ _")
            print(f'\n{title}, link: {announcement_link}')
            print(f'\nЦіна: {price}')
            print(f'\nОпис: {description}')
            print("_ _ _ _ _ _ _")

    df = pd.DataFrame(info)
    output_filename = get_unique_filename('parsing_done')
    df.to_excel(output_filename, index=False, engine='openpyxl')
    return output_filename