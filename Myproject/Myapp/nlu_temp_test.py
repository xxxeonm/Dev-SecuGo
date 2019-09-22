import json
from .models import Data
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    iam_apikey='FZxffQMR704hKD0dgFXEC8T0L0FFkhWzNImrOWPG6ZVh',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

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
count = 0

response = natural_language_understanding.analyze(
    url='https://www.owasp.org/index.php/Top_10-2017_A7-Cross-Site_Scripting_(XSS)',
    #text='IBM is an American multinational technology company '
    #   'headquartered in Armonk, New York, United States, '
    #   'with operations in over 170 countries.',
    #features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()
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
print(count)
count = count + 1

print(semantic_roles[0].__str__().split('"'))
#data = Data(seq=count, keywords=Content['keywords']['text'][0], entities=Content['entities']['text'],
#            categories=Content['categories']['text'],
#            desc=semantic_roles[0].__str__().split('"'), source='', etc='')
#data.save()
#print(json.dumps(response, indent=2))
