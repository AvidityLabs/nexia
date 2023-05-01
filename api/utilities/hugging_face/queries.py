import requests
import os

# Get the value of an environment variable
EMOTION_MODEL_TOKEN=os.environ.get('EMOTION_MODEL_TOKEN')
EMOTION_MODEL_URL=os.environ.get('EMOTION_MODEL_URL')
SENTIMENT_MODEL_URL=os.environ.get('SENTIMENT_MODEL_URL')
SENTIMENT_MODEL_TOKEN=os.environ.get('SENTIMENT_MODEL_TOKEN')


# https://huggingface.co/j-hartmann/emotion-english-distilroberta-base
def query_emotions_model(payload):
	headers = {"Authorization": f"Bearer {EMOTION_MODEL_TOKEN}"}
	try:
		response = requests.post(EMOTION_MODEL_URL, headers=headers, json=payload)
		return response.json()
	except Exception as e:
		return None

# https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment
def query_sentiment_model(payload):
	headers = {"Authorization": f"Bearer {SENTIMENT_MODEL_TOKEN}"}
	try:
		response = requests.post(SENTIMENT_MODEL_URL, headers=headers, json=payload)
		return response.json()
	except Exception as e:
		return None
	

		