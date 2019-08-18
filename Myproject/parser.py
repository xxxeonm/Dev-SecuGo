## parser.py

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myproject.settings")
import django
django.setup()

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup


from s_parser.models import AllLanguages
from s_parser.models import BlogData


class ClassInfo:
    language_name = ""
    class_name = ""
    # method_name = ""
    param_name = ""
    link = ""
    score = ""
    pub_date = ""
    etc = ""

    def __init__(self, language_name, class_name, param_name, link, score, pub_date, etc):
        self.language_name = language_name
        self.class_name = class_name
        self.param_name = param_name
        self.link = link
        self.score = score
        self.pub_date = pub_date
        self.etc = etc


# bs4 ver.
# def parse_link():
#     req = requests.get('https://docs.oracle.com/javase/10/docs/api/allclasses-noframe.html')
#     html = req.text
#     soup = BeautifulSoup(html, 'html.parser')
#
#     class_list = soup.select('li > a')
#
#     data = {}
#     for class_item in class_list:
#         print("ALL:::", class_item.text, "LINK:::", class_item.get('href'))
#         # soup = BeautifulSoup(requests.get(class_item.get('href')).text, 'html.parser')
#         # print("DETAIL:::", soup.select('h2'))
#
#     return data


# selenium ver.
def parse_info():
    base_url = 'https://docs.oracle.com/javase/10/docs/api/allclasses-noframe.html'
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.get(base_url)

    ### implicit waits
    driver.implicitly_wait(10)

    class_list = driver.find_elements_by_css_selector('li')
    for class_item in class_list:
        print("ALL:::class_name", class_item.text)
        print("ALL:::link:::", class_item.find_element_by_css_selector('a').get_attribute('href'))

        ### access detail class page
        driver.get(class_item.find_element_by_css_selector('a').get_attribute('href'))
        ### implicit waits
        driver.implicitly_wait(10)

        method_summary = driver.find_element_by_id('method.summary')
        if (method_summary.find_element_by_xpath("..").find_elements_by_tag_name('table')):
            print("DETAIL:::class_name:::", driver.find_element_by_css_selector('.header>.title').text)
        else:
            print("NO 'MEMEBER_SUMMARY' TABLE")

        driver.back()


## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    parse_info()
    # blog_data_dict = parse_info()
    # for t, l in blog_data_dict.items():
    #     BlogData(title=t, link=l).save()