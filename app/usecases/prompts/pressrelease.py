from api.utilities.openai.utils import completion

def generatePressRelease(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a compelling press release based on the provided information.
    2 - Consider the news or announcement that needs to be conveyed.
    3 - Begin the press release with a strong headline and a concise introductory paragraph that grabs attention.
    4 - Provide relevant details, such as the who, what, when, where, and why of the news or announcement.
    5 - Include quotes from key individuals or stakeholders to add credibility and human interest.
    6 - Highlight the key benefits, features, or impact of the news or announcement.
    7 - Ensure the press release follows proper press release formatting and style.
    8 - Proofread and edit the press release for clarity, accuracy, and professionalism.
    9 - Output the resulting press release in HTML format.

    Press Release Title:
    {payload['title']}

    Press Release Content:
    {payload['content']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)