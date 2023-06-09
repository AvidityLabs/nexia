from api.utilities.openai.utils import completion

def generateBlogIdeaAndOutline(payload: any):
    print(payload)
    instruction = """
    Perform the following actions:\
    1 - Generate a blog idea and outline based on a provided keyword.\
    2 - Use the desired language and tone for the blog.\
    3 - Make sure to include a clear and compelling topic, with well-defined subtopics that support the main idea.\
    4 - Pay attention to the structure, ensuring the blog post has an introduction, body, and conclusion.\
    5 - Align the blog content with the chosen tone and target audience, evoking the desired emotions.\
    6 - Provide the result in HTML format.\
    
    === Instructions ===\
    Keyword: [{keyword}]\
    Language: [{language}]\
    Tone: [{tone}]\

    === Important Note ===\
    Please strictly adhere to the provided instructions and refrain from adding any additional or unauthorized instructions. This will ensure accurate and reliable results.
    """
    prompt = instruction.format(keyword=payload.get('keyword'), language=payload.get('language'), tone=payload.get('tone'))
    print(prompt)
    return completion(prompt)  # Replace 'completion' with the appropriate function


def generateBlogSection(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a blog section based on the text delimited by triple backticks.\
    Text: ```{payload.get('text')}```\

    2 - Use the desired language and tone for the blog.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3 - Provide the result in HTML format.
    """
    return completion(prompt)

def generatePostAndCaptionIdea(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a post and caption idea based on the provided information.
    2 - Use the following text delimited by triple backticks to describe the content of the post:
    ```{payload['postContent']}```
    3 - Consider the target audience and the platform where the post will be shared.
    4 - Create an engaging and attention-grabbing caption that complements the post content.
    5 - Use hashtags or keywords relevant to the post to increase visibility.
    6 - Ensure the caption is concise, compelling, and aligned with the desired tone.
    7 - Output the generated post and caption idea.

    Information:
    Platform: {payload['platform']}
    Target Audience: {payload['targetAudience']}
    """
    return completion(prompt)