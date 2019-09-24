## parser.py

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myproject.settings")
import django
django.setup()

from selenium import webdriver as wd

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


# selenium ver.
def parse_info_php():
    base_url = "https://www.php.net/manual/en/reserved.interfaces.php"
    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')

    ### access site [GET]
    driver.get(base_url)
    ### implicit waits
    driver.implicitly_wait(5)

    ### scrap class name and link to detail page
    link_list = driver.find_element_by_id('reserved.interfaces').find_elements_by_css_selector('li')
    link_data = [];
    for link_item in link_list:
        link_data.append(ClassLink(class_name=link_item.text,
                                   link=link_item.find_element_by_css_selector('a').get_attribute('href')))

    class_data = [];
    for class_item in link_data:

        ### access detail class page
        driver.get(class_item.link)
        ### implicit waits
        driver.implicitly_wait(5)

        if 'class' in driver.find_element_by_class_name('title').text:
            method_list = driver.find_elements_by_class_name('methodsynopsis')
            for method_item in method_list:
                class_data.append(ClassInfo(
                    language_name='php',
                    class_name=class_item.class_name,
                    link=class_item.link,
                    method_name=method_item.find_element_by_class_name('methodname').text,
                    param_name= '' if method_item.find_element_by_class_name('methodparam').text == 'void' else method_item.find_element_by_class_name('methodparam').text,
                    # TODO: edit score?, pub_date, etc
                    score=-1,
                    pub_date=timezone.now(),
                    etc=""
                ))

        driver.back()
        ### implicit waits
        driver.implicitly_wait(5)

    return class_data

def parse_info_java():
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
        link_data.append(ClassLink(class_name=link_item.text,
                                   link=link_item.find_element_by_css_selector('a').get_attribute('href')))
        i += 1
        # TODO: remove flag
        if i >= 10: break


    class_data = []; i = 0;
    for class_item in link_data:

        ### access detail class page
        driver.get(class_item.link)
        ### implicit waits
        driver.implicitly_wait(5)

        if driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_elements_by_tag_name('table'):
            method_data = driver.find_element_by_id('method.summary').find_element_by_xpath("..").find_element_by_tag_name('table')

            method_list = method_data.find_elements_by_class_name('colSecond')
            for j in range(1, len(method_list)):

                ### insert class data into ClassInfo Object List
                class_data.append(ClassInfo(
                    language_name='java',
                    class_name=class_item.class_name,
                    link=class_item.link,
                    ### pre-process method info
                    method_name=method_list[j].text[0:method_list[j].text.find('(')],
                    param_name=method_list[j].text[method_list[j].text.find('(') + 1:-1],
                    # TODO: edit score?, pub_date, etc
                    score=-1,
                    pub_date=timezone.now(),
                    etc=""
                ))

        i += 1
        driver.back()
        ### implicit waits
        driver.implicitly_wait(5)

    driver.close()
    driver.quit()

    return class_data

# 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':

    all_languages_list = parse_info_java()
    all_languages_list.extend(parse_info_php())
    for item in all_languages_list:
        # item.toString()
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
