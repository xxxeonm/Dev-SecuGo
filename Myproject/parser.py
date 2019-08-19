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

from django.utils import timezone

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

    def toString(self):
        print("LAN:", self.language_name, "CLASS:", self.class_name, "METHOD:", self.method_name, "PARAM:", self.param_name, "LINK:", self.link)

    def __init__(self, language_name, class_name, method_name, param_name, link, score, pub_date, etc):
        self.language_name = language_name
        self.class_name = class_name
        self.method_name = method_name
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

    ### access site [GET]
    driver.get(base_url)
    ### implicit waits
    driver.implicitly_wait(5)

    ### scrap class name and link to detail page
    link_list = driver.find_elements_by_css_selector('li')
    link_data = []; i = 0;
    for link_item in link_list:
        print(i, "ALL:::class_name:::", link_item.text) ### class name
        # print(i, "ALL:::link:::", link_item.find_element_by_css_selector('a').get_attribute('href')) ### link
        link_data.append(ClassLink(class_name=link_item.text, link=link_item.find_element_by_css_selector('a').get_attribute('href')))
        i += 1
        # TODO: remove flag
        if i >= 5: break


    class_data = []; i = 0;
    for class_item in link_data:

        ### access detail class page
        driver.get(class_item.link)
        ### implicit waits
        driver.implicitly_wait(5)

        if (driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_elements_by_tag_name('table')):
            method_data = driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_element_by_tag_name('table')
            # print(i, "DETAIL:::class_name:::", class_item.class_name)
            # print(i, "DETAIL:::link:::", class_item.link)

            method_list = method_data.find_elements_by_class_name('colSecond')
            for j in range(1, len(method_list)):
                ### pre-process method name
                # print(method_list[j].text[0:method_list[j].text.find('(')]) ### method name
                # print(method_list[j].text[method_list[j].text.find('(') + 1:-1]) ### parameter name

                class_data.append(ClassInfo(
                    language_name='java',
                    class_name=class_item.class_name,
                    link=class_item.link,
                    method_name=method_list[j].text[0:method_list[j].text.find('(')],
                    param_name=method_list[j].text[method_list[j].text.find('(') + 1:-1],
                    # TODO: edit score?, pub_date, etc
                    score=-1,
                    pub_date=timezone.now(),
                    etc=""
                ))
        else:
            print(i, "NO 'MEMEBER_SUMMARY' TABLE")

        i += 1
        driver.back()

    driver.close()
    driver.quit()

    return class_data

# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    # blog_data_dict = parse_info()
    # for i in blog_data_dict:
    #     BlogData(title=i.class_name, link=i.link).save()
    all_languages_list = parse_info()
    for item in all_languages_list:
        item.toString()
        AllLanguages(
            languageName=item.language_name,
            className=item.class_name,
            methodName=item.method_name,
            parameterName=item.param_name,
            link=item.link,
            score=item.score,
            pub_date=item.pub_date,
            etc=item.etc
        ).save()