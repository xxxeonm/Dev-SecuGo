## parser.py
import requests
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myproject.settings")
import django
django.setup()
from s_parser.models import AllLanguages
from s_parser.models import BlogData

def parse_site():
    req = requests.get('https://docs.oracle.com/javase/10/docs/api/allclasses-noframe.html')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_classNames = soup.select(
        'li > a'
        )
    data = {}
    for title in my_classNames:
        data[title.text] = title.get('href')
    return data

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
if __name__=='__main__':
    blog_data_dict = parse_site()
    for t, l in blog_data_dict.items():
        BlogData(title=t, link=l).save()



