import csv
import boto3
client = boto3.client(
    'comprehend',
    aws_access_key_id="yolopolo",
    aws_secret_access_key="swag"
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

