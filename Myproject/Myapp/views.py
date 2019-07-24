from django.shortcuts import render
from django.http import HttpResponse
from .models  import Data
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from django.http import HttpResponseRedirect
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from django.views.decorators.csrf import csrf_exempt
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions
import pymysql


source = ''
Content = {
    'keywords': {
        'text': [],
        'score': []
    },
    'entities': {
        'text': [],
        'score': []
    },
    'categories': {
        'text': [],
        'score': []
    },
}
semantic_roles = []



def Know(text):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username='acdb979b-4643-461e-a34f-02ff2271210a',
        password='5xDqzWdlyeao',
        version='2018-03-16')

    response = natural_language_understanding.analyze(
        text= text,
        features=Features(
        entities=EntitiesOptions(
        emotion=False,

        ),
        categories=EntitiesOptions(
        emotion=False,
        ),
        semantic_roles=EntitiesOptions(
      emotion=False,
      sentiment=False,
      ),
    keywords=KeywordsOptions(
      emotion=False,
      sentiment=False,
      )))

    re = response

    semantic_roles.append(json.dumps(re['semantic_roles'][0]['sentence']))
    for h in ['keywords','entities','categories']:
        for i in re[h]:
            try:
                try:
                    if (float(json.dumps(i['relevance'])) > 0.3):
                        Content[h]['text'].append(i['text'])
                        Content[h]['score'].append(i['relevance'])
                    else:
                        pass
                except:
                    if (float(json.dumps(i['relevance'])) > 0.3):
                        Content[h]['text'].append(i['label'])
                        Content[h]['score'].append(i['relevance'])
                    else:
                        pass

            except:
                try:
                    if (float(json.dumps(i['score'])) > 0.3):
                        Content[h]['text'].append(i['text'])
                        Content[h]['score'].append(i['score'])
                    else:
                        pass
                except:
                    if (float(json.dumps(i['score'])) > 0.3):
                        Content[h]['text'].append(i['label'])
                        Content[h]['score'].append(i['score'])
                    else:
                        pass

    count = Data.objects.count()
    count = count + 1
    data = Data(seq=count, keywords=Content['keywords']['text'][0], entities=Content['entities']['text'],
                categories=Content['categories']['text'],
                desc=semantic_roles[0].__str__().split('"'), source='', etc='')
    data.save()


def db_compare(comparesource):
    conn = pymysql.connect(host='localhost', user='root', password='password', db='test1', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select * from test"
    number_of_rows = curs.execute(sql)
    rows = curs.fetchall()
    keysource = []
    num = 0
    a = comparesource.split('\n')

    for i in range(number_of_rows):
        keysource.insert(num,rows[i]['keysource'])
        num+=1

    for i in keysource:
        for k in range(number_of_rows):
            if(rows[k]["keysource"]==i):
                rownum = k

        for j in a:
            fin = j.find(i)

            if(fin != -1):
                result = str(a.index(j)+1)+"번 째 줄 "+"\n" + j +"\n"\
                +"keyword= "+str(rows[rownum]["keyword"])+"\n"\
                + "category= "+str(rows[rownum]["category"])+"\n"\
                +"description= "+str(rows[rownum]["description"])+"\n"\
                +"url= " + str(rows[rownum]["url"])+"\n"\
                +"source= "+str(rows[rownum]["source"])+"\n"\
                +"keysource= " + str(rows[rownum]["keysource"])

            else:
                continue

    return result


def sync(comparesource):
    fin = comparesource.find('request.getParameter')
    first = comparesource.find('String')
    end = comparesource.find(';',fin)
    a =''
    for i in range(first,end) :
        a +=comparesource[i]

    return  a


def reset(Content):
    for h in ['keywords', 'entities', 'categories']:
        Content[h]['text'].clear()
        Content[h]['score'].clear()
    semantic_roles.clear()



def source(te):
    re = []
    return te.split(";")[0]


def index(request):
    return render(request, 'tem.html')


def compare(request):
    data = request.GET['text']
    return render(request, 'comparecode.html',{"source" : db_compare(data)})


def pro(request):

    reset(Content)
    cont = request.POST.get('a')

    return HttpResponse(source(cont))

