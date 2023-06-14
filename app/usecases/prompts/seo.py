from api.utilities.openai.utils import completion

def generateSeoMetaTitle(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate an SEO meta title based on the provided information.
    2 - Use the following text delimited by triple backticks to describe the content or topic for which the SEO meta title is needed:
    ```{payload['content']}```
    3 - Consider the target audience and the purpose of the content when crafting the meta title.
    4 - Ensure the meta title is concise, compelling, and accurately reflects the content's topic or main idea.
    5 - Incorporate relevant keywords or phrases to improve search engine visibility.
    6 - Optimize the meta title length to fit within the recommended character limit for search engines.
    7 - Output the generated SEO meta title.

    Information:
    Target Audience: {payload['targetAudience']}
    Content Type: {payload['contentType']}
    """
    return completion(prompt)