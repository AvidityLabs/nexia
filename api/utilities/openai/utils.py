import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

openai.organization = os.environ.get('OPENAI_ORGANIZATION')


# general 
def completion(topic):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "text"}
            ])
        return completion
    except Exception as e:
        return None
