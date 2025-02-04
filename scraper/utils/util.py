"""
Util Funtions
Author: Mustapha ELKAMILI
"""
import json
import os

import lxml
import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from .const import FILE_URLS, FOLDER_DICT, PARENT_FOLDER, URL_START_POINT
from .scrape import clean_folder_name, create_folder, random_name, scrap_page


def dumps_in_json():
    """ saves urls in json """
    with open(r"./urls.json", 'w', encoding='utf-8') as f_urls:
        json.dump(FOLDER_DICT, f_urls)

def get_span_text(div_ele: Tag) -> str:
    """ retrieve the text of the span inside of the 'div' Tag """
    span = div_ele.find('span')
    a_tag = div_ele.find('a')

    if a_tag is not None and a_tag.text:
        return clean_folder_name(a_tag.text)
    
    if a_tag is None and span is not None and span.text:
        return clean_folder_name(span.text)

    return random_name()

def get_li_ul(li_items: ResultSet = None, folder: str= '', start: int = 0):
    """     
        from a 'ul' tag, extract all 'li' and check if the 'li' tag having a href
        or recursive calling the function on the new 'ul' tag
    """
    for element in li_items if li_items is not None else ():
        # record = {}

        # check
        ul_ele = element.find('ul')
        if ul_ele is not None:
            # span
            span_div = element.find('div')
            folder_name = get_span_text(span_div)

            if start == 1 and folder_name not in {'LIBRARY'}:
                continue

            sub_f = os.path.join(folder, folder_name)

            create_folder(sub_f)
            get_li_ul(ul_ele.find_all('li', recursive=False), sub_f)
            # report[folder] = record
            continue

        # 'a' Tag
        href = element.find('a').get('href')
        sub_f = os.path.join(folder, clean_folder_name(element.find('a').text))
        create_folder(sub_f)

        # calling a href_scraper
        scrap_page(href, sub_f)


def start():
    """ starting point """
    res_path = os.path.join(os.getcwd(), PARENT_FOLDER)
    print(f"Creating {res_path} to save files ... ")
    create_folder(res_path)

    print(f"Start scraping {URL_START_POINT} site ... ")

    try:
        response = requests.get(URL_START_POINT, headers={"User-Agent":"Mozilla/5.0"})
    except requests.ConnectionError as err:
        print(err)
        return

    if response.status_code != 200:
        print(f"Error while requesting {URL_START_POINT}")
        return

    print("Getting source page ...")
    start_page = BeautifulSoup(response.content, "lxml-xml")

    nav_bar = start_page.header
    if nav_bar is None:
        print("No Header in source page ...")
        return

    nav_bar = nav_bar.find_all('nav')
    if nav_bar is None and len(nav_bar) < 2:
        print("No 'nav' tag ... ")
        return

    nav_bar = nav_bar[1].div
    if nav_bar is None:
        print("No 1st 'div' in source page ...")
        return

    nav_bar = nav_bar.div
    if nav_bar is None:
        print("No 2nd 'div' in source page ...")
        return

    get_li_ul(nav_bar.find('ul').find_all('li', recursive=False), res_path, 1)

    # back up
    with open(r"./urls.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(FILE_URLS))
