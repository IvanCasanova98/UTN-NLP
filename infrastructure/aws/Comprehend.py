import boto3
import os

region = "us-east-2"

class ComprehendHandler:

    def __init__(self):
        try:
            import config
            AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
            AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
        except:
            AWS_ACCESS_KEY_ID = os.getenv("SECRET_ACCESS_KEY")
            AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_SECRET_KEY")
        self.client = boto3.client('comprehend',region_name=region,aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def get_entities(self, text):
        response = self.client.batch_detect_entities(
            TextList=[
                text,
            ],
            LanguageCode='es')
        return response

    def get_dominant_language(self,text):
        response = self.client.detect_dominant_language(
            Text=text
        )
        return response

    def get_key_phrases(self, text):
        response = self.client.detect_key_phrases(
            Text=text,
            LanguageCode='es')
        return response
