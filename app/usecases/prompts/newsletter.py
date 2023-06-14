from api.utilities.openai.utils import completion

def generateNewsletterIdea(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a newsletter idea based on the provided information.
    2 - Consider the target audience and purpose of the newsletter.
    3 - Identify a relevant and engaging topic that would interest the subscribers.
    4 - Outline the key sections or topics to include in the newsletter.
    5 - Provide valuable content, such as industry insights, tips, news, or updates.
    6 - Incorporate visuals, such as images or infographics, to enhance the newsletter's appeal.
    7 - Include a call-to-action to encourage reader engagement or conversion.
    8 - Personalize the newsletter by addressing the subscribers by name, if applicable.
    9 - Ensure the tone and language align with the brand and audience.
    10 - Format the newsletter in a visually appealing and easy-to-read manner.
    11 - Proofread and edit the content for clarity, grammar, and coherence.
    12 - Output the resulting newsletter idea in a suitable format.

    Target Audience: {payload['audience']}
    Newsletter Purpose: {payload['purpose']}
    Key Topics/Ideas:
    - Idea 1: {payload['topic1']}
    - Idea 2: {payload['topic2']}
    - Idea 3: {payload['topic3']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)


def generateNewsletterTitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a catchy and attention-grabbing title for a newsletter.
    2 - Consider the target audience, purpose, and content of the newsletter.
    3 - Create a title that reflects the main theme or topic of the newsletter.
    4 - Use language and words that evoke curiosity, interest, or excitement.
    5 - Keep the title concise, clear, and easy to understand.
    6 - Make sure the title aligns with the brand and the tone of the newsletter.
    7 - Output the resulting newsletter title.

    Target Audience: {payload['audience']}
    Newsletter Purpose: {payload['purpose']}
    Key Topics/Ideas: {payload['topics']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)