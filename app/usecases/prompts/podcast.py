from api.utilities.openai.utils import completion

def generatePodcastIdea(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a unique and captivating podcast idea based on the provided information.
    2 - Consider the target audience, niche, and overall theme of the podcast when brainstorming the idea.
    3 - Incorporate relevant keywords, trends, or current topics to make the podcast idea timely and appealing.
    4 - Highlight the main purpose or value proposition of the podcast, such as education, entertainment, or inspiring stories.
    5 - Ensure that the podcast idea is specific, concise, and easily understandable for potential listeners.
    6 - Include potential episode topics or segments that can be covered in the podcast to give a clearer picture of the content.
    7 - Output the resulting podcast idea.

    Podcast Niche:
    {payload['niche']}

    Target Audience:
    {payload['audience']}

    Main Theme:
    {payload['theme']}
    """
    return completion(prompt)


def generatePodcastTitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate a catchy and engaging podcast title based on the provided information.
    2 - Consider the podcast niche, target audience, and main theme when creating the title.
    3 - Use attention-grabbing words, intriguing phrases, or wordplay to make the title memorable and enticing.
    4 - Ensure that the title accurately represents the content and tone of the podcast.
    5 - Keep the title concise and easy to understand, avoiding overly complex or confusing wording.
    6 - Output the resulting podcast title.

    Podcast Niche:
    {payload['niche']}

    Target Audience:
    {payload['audience']}

    Main Theme:
    {payload['theme']}
    """
    return completion(prompt)