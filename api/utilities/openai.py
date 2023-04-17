from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
import requests

import os

# Get the value of an environment variable
X_RAPID_API_KEY = os.environ.get('X_RAPID_API_KEY')
X_RAPID_API_HOST = os.environ.get('X_RAPID_API_HOST')


HEADERS =  {
        "X-RapidAPI-Key": f"{X_RAPID_API_KEY}",
        "X-RapidAPI-Host": f"{X_RAPID_API_HOST}",
        "Content-Type": "application/json"
    }

def get_models():
    try:
        url = "https://openai80.p.rapidapi.com/models"

        response = requests.request("GET", url, headers=HEADERS)
        return response.json()
    except Exception as e:
        return str(e)




"""
On the other hand, the create_completion endpoint is intended for use cases where you want 
to generate a new text based on a given prompt. The generated text can be completely 
new and original, or it can be a continuation of the prompt.
"""
def create_completion(
        model,
        prompt_text,
        max_tokens, temperature, top_p, n, stream, logprobs, stop):
    url = "https://openai80.p.rapidapi.com/completions"

    payload = {
        "model": model,
        "prompt": prompt_text,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "n": n,
        "stream": stream,
        "logprobs": logprobs,
        "stop": stop
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()



"""
The edit endpoint is intended for use cases where you want to make specific modifications 
to a given input text based on a provided instruction. This could be useful,
for example, when you want to summarize a long piece of text, or when you want 
to rephrase a sentence to make it more concise.
"""
def create_edit(model, input, instruction):
    url = "https://openai80.p.rapidapi.com/edits"

    payload = {
        "model": f"{model}",
        "input": f"{input}",
        "instruction": f"{instruction}"
    }
    response = requests.request("POST", url, json=payload, headers=HEADERS)
    return response.json()
