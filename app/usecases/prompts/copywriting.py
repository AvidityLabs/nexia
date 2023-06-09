from api.utilities.openai.utils import completion

def generateCopywritingFrameworkAIDA(payload: any):
    prompt = f"""
    Perform the following actions:\
    1 - Generate a copywriting framework using AIDA (Attention, Interest, Desire, Action) for a product or brand, described in the following text delimited by triple backticks.\
    Description: ```{payload.get('description')}```\

    2 - Use the desired language and tone for the copywriting framework.\
    Language: ```{payload.get('language')}```\
    Tone: ```{payload.get('tone')}```\

    3 - Ensure that the generated copy grabs the attention of the audience, creates interest in the product or brand, builds desire for the product or brand, and creates a sense of urgency to take action.\

    4 - Provide the result in HTML format.
    """
    return completion(prompt)