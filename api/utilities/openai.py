import openai
openai.api_key = "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"
openai.organization = "org-M3s4CIjWGwvBbMzjsII5OAcB"


def get_chatgpt_completion(topic):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "text"}
            ])
        return completion
    except Exception as e:
        return None
