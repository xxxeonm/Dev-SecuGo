from django.shortcuts import render
from django.http import HttpResponse
from .models import Data
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from nltk.tokenize import sent_tokenize, word_tokenize


def index(request):
    return render(request, 'templates/index.html')

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



def learn(request):
    """
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2019-07-12',
        iam_apikey='FZxffQMR704hKD0dgFXEC8T0L0FFkhWzNImrOWPG6ZVh',
        url='https://gateway.watsonplatform.net/natural-language-understanding/api'
    )
    """
    try:
        authenticator = IAMAuthenticator('FZxffQMR704hKD0dgFXEC8T0L0FFkhWzNImrOWPG6ZVh')
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2019-07-12',
            authenticator=authenticator
        )
        natural_language_understanding.set_service_url('https://gateway.watsonplatform.net/natural-language-understanding/api')

    except expression as identifier:
        print("Watson Api connection error!")

    textinput = request.POST.get('a')

    """Catch the code line!!!"""
    # Python program for KMP Algorithm 
    def KMPSearch(pat, txt): 
        M = len(pat) 
        N = len(txt) 
    
        # create lps[] that will hold the longest prefix suffix  
        # values for pattern 
        lps = [0]*M 
        j = 0 # index for pat[] 
    
        # Preprocess the pattern (calculate lps[] array) 
        computeLPSArray(pat, M, lps) 
    
        i = 0 # index for txt[] 
        while i < N: 
            if pat[j] == txt[i]: 
                i += 1
                j += 1
    
            if j == M: 
                print ("Found pattern at index"+str(i-j))
                print (txt)
                j = lps[j-1] 
    
            # mismatch after j matches 
            elif i < N and pat[j] != txt[i]: 
                # Do not match lps[0..lps[j-1]] characters, 
                # they will match anyway 
                if j != 0: 
                    j = lps[j-1] 
                else: 
                    i += 1
    
    def computeLPSArray(pat, M, lps): 
        len = 0 # length of the previous longest prefix suffix 
    
        lps[0] # lps[0] is always 0 
        i = 1
    
        # the loop calculates lps[i] for i = 1 to M-1 
        while i < M: 
            if pat[i]== pat[len]: 
                len += 1
                lps[i] = len
                i += 1
            else: 
                # This is tricky. Consider the example. 
                # AAACAAAA and i = 7. The idea is similar  
                # to search step. 
                if len != 0: 
                    len = lps[len-1] 
    
                    # Also, note that we do not increment i here 
                else: 
                    lps[i] = 0
                    i += 1
    
    pat = "getParameter"

    #print(sent_tokenize(textinput))
    for i in sent_tokenize(textinput): 
        #print(i)
        KMPSearch(pat, i)
    """Catch the code line!!! end"""


    response = natural_language_understanding.analyze(
        text=textinput,
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
            )
        )
    )

    re = response

    semantic_roles.append(json.dumps(re.result['semantic_roles'][0]['sentence']))
    for h in ['keywords','entities','categories']:
        for i in re.result[h]:
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
    print("saved!")
    reset(Content)
    cont = request.POST.get('a')
    return HttpResponse(source(cont))

def db_compare(comparesource):
    conn = pymysql.connect(host='localhost', user='secugo', password='password', db='test1', charset='utf8')
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


def codeform(request):
    return render(request, 'templates/tem.html')


def compare(request):
    data = request.GET['text']
    return render(request, 'templates/comparecode.html',{"source" : db_compare(data)})


def pro(request):
    return render(request, 'templates/tem.html')


