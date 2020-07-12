import os
import nltk
import PyPDF2
import docx2txt
import unidecode
from textmatcher.text_matcher import matcher
import easygui
from infrastructure.aws.Comprehend import ComprehendHandler
import json

file = easygui.fileopenbox()
comprehend = ComprehendHandler()
results = {}

file_object = open('./dataset/file.txt', 'a')
if file.endswith(".pdf"):
    with open(file, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        i = 0
        while reader.getNumPages() > i:
            page = reader.getPage(i)
            i = i + 1
            file_object.write(unidecode.unidecode(page.extractText()))
if file.endswith(".docx"):
    text = docx2txt.process(file)
    file_object.write(unidecode.unidecode(text))

Corpus = matcher.Text(open('./dataset/corpus.txt').read(), 'Corpus')
Text = matcher.Text(open('./dataset/file.txt').read(), 'Test')

string = open('./dataset/file.txt').read()

cantidad_total = 0
for word in string.split():
    cantidad_total += len(word)

language_data = comprehend.get_dominant_language(string[0:4500])

batch_entities = comprehend.get_entities(string[0:4500])

posibles_autores = list(
    map(lambda x: x['Text'], (filter(lambda x: x['Type'] == 'PERSON', batch_entities['ResultList'][0]['Entities']))))

topicos = list(
    map(lambda x: x['Text'], (filter(lambda x: x['Type'] == 'TITLE', batch_entities['ResultList'][0]['Entities']))))


results['titulo'] = file.split("\\")[-1]
results['posibles_autores'] = posibles_autores
results['topicos'] = topicos


matches = matcher.Matcher(Corpus, Text).match()

cantidad_copiada = -15
for match in matches[4]:
    for word in match.split():
        cantidad_copiada += len(word)

results['language'] = language_data['Languages'][0]['LanguageCode']
results['porcentaje_plagio'] = cantidad_copiada/cantidad_total*100
results['citas_originales'] = matches[3]
results['citas_plagio'] = matches[4]

with open('result.json', 'w') as fp:
    json.dump(results, fp)
