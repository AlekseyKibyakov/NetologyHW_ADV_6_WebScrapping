import requests
import lxml
import re
import time
import json
from alive_progress import alive_bar
from pprint import pprint
from fake_headers import Headers
from bs4 import BeautifulSoup

def get_headers():
    return Headers(browser='chrome', os='win').generate()

def get_params(page_num):
    return {
        'text': 'python',
        'area': [1, 2],
        'page': page_num
    }

def get_links(url, res_list, page_num):
    attr_comp = {'data-qa': "vacancy-serp__vacancy-employer"}
    attr_adress = {'data-qa': "vacancy-serp__vacancy-address"}
    regexp_search = r'.*((D|d)jango).*((F|f)lask).*'
    req = requests.get(url=url, headers=get_headers(), params=get_params(page_num))
    soup = BeautifulSoup(req.text, 'lxml')
    items_links = soup.find_all("a", class_="serp-item__title")
    items_companies = soup.find_all("a", attrs=attr_comp)
    items_adresses = soup.find_all(attrs=attr_adress)
    
    for i, item in enumerate(items_links):
        with alive_bar(title=f'Page {page_num+1} Vacancy {i+1}') as bar:
            sal_and_desc = get_salary_and_vacancy_description(item.attrs['href'])
            if re.match(regexp_search, sal_and_desc[1]):
                # if 'USD' in sal_and_desc[0]:
                    res_list.append({
                        'title': item.contents[0],
                        'link': item.attrs['href'],
                        'company': items_companies[i].text,
                        'salary': sal_and_desc[0],
                        'city': items_adresses[i].text
                        })
            time.sleep(0.1)
            bar()        

def get_salary_and_vacancy_description(url):
    while True:
        req = requests.get(url=url, headers=get_headers())
        attr_description = {'data-qa': "vacancy-description"}
        soup = BeautifulSoup(req.text, 'lxml')
        salary = soup.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
        if salary is None:
            time.sleep(0.2)
            continue
        description = soup.find(attrs=attr_description)
        text_salary = salary.text.replace('\xa0', "")
        return [text_salary, description.text]

if __name__ == "__main__":
    url = 'https://spb.hh.ru/search/vacancy'
    result = []
    counter = 0
    t = 0.3
    # while True:
    while True:
        response = requests.get(url=url, headers=get_headers(), params=get_params(counter))
        time.sleep(t)
        if 100 < response.status_code < 300:
            get_links(url, result, counter)
            counter += 1
        else:
            print("The End!")
            break
        

    with open('vacancies.json', 'w', encoding='utf-8') as v:
        json.dump(result, v, ensure_ascii=False)
            

    