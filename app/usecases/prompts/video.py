from api.utilities.openai.utils import completion


def generateVideoScript(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a video script.\
    2 - The video script should align with the following guidelines:"\
    3- Please cover the following main points in the video script in the text delimited by tripple backticks:\
       
       Key Points:\
       ```{payload.get('keyPoints')}```\
    4 - The video script should have a tone as described in the text delimited by angle brackets, appealing to target audience in the text delimited by tripple dashes."\
        
        Tone:\
        <{payload.get('tone')}>\

        Audience:\
        ---{payload.get('audience')}---\

    5 - The key messages to convey in the video script are in the following text delimited by XML tags. At the end, please include a call to action encouraging viewers to subscribe."\

        Message:
        <tag>{payload.get('message')}</tag>

    6 - The video script should be approximately have a duration mentioned in the following text delimited by backticks and formatted in a formated style, including scene descriptions, dialogue, and narration."\

        Duration:
        ```{payload.get('duration')}```

    7 - You are encouraged to provide a creative, engaging, and coherent video script that captures the viewers' attention and effectively conveys the desired messages."\
    8 - Output the result in HTML format 

    """
    return completion(prompt)
