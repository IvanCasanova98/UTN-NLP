import PyPDF2
import boto3
import os
import docx2txt
import unidecode
from infrastructure.aws import S3

s3_client = S3.S3Handler()

s3_client.download_dir("tp-plagio/stage/dataset/","./tmp","utn-nlp")

TEMPORAL_DIRECTORY = './tmp'
try:
    os.remove('./dataset/corpus.txt')
except:
    pass
file_object = open('./dataset/corpus.txt', 'a')
for filename in os.listdir(TEMPORAL_DIRECTORY):
    name = filename.split(".")[0]
    if filename.endswith(".pdf"):
        with open(TEMPORAL_DIRECTORY + "/" + filename, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            i = 0
            while reader.getNumPages() > i:
                page = reader.getPage(i)
                i = i + 1
                file_object.write(unidecode.unidecode(page.extractText()))
    if filename.endswith(".docx"):
        text = docx2txt.process(TEMPORAL_DIRECTORY + "/" + filename)
        file_object.write(unidecode.unidecode(text))
    os.remove(TEMPORAL_DIRECTORY + "/" + filename)
os.rmdir(TEMPORAL_DIRECTORY)
