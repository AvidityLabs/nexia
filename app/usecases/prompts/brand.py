from api.utilities.openai.utils import completion

def generateTagLineAndHeadline(payload):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a tagline and headline based on the following key points described in the text delimited by tripple backticks.
    2 - The language should be in ```{payload.language}```, with a tone that is ```{payload.tone}```.\
    3 - Make sure to include key words and phrases that accurately reflect the brand or product being promoted.\
    4 - Also, make sure that the tagline and headline are concise and easily understandable by the target audience.\
    5 - Use persuasive language to create a sense of urgency and inspire the audience to take action.\
    6 - Ensure that the tagline and headline are unique and memorable in order to make a lasting impression.\
    7 - Output the result in HTML format.
    
    Text:
    ```{payload.keyPoints}```
    """
    return completion(prompt)



def generateBrandName(payload):
    # [Specify the desired brand image, e.g., modern, sophisticated, playful]
    # [Describe the purpose or mission of the brand
    prompt = f"""
    Perform the following actions:\
    1 - Generate a brand name that reflects the desired brand image and purpose. Consider the target audience and desired tone and style.\
    2 - The output should be a brand name that resonates with customers and effectively represents the brand's identity.\
    3 - Utilize creativity and uniqueness to craft a memorable and distinctive brand name.\
    4 - Consider any specific keywords or themes that should be incorporated into the brand name.\
    5 - Output the result in HTML format\

    Instructions:\

    Desired Brand Image: The specified brand image is described in the following text delimited by tripple backticks Brand Image:```{payload.get('brandImage')}```\
    Brand Purpose: The purpose or mission of the brand is described in the following text delimited by tripple backticks Purpose:```{payload.get('purpose')}```\
    Target Audience: The target audience for the brand is described in the following text delimited by tripple backticks Audience:```{payload.get('audience')}```\
    Tone and Style: The desired tone and style of the brand name is described in the following text delimited by tripple backticks Audience:```{payload.get('tone')}```\
    Language: The language of the brand name is described in the following text delimited by tripple backticks Audience:```{payload.get('language')}```\
    Generate a compelling brand name that aligns with the provided instructions. The brand name should effectively represent the desired brand image, purpose, target audience, and tone. Ensure it is unique, memorable, and capable of resonating with customers.
    """
    return completion(prompt)