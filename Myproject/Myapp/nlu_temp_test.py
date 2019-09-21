import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    iam_apikey='FZxffQMR704hKD0dgFXEC8T0L0FFkhWzNImrOWPG6ZVh',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

response = natural_language_understanding.analyze(
    #url='www.ibm.com',
    text='IBM is an American multinational technology company '
       'headquartered in Armonk, New York, United States, '
       'with operations in over 170 countries.',
    features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()

print(json.dumps(response, indent=2))