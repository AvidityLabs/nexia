from api.utilities.openai.utils import completion

def generateSalesCopy(payload):
    prompt = f"""
    Perform the following actions:
    1 - Generate compelling and persuasive sales copy for a product or service.
    2 - Consider the target audience, product features, and unique selling points.
    3 - Highlight the benefits and value proposition of the product/service.
    4 - Use persuasive language and techniques to create a sense of urgency and desire.
    5 - Craft a strong call-to-action that encourages the reader to take immediate action.
    6 - Ensure the sales copy aligns with the brand and desired tone.
    7 - Output the resulting sales copy.

    Product/Service: {payload['product']}
    Target Audience: {payload['audience']}
    Unique Selling Points: {payload['usp']}
    Key Features: {payload['features']}

    Language: {payload['language']}
    Tone: {payload['tone']}
    """
    return completion(prompt)