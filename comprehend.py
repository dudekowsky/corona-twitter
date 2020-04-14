from dotenv import load_dotenv
import os
import csv
import boto3

load_dotenv()
client = boto3.client(
    'comprehend',
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key")
)

def process(row):
	response = client.detect_sentiment(Text=row['text'], LanguageCode=row['lang'])
	output_file = open("mytextoutput.txt", "a")
	writer = csv.writer(output_file)
	writer.writerow([row['status_id'], response['Sentiment']])
	output_file.close()

with open('./preprocessed/FILENAME', newline='') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		process(row)

