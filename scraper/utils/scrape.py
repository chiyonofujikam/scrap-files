"""
Given a html page, retrieves all href that has a file in it or other urls to do the same
Author: Mustapha ELKAMILI
"""
import os
import random
from io import BytesIO
from time import sleep

import lxml
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from tqdm import tqdm

from .const import (EXTENSIONS, FILE_URLS, FOLDER_NAMES, URL_CHECKED,
                    URL_START_POINT)


def create_folder(name: str) -> None:
    """ checks and creates a folder """
    if not os.path.exists(name):
        os.makedirs(name)

def random_name() -> str:
    """ makes a random name """
    res = f'Unfound span {random.randint(0, 1_000_000)}'
    while res in FOLDER_NAMES:
        res = f'Unfound_{random.randint(0, 1_000_000)}'
        continue

    FOLDER_NAMES.update({res})
    return res

def clean_folder_name(name: str) -> str:
    """ removes undesirect caracteres frome the name """
    return name.strip().replace(' ', '_'
                        ).replace('\n', ''
                        ).replace('?', ''
                        ).replace('%20', ' '
                        ).replace('/', '_'
                        ).replace(':', '_'
                        ).replace('#', '')

def write_into_file(file_name: str, ext: str, content) -> None:
    """ writes into a file """
    with open(f"{file_name}.{ext}", 'wb') as f:
        f.write(content)

def save_file(url: str, folder: str):
    """ saves the founded file """
    if url in FILE_URLS:
        return

    try:
        response = requests.get(url)
    except requests.exceptions.ChunkedEncodingError as err:
        print(err)
        return

    content = response.content

    FILE_URLS.add(url)

    if ".pdf" in url.lower():
        file_name = os.path.join(folder,
                    clean_folder_name(url.split('.pdf', maxsplit=1)[0].split('/')[-1]))        
        write_into_file(file_name, 'pdf', content)
        return

    if ".docx" in url.lower():
        file_name = os.path.join(folder,
                    clean_folder_name(url.split('.docx', maxsplit=1)[0].split('/')[-1]))
        write_into_file(file_name, 'docx', content)
        return

    if ".doc" in url.lower():
        file_name = os.path.join(folder,
                    clean_folder_name(url.split('.doc', maxsplit=1)[0].split('/')[-1]))
        write_into_file(file_name, 'doc', content)
        return

    if ".zip" in url.lower():
        file_name = os.path.join(folder,
                    clean_folder_name(url.split('.zip', maxsplit=1)[0].split('/')[-1]))
        write_into_file(file_name, 'zip', content)
        return

    if ".7z" in url.lower():
        file_name = os.path.join(folder,
                    clean_folder_name(url.split('.7z', maxsplit=1)[0].split('/')[-1]))
        write_into_file(file_name, '7z', content)
        return

    if 'xlsx' in url.lower():
        file_name = os.path.join(folder,
                    clean_folder_name(url.split('.xlsx', maxsplit=1)[0].split('/')[-1]))
        try:
            load_workbook(filename=BytesIO(content)).save(f"{file_name}.xlsx")
        except Exception as esc:
            print(f"Error while saving {url} : {esc}")
        return

    sleep(0.5)

    print(f"No extension found in 'url': {url}")
    return

def scrap_page(url: str, folder: str):
    """ get files form url page """
    url = url if url else ''
    url = (url if url.startswith(URL_START_POINT) else '') if url.startswith('http') else URL_START_POINT + url

    if not url:
        return

    if url in URL_CHECKED:
        return
    URL_CHECKED.add(url)

    # print(f'checking {url} ... ')
    if any(ext in url.lower() for ext in EXTENSIONS):
        save_file(url, folder)
        return

    try:
        response = requests.get(url) # , headers={"User-Agent":"Mozilla/5.0"}
    except requests.ConnectionError as err:
        print(err)
        return

    if response.status_code != 200:
        print(f"Error while requesting {url}")
        return

    # beautify html page
    start_page = BeautifulSoup(response.content, "lxml-xml")

    artical = start_page.find_all('article')
    if artical is None:
        print(f"No 'artical' in {url} ...")
        return

    # creation of sub folder
    sub_f = os.path.join(folder, clean_folder_name(url.replace(URL_START_POINT, '')))
    create_folder(sub_f)

    # extraction of hrefs
    print(f"checking 'a' tags of {url}...")

    for art in artical:
        if art.get('class') is not None:
            continue

        for a_tag in art.find_all('a'):
            scrap_page(a_tag.get('href'), sub_f)

        break

    # Huminize scraping
