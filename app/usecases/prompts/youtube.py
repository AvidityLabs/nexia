from api.utilities.openai.utils import completion
from api.utilities.langchain.config import openai_wrapper
from langchain.prompts.chat import ChatPromptTemplate
from api.utilities.openai.utils import completion
from api.utilities.langchain.config import openai_wrapper


def generateYoutubeChannelDescription(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a YouTube channel description for a channel based on the following text delimited by tripple backticks in {prompt.language} language with a tone that is {prompt.tone}.\
    2 - Include a detailed and clear overview of the channel, including the type of content, target audience, and unique selling points.\
    3 - Include a call-to-action, encouraging viewers to subscribe to the channel.\
    4 - Use appropriate keywords to optimize the channel description for search engines and make sure to align the tone with the channel's purpose and target audience.\
    5 - Output the result in HTML format.

    Text:
    ```{payload.channelDescription}```       
    """
    
    #     template_string = """
    # You are a help assistant that generates an email and the text style that is translated into {language} in a {tone} and is formatted into HTML format. Based on the text: ```{text}```
    # """

    # human_template = "{text}"

    # chat_prompt = ChatPromptTemplate.from_messages([
    #     ("system", template_string),
    #     ("human", human_template),
    # ])

    # formatted_messages = chat_prompt.format_messages(
    #     language=payload.get('language'),
    #     tone=payload.get('tone'),
    #     text=payload.get('email_content')
    # )
    

    # return formatted_messages
    # return openai_wrapper.get_response(prompt)


def generateYoutubeVideoDescription(payload):
    template_string ="""
    You are a help assistant that generates a youtube video description with the text style that is translated into {language} in a {tone} and is formatted into HTML format. Based on the following Text:
    
    Perform the following actions:
    1 - Generate a YouTube video description based on the following text delimited by triple backticks in {language} language, with a tone that is {tone}.\

    2 - Include a brief summary of the video content, highlighting the key points and main takeaways.\

    3 - Include relevant keywords and hashtags to optimize the video for search engines.\

    4 - Use persuasive language to encourage viewers to watch the video and to subscribe to your channel.\

    5 - Include a call-to-action, such as asking viewers to leave a comment or to check out a related video or website.\

    6 - Output the result in HTML format.

    Text: ```{text}```
    """


    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template_string),
        ("human", human_template),
    ])

    formatted_messages = chat_prompt.format_messages(
        language=payload.get('language'),
        tone=payload.get('tone'),
        text=payload.get('videoDescription')
    )

    return formatted_messages


def generateYouTubeVideoScript(payload):
    template_string = """
    You are a help assistant that generates a youtube video script with the text style that is translated into {language} in a {tone} and is formatted into HTML format. Based on the following Text:
    
    
    Text: {text}
    """
    
    human_template = "{text}"

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", template_string),
        ("human", human_template),
    ])
    
    formatted_messages = chat_prompt.format_messages(
        language=payload.get('language'),
        tone=payload.get('tone'),
        text=payload.get('videoDescription')
    )

    return formatted_messages