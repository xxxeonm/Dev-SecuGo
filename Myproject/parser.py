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

class ClassLink:
    class_name = ""
    link = ""

    def __init__(self, class_name, link):
        self.class_name = class_name
        self.link = link

class ClassInfo:
    language_name = ""
    class_name = ""
    method_name = ""
    param_name = ""
    link = ""
    score = ""
    pub_date = ""
    etc = ""

    def __init__(self, language_name, class_name, method_name, param_name, link, score, pub_date, etc):
        self.language_name = language_name
        self.class_name = class_name
        self.method_name = method_name
        self.param_name = param_name
        self.link = link


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

    ### access site [GET]
    driver.get(base_url)
    ### implicit waits
    driver.implicitly_wait(5)

    ### scrap class name and link to detail page
    link_list = driver.find_elements_by_css_selector('li')
    link_data = []; i = 0;
    for link_item in link_list:
        print(i, "ALL:::class_name:::", link_item.text) ### class name
        print(i, "ALL:::link:::", link_item.find_element_by_css_selector('a').get_attribute('href')) ### link
        link_data.append(ClassLink(class_name=link_item.text, link=link_item.find_element_by_css_selector('a').get_attribute('href')))
        i += 1
        if i >= 20: break


    class_data = []; i = 0;
    for class_item in link_data:

        ### access detail class page
        driver.get(class_item.link)
        ### implicit waits
        driver.implicitly_wait(5)

        if (driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_elements_by_tag_name('table')):
            method_data = driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_element_by_tag_name('table')
            print(i, "DETAIL:::class_name:::", class_item.class_name)
            print(i, "DETAIL:::link:::", class_item.link)

            method_list = method_data.find_elements_by_class_name('colSecond')
            for j in range(1, len(method_list)):
                print(method_list[j].text)
                ### pre-process method name

            # print(i, "DETAIL:::method_name:::", class_item.link)
            # print(i, "DETAIL:::param_name:::", class_item.link)
            # class_data.append(ClassInfo(
            #     language_name='java',
            #     class_name=class_item.class_name,
            #     link=class_item.link,
            #     method_name=,
            #     param_name=
            # ))
        else:
            print(i, "NO 'MEMEBER_SUMMARY' TABLE")

        i += 1
        driver.back()

    driver.quit()


## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    parse_info()
    # blog_data_dict = parse_info()
    # for t, l in blog_data_dict.items():
    #     BlogData(title=t, link=l).save()