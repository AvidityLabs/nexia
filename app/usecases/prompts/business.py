
from api.utilities.openai.utils import completion

def generateBusinessIdea(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate unique business ideas based on the text delimited by triple backticks.\
    Text: ```{payload.text}```\

    2 - Use the desired language and tone for the ideas.\
    Language: ```{payload.language}```\
    Tone: ```{payload.tone}```\

    3 - Provide the result in HTML format.
    """
    return completion(prompt)


def generateBusinessIdeaPitch(payload: any):
    prompt = f"""
    Perform the following actions:\
    1. Generate a business idea pitch based on the text delimited by triple backticks.\
    Text: ```{payload.get('businessIdea')}```\

    2. Use the desired language and tone for the pitch.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3. Include any relevant statistics or data that support the viability of the business idea, and a clear call-to-action for the audience.\

    4. Indicate the target audience for the pitch, so that it can be tailored accordingly. Ensure that the pitch is easy to understand by the general public, not just by industry experts.\

    5. Provide the result in HTML format.
    """
    return completion(prompt)