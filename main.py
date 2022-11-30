import requests
import lxml
import re
from pprint import pprint
from fake_headers import Headers
from bs4 import BeautifulSoup

def get_headers():
    return Headers(browser='chrome', os='win').generate()

def get_params():
    return {
        'text': 'python',
        'area': [1, 2]
    }

def get_links(url):
    res_list = []
    attr_comp = {'data-qa': "vacancy-serp__vacancy-employer"}
    regexp_salary = re.compile(r'(от\s)|(до\s)*\s?(\d+)\\xa?0{1}(0{3})(\s*[A-Z]*[а-я]*\D*)')
    req = requests.get(url=url, headers=get_headers(), params=get_params())
    soup = BeautifulSoup(req.text, 'lxml')
    items_links = soup.find_all("a", class_="serp-item__title")
    items_companies = soup.find_all("a", attrs=attr_comp)
    for i, item in enumerate(items_links):
        res_list.append({
            'title': item.contents[0],
            'link': item.attrs['href'],
            'company': items_companies[i].text,
            'salary': regexp_salary.sub(r'\1\2\3\4\5', get_salary(item.attrs['href']))
            })
    return res_list

def get_salary(url):
    req = requests.get(url=url, headers=get_headers())
    soup = BeautifulSoup(req.text, 'lxml')
    salary = soup.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
    text = salary.text
    
    return text

if __name__ == "__main__":
    url = 'https://spb.hh.ru/search/vacancy'
    
    pprint(get_links(url))
