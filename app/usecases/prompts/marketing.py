from api.utilities.openai.utils import completion

def generateCallToAction(payload: any):
    prompt = f"""
    Perform the following actions:\
    1. Generate a call to action based on the text delimited by triple backticks.\
    Text: ```{payload.get('text')}```\

    2. Use the desired language and tone for the call to action.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3. Write the call to action in a clear and compelling manner using persuasive language and techniques to encourage the reader to take action.\

    4. Provide the result in HTML format.
    """
    return completion(prompt)


