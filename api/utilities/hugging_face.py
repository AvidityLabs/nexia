import requests
import os

# Get the value of an environment variable
DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_TOKEN=os.environ.get('DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_TOKEN')
DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_URL=os.environ.get('DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_URL')
DISTILBERT_BASE_UNCASED_FINETUNED_SST_2_ENGLISH_URL=os.environ.get('DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_TOKEN')
DISTILBERT_BASE_UNCASED_FINETUNED_SST_2_ENGLISH_TOKEN=os.environ.get('DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_URL')



def query_emotions_model(payload):
	headers = {"Authorization": f"Bearer {DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_TOKEN}"}
	response = requests.post(DISTILBERT_BASE_UNCASED_GO_EMOTIONS_STUDENT_MODEL_URL, headers=headers, json=payload)
	return response.json()
	

def query_sentiment_model(payload):
	headers = {"Authorization": f"Bearer {DISTILBERT_BASE_UNCASED_FINETUNED_SST_2_ENGLISH_TOKEN}"}
	response = requests.post(DISTILBERT_BASE_UNCASED_FINETUNED_SST_2_ENGLISH_URL, headers=headers, json=payload)
	return response.json()
	

		