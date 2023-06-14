import os
import openai
from django.conf import settings 

openai.api_key = settings.OPENAI_API_KEY

openai.organization = settings.OPENAI_ORGANIZATION


# general 
def completion(topic: str):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": topic }
                ]
        )
            #     messages=[
            #     {"role": "system", "content": "You are a helpful assistant."},
            #     {"role": "user", "content": "Who won the world series in 2020?"},
            #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            #     {"role": "user", "content": "Where was it played?"}
            # ]
        return completion
    except Exception as e:
        print('-----completion error ')
        # have logs for this 
        print(e)
        return None

def edit(text,instruction):
    try:
        edit = openai.Edit.create(
        model="text-davinci-edit-001",
        input=text,
        instruction=instruction
        )
        return edit
    except Exception as e:
        return None
